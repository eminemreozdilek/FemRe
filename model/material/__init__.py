from dataclasses import dataclass
import numpy as np
from .plasticity import compute_j2_return_mapping_mandel


@dataclass
class BaseMaterial:
    material_id: int
    youngs_modulus: float
    poissons_ratio: float
    yield_strength: float
    tangent_modulus: float

    def lame_parameters(self, E: float = None) -> tuple[float, float]:
        if E is None:
            E = self.youngs_modulus
        nu = self.poissons_ratio
        lam = E * nu / ((1 + nu) * (1 - 2 * nu))
        mu = E / (2 * (1 + nu))
        return lam, mu

    def _D_from_E(self, E: float = None) -> np.ndarray:
        lam, mu = self.lame_parameters(E)
        m_lambda = np.array(
            [[1, 1, 1, 0, 0, 0],
             [1, 1, 1, 0, 0, 0],
             [1, 1, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0]], dtype=float
        )
        m_mu = np.array(
            [[2, 0, 0, 0, 0, 0],
             [0, 2, 0, 0, 0, 0],
             [0, 0, 2, 0, 0, 0],
             [0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 1]], dtype=float
        )
        return lam * m_lambda + mu * m_mu

    @property
    def constitutive_matrix(self) -> np.ndarray:
        """Returns the constant linear elasticity matrix."""
        return self._D_from_E(self.youngs_modulus)


@dataclass
class BilinearJ2Material(BaseMaterial):
    @staticmethod
    def initial_state() -> dict:
        return {
            "plastic_strain_voigt": np.zeros(6, dtype=float),
            "equivalent_plastic_strain": 0.0,
        }

    def isotropic_hardening_modulus_from_tangent(self) -> float:
        youngs_modulus_value = float(self.youngs_modulus)
        tangent_modulus_value = float(self.tangent_modulus)
        if tangent_modulus_value <= 0.0:
            return 0.0
        if tangent_modulus_value >= youngs_modulus_value:
            raise ValueError("tangent_modulus must be smaller than youngs_modulus for bilinear plasticity")
        return (youngs_modulus_value * tangent_modulus_value) / (youngs_modulus_value - tangent_modulus_value)

    def constitutive_response(self, strain_voigt: np.ndarray, state: dict) -> tuple[np.ndarray, np.ndarray, dict]:
        total_strain_voigt = np.asarray(strain_voigt, dtype=float).reshape(6)
        plastic_strain_voigt_old = np.asarray(state["plastic_strain_voigt"], dtype=float).reshape(6)
        equivalent_plastic_strain_old = float(state["equivalent_plastic_strain"])

        elastic_matrix_voigt = np.asarray(self.constitutive_matrix, dtype=float).reshape(6, 6)

        lame_lambda_value, shear_modulus_value = self.lame_parameters(float(self.youngs_modulus))
        isotropic_hardening_modulus_value = float(self.isotropic_hardening_modulus_from_tangent())

        updated_stress_voigt, algorithmic_tangent_voigt, updated_plastic_strain_voigt, updated_equivalent_plastic_strain = compute_j2_return_mapping_mandel(
            total_strain_voigt=total_strain_voigt,
            plastic_strain_voigt_old=plastic_strain_voigt_old,
            equivalent_plastic_strain_old=equivalent_plastic_strain_old,
            elastic_matrix_voigt=elastic_matrix_voigt,
            shear_modulus_value=float(shear_modulus_value),
            yield_strength_value=float(self.yield_strength),
            isotropic_hardening_modulus_value=float(isotropic_hardening_modulus_value),
        )

        new_state = {
            "plastic_strain_voigt": updated_plastic_strain_voigt,
            "equivalent_plastic_strain": float(updated_equivalent_plastic_strain),
        }
        return updated_stress_voigt, algorithmic_tangent_voigt, new_state
