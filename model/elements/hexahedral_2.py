import numpy as np
from model.material import BaseMaterial
from model.elements.finite_element import FiniteElement


class SecondOrderHexahedralElement(FiniteElement):
    default_formulation = "standard"

    def __init__(
        self,
        nodes: np.ndarray,
        material: BaseMaterial,
        formulation: str | None = None,
    ):
        if np.array(nodes, dtype=float).shape != (20, 3):
            raise ValueError("For a second-order hexahedral element, nodes must be a (20,3) array.")
        super().__init__(nodes, material)

        self.formulation = formulation if formulation is not None else self.default_formulation
        if self.formulation != "standard":
            raise ValueError(
                "SecondOrderHexahedralElement supports only formulation='standard'."
            )

    # ------------------------------------------------------------
    # Shape functions etc. (same as before)
    # ------------------------------------------------------------
    def __shape_function(self, xi, eta, zeta):
        N = np.zeros(20)
        dN = np.zeros((20, 3))
        corner_coords = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
                         (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
        for i, (xi_i, eta_i, zeta_i) in enumerate(corner_coords):
            N[i] = (1 / 8) * (1 + xi * xi_i) * (1 + eta * eta_i) * (1 + zeta * zeta_i) * \
                   (xi * xi_i + eta * eta_i + zeta * zeta_i - 2)

            dN[i, 0] = (xi_i / 8) * (1 + eta * eta_i) * (1 + zeta * zeta_i) * \
                       (2 * xi * xi_i + eta * eta_i + zeta * zeta_i - 1)
            dN[i, 1] = (eta_i / 8) * (1 + xi * xi_i) * (1 + zeta * zeta_i) * \
                       (xi * xi_i + 2 * eta * eta_i + zeta * zeta_i - 1)
            dN[i, 2] = (zeta_i / 8) * (1 + xi * xi_i) * (1 + eta * eta_i) * \
                       (xi * xi_i + eta * eta_i + 2 * zeta * zeta_i - 1)

        # edge nodes (unchanged from your original code) ...
        # [keeping exact content from your file]  :contentReference[oaicite:4]{index=4}
        # --- Edge nodes ---
        N[8] = 1 / 4 * (1 - xi ** 2) * (1 - eta) * (1 - zeta)
        dN[8, 0] = -0.5 * xi * (1 - eta) * (1 - zeta)
        dN[8, 1] = -0.25 * (1 - xi ** 2) * (1 - zeta)
        dN[8, 2] = -0.25 * (1 - xi ** 2) * (1 - eta)

        N[9] = 1 / 4 * (1 + xi) * (1 - eta ** 2) * (1 - zeta)
        dN[9, 0] = 0.25 * (1 - eta ** 2) * (1 - zeta)
        dN[9, 1] = -0.5 * eta * (1 + xi) * (1 - zeta)
        dN[9, 2] = -0.25 * (1 + xi) * (1 - eta ** 2)

        N[10] = 1 / 4 * (1 - xi ** 2) * (1 + eta) * (1 - zeta)
        dN[10, 0] = -0.5 * xi * (1 + eta) * (1 - zeta)
        dN[10, 1] = 0.25 * (1 - xi ** 2) * (1 - zeta)
        dN[10, 2] = -0.25 * (1 - xi ** 2) * (1 + eta)

        N[11] = 1 / 4 * (1 - xi) * (1 - eta ** 2) * (1 - zeta)
        dN[11, 0] = -0.25 * (1 - eta ** 2) * (1 - zeta)
        dN[11, 1] = -0.5 * eta * (1 - xi) * (1 - zeta)
        dN[11, 2] = -0.25 * (1 - xi) * (1 - eta ** 2)

        N[12] = 1 / 4 * (1 - xi ** 2) * (1 - eta) * (1 + zeta)
        dN[12, 0] = -0.5 * xi * (1 - eta) * (1 + zeta)
        dN[12, 1] = -0.25 * (1 - xi ** 2) * (1 + zeta)
        dN[12, 2] = 0.25 * (1 - xi ** 2) * (1 - eta)

        N[13] = 1 / 4 * (1 + xi) * (1 - eta ** 2) * (1 + zeta)
        dN[13, 0] = 0.25 * (1 - eta ** 2) * (1 + zeta)
        dN[13, 1] = -0.5 * eta * (1 + xi) * (1 + zeta)
        dN[13, 2] = 0.25 * (1 + xi) * (1 - eta ** 2)

        N[14] = 1 / 4 * (1 - xi ** 2) * (1 + eta) * (1 + zeta)
        dN[14, 0] = -0.5 * xi * (1 + eta) * (1 + zeta)
        dN[14, 1] = 0.25 * (1 - xi ** 2) * (1 + zeta)
        dN[14, 2] = 0.25 * (1 - xi ** 2) * (1 + eta)

        N[15] = 1 / 4 * (1 - xi) * (1 - eta ** 2) * (1 + zeta)
        dN[15, 0] = -0.25 * (1 - eta ** 2) * (1 + zeta)
        dN[15, 1] = -0.5 * eta * (1 - xi) * (1 + zeta)
        dN[15, 2] = 0.25 * (1 - xi) * (1 - eta ** 2)

        N[16] = 1 / 4 * (1 - xi) * (1 - eta) * (1 - zeta ** 2)
        dN[16, 0] = -0.25 * (1 - eta) * (1 - zeta ** 2)
        dN[16, 1] = -0.25 * (1 - xi) * (1 - zeta ** 2)
        dN[16, 2] = -0.5 * zeta * (1 - xi) * (1 - eta)

        N[17] = 1 / 4 * (1 + xi) * (1 - eta) * (1 - zeta ** 2)
        dN[17, 0] = 0.25 * (1 - eta) * (1 - zeta ** 2)
        dN[17, 1] = -0.25 * (1 + xi) * (1 - zeta ** 2)
        dN[17, 2] = -0.5 * zeta * (1 + xi) * (1 - eta)

        N[18] = 1 / 4 * (1 + xi) * (1 + eta) * (1 - zeta ** 2)
        dN[18, 0] = 0.25 * (1 + eta) * (1 - zeta ** 2)
        dN[18, 1] = 0.25 * (1 + xi) * (1 - zeta ** 2)
        dN[18, 2] = -0.5 * zeta * (1 + xi) * (1 + eta)

        N[19] = 1 / 4 * (1 - xi) * (1 + eta) * (1 - zeta ** 2)
        dN[19, 0] = -0.25 * (1 + eta) * (1 - zeta ** 2)
        dN[19, 1] = 0.25 * (1 - xi) * (1 - zeta ** 2)
        dN[19, 2] = -0.5 * zeta * (1 - xi) * (1 + eta)

        return N, dN

    def __jacobian(self, dN_dxi):
        J = np.zeros((3, 3))
        for i in range(20):
            J += np.outer(dN_dxi[i, :], self.nodes[i, :])
        return J

    def __assemble_B_matrix(self, dN_global):
        B = np.zeros((6, 60))
        for i in range(20):
            col = 3 * i
            dN_dx = dN_global[i, 0]
            dN_dy = dN_global[i, 1]
            dN_dz = dN_global[i, 2]
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

    def _gauss_points(self):
        gp = np.array([-np.sqrt(3 / 5), 0.0, np.sqrt(3 / 5)])
        gw = np.array([5 / 9, 8 / 9, 5 / 9])
        pts = []
        for i, xi in enumerate(gp):
            for j, eta in enumerate(gp):
                for k, zeta in enumerate(gp):
                    pts.append((xi, eta, zeta, gw[i] * gw[j] * gw[k]))
        return pts

    # ----- linear stiffness -----
    def stiffness_matrix(self):
        D = self.material.constitutive_matrix
        ke = np.zeros((60, 60))
        B_list = self.B_matrices()
        dV = self.integration_weights()
        for B, dv in zip(B_list, dV):
            ke += B.T @ D @ B * dv
        return ke

    # ----- nonlinear integration support -----
    def B_matrices(self):
        B_list = []
        for xi, eta, zeta, _w in self._gauss_points():
            _, dN_dxi = self.__shape_function(xi, eta, zeta)
            J = self.__jacobian(dN_dxi)
            detJ = np.linalg.det(J)
            if detJ <= 0:
                raise ValueError("Jacobian determinant is non-positive.")
            invJ = np.linalg.inv(J)
            dN_global = dN_dxi @ invJ.T
            B_list.append(self.__assemble_B_matrix(dN_global))
        return B_list

    def integration_weights(self) -> np.ndarray:
        weights = []
        for xi, eta, zeta, w in self._gauss_points():
            _, dN_dxi = self.__shape_function(xi, eta, zeta)
            J = self.__jacobian(dN_dxi)
            detJ = np.linalg.det(J)
            if detJ <= 0:
                raise ValueError("Jacobian determinant is non-positive.")
            weights.append(detJ * w)
        return np.array(weights, dtype=float)

    # ----- strain / stress / energy -----
    def compute_strain(self, displacements: np.ndarray, xi: float = 0.0,
                       eta: float = 0.0, zeta: float = 0.0) -> np.ndarray:
        u = np.array(displacements, dtype=float).flatten()
        _, dN_dxi = self.__shape_function(xi, eta, zeta)
        J = self.__jacobian(dN_dxi)
        detJ = np.linalg.det(J)
        if detJ <= 0:
            raise ValueError("Jacobian determinant is non-positive.")
        invJ = np.linalg.inv(J)
        dN_global = dN_dxi @ invJ.T
        B = self.__assemble_B_matrix(dN_global)
        return B @ u

    def compute_stress(self, displacements: np.ndarray, xi: float = 0.0,
                       eta: float = 0.0, zeta: float = 0.0) -> np.ndarray:
        strain = self.compute_strain(displacements, xi, eta, zeta)
        D = self.material.constitutive_matrix
        return D @ strain

    def compute_strain_energy(self, displacements: np.ndarray) -> np.ndarray:
        u = np.array(displacements, dtype=float).flatten()
        ke = self.stiffness_matrix()
        return 0.5 * u.T @ ke @ u

    @staticmethod
    def von_mises_stress(stress: np.ndarray) -> np.ndarray:
        sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_zx = stress
        return np.sqrt(((sigma_x - sigma_y) ** 2 +
                        (sigma_y - sigma_z) ** 2 +
                        (sigma_z - sigma_x) ** 2 +
                        6 * (tau_xy ** 2 + tau_yz ** 2 + tau_zx ** 2)) / 2)

    @staticmethod
    def von_mises_strain(strain: np.ndarray) -> np.ndarray:
        eps_x, eps_y, eps_z, gamma_xy, gamma_yz, gamma_zx = strain
        return np.sqrt(((eps_x - eps_y) ** 2 +
                        (eps_y - eps_z) ** 2 +
                        (eps_z - eps_x) ** 2 +
                        3 * (gamma_xy ** 2 + gamma_yz ** 2 + gamma_zx ** 2)) / 2)
