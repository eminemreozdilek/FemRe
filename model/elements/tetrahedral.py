import numpy as np
from model.material import BaseMaterial
from model.elements.finite_element import FiniteElement


class TetrahedralElement(FiniteElement):
    default_formulation = "standard"

    def __init__(
        self,
        nodes: np.ndarray,
        material: BaseMaterial,
        formulation: str | None = None,
    ):
        if np.array(nodes, dtype=float).shape != (4, 3):
            raise ValueError("nodes must be a (4,3) array")
        super().__init__(nodes, material)

        self.formulation = formulation if formulation is not None else self.default_formulation
        if self.formulation != "standard":
            raise ValueError(
                "TetrahedralElement supports only formulation='standard'."
            )

    def __compute_volume(self):
        M = np.ones((4, 4))
        M[:, 1:] = self.nodes
        det_M = np.linalg.det(M)
        volume = abs(det_M) / 6.0
        return volume, det_M

    def __compute_shape_function_derivatives(self):
        volume, det_M = self.__compute_volume()
        if np.isclose(det_M, 0.0):
            raise ValueError("Degenerate tetrahedron (zero volume).")
        dN = np.zeros((4, 3))
        for i in range(4):
            indices = [j for j in range(4) if j != i]
            coords = self.nodes[indices]
            x = coords[:, 0]
            y = coords[:, 1]
            z = coords[:, 2]

            mat_b = np.array([[1, y[0], z[0]],
                              [1, y[1], z[1]],
                              [1, y[2], z[2]]])
            mat_c = np.array([[1, x[0], z[0]],
                              [1, x[1], z[1]],
                              [1, x[2], z[2]]])
            mat_d = np.array([[1, x[0], y[0]],
                              [1, x[1], y[1]],
                              [1, x[2], y[2]]])

            b_i = np.linalg.det(mat_b)
            c_i = np.linalg.det(mat_c)
            d_i = np.linalg.det(mat_d)

            dN[i, 0] = ((-1) ** (i + 1)) * b_i / det_M
            dN[i, 1] = ((-1) ** (i + 2)) * c_i / det_M
            dN[i, 2] = ((-1) ** (i + 3)) * d_i / det_M

        return dN

    def __assemble_B_matrix(self, dN):
        B = np.zeros((6, 12))
        for i in range(4):
            col = 3 * i
            dN_dx = dN[i, 0]
            dN_dy = dN[i, 1]
            dN_dz = dN[i, 2]
            B[0, col] = dN_dx
            B[1, col + 1] = dN_dy
            B[2, col + 2] = dN_dz
            B[3, col] = dN_dy
            B[3, col + 1] = dN_dx
            B[4, col + 1] = dN_dz
            B[4, col + 2] = dN_dy
            B[5, col] = dN_dz
            B[5, col + 2] = dN_dx
        return B

    # ----- linear stiffness -----
    def stiffness_matrix(self):
        dN = self.__compute_shape_function_derivatives()
        B = self.__assemble_B_matrix(dN)
        D = self.material.constitutive_matrix
        volume, _ = self.__compute_volume()
        return volume * (B.T @ D @ B)

    # ----- nonlinear integration support -----
    def B_matrices(self):
        dN = self.__compute_shape_function_derivatives()
        B = self.__assemble_B_matrix(dN)
        return [B]

    def integration_weights(self) -> np.ndarray:
        volume, _ = self.__compute_volume()
        return np.array([volume], dtype=float)

    # ----- strain / stress / energy -----
    def compute_strain(self, displacements, **kwargs):
        u = np.array(displacements, dtype=float).flatten()
        dN = self.__compute_shape_function_derivatives()
        B = self.__assemble_B_matrix(dN)
        return B @ u

    def compute_stress(self, displacements, **kwargs):
        strain = self.compute_strain(displacements)
        D = self.material.constitutive_matrix
        return D @ strain

    def compute_strain_energy(self, displacements):
        strain = self.compute_strain(displacements)
        stress = self.compute_stress(displacements)
        energy_density = 0.5 * np.dot(strain, stress)
        volume, _ = self.__compute_volume()
        return energy_density * volume

    @staticmethod
    def von_mises_stress(stress):
        sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_zx = stress
        return np.sqrt(((sigma_x - sigma_y) ** 2 +
                        (sigma_y - sigma_z) ** 2 +
                        (sigma_z - sigma_x) ** 2 +
                        6 * (tau_xy ** 2 + tau_yz ** 2 + tau_zx ** 2)) / 2)

    @staticmethod
    def von_mises_strain(strain):
        eps_x, eps_y, eps_z, gamma_xy, gamma_yz, gamma_zx = strain
        return np.sqrt(((eps_x - eps_y) ** 2 +
                        (eps_y - eps_z) ** 2 +
                        (eps_z - eps_x) ** 2 +
                        3 * (gamma_xy ** 2 + gamma_yz ** 2 + gamma_zx ** 2)) / 2)
