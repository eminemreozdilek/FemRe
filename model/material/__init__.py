from dataclasses import dataclass
import numpy as np


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
