from dataclasses import dataclass
import numpy as np


@dataclass
class BaseMaterial:
    material_id: int
    youngs_modulus: float
    poissons_ratio: float
    __constitutive_matrix: np.ndarray | None = None

    def lame_parameters(self) -> tuple[float, float]:
        nu = self.poissons_ratio
        lam = self.youngs_modulus * nu / ((1 + nu) * (1 - 2 * nu))
        mu = self.youngs_modulus / (2 * (1 + nu))
        return lam, mu

    def __calculate_isotropic_stiffness_matrix(self) -> np.ndarray:
        nu = self.poissons_ratio
        factor = self.youngs_modulus / ((1 + nu) * (1 - 2 * nu))
        return factor * np.array([
            [1 - nu, nu, nu, 0, 0, 0],
            [nu, 1 - nu, nu, 0, 0, 0],
            [nu, nu, 1 - nu, 0, 0, 0],
            [0, 0, 0, (1 - 2 * nu) / 2, 0, 0],
            [0, 0, 0, 0, (1 - 2 * nu) / 2, 0],
            [0, 0, 0, 0, 0, (1 - 2 * nu) / 2],
        ], dtype=float)

    @property
    def constitutive_matrix(self) -> np.ndarray:
        if self.__constitutive_matrix is None:
            self.__constitutive_matrix = self.__calculate_isotropic_stiffness_matrix()
        return self.__constitutive_matrix

    @constitutive_matrix.setter
    def constitutive_matrix(self, matrix: np.ndarray) -> None:
        self.__constitutive_matrix = matrix
