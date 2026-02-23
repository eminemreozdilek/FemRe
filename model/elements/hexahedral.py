import numpy as np
from model.material import BaseMaterial
from model.elements.finite_element import FiniteElement


class HexahedralElement(FiniteElement):
    def __init__(self, nodes, material: BaseMaterial):
        """
        8-node linear hexahedral element.
        nodes : (8, 3) array of [x,y,z].
        """
        if np.array(nodes, dtype=float).shape != (8, 3):
            raise ValueError("nodes must be an (8,3) array")
        super().__init__(nodes, material)

    # ------------------------------------------------------------
    # Shape functions and kinematics
    # ------------------------------------------------------------
    def __shape_function(self, xi, eta, zeta):
        N = np.zeros(8)
        N[0] = 1 / 8 * (1 - xi) * (1 - eta) * (1 - zeta)
        N[1] = 1 / 8 * (1 + xi) * (1 - eta) * (1 - zeta)
        N[2] = 1 / 8 * (1 + xi) * (1 + eta) * (1 - zeta)
        N[3] = 1 / 8 * (1 - xi) * (1 + eta) * (1 - zeta)
        N[4] = 1 / 8 * (1 - xi) * (1 - eta) * (1 + zeta)
        N[5] = 1 / 8 * (1 + xi) * (1 - eta) * (1 + zeta)
        N[6] = 1 / 8 * (1 + xi) * (1 + eta) * (1 + zeta)
        N[7] = 1 / 8 * (1 - xi) * (1 + eta) * (1 + zeta)

        dN_dxi = np.zeros((8, 3))
        # d/dxi, d/deta, d/dzeta
        dN_dxi[0, 0] = -1 / 8 * (1 - eta) * (1 - zeta)
        dN_dxi[0, 1] = -1 / 8 * (1 - xi) * (1 - zeta)
        dN_dxi[0, 2] = -1 / 8 * (1 - xi) * (1 - eta)

        dN_dxi[1, 0] = 1 / 8 * (1 - eta) * (1 - zeta)
        dN_dxi[1, 1] = -1 / 8 * (1 + xi) * (1 - zeta)
        dN_dxi[1, 2] = -1 / 8 * (1 + xi) * (1 - eta)

        dN_dxi[2, 0] = 1 / 8 * (1 + eta) * (1 - zeta)
        dN_dxi[2, 1] = 1 / 8 * (1 + xi) * (1 - zeta)
        dN_dxi[2, 2] = -1 / 8 * (1 + xi) * (1 + eta)

        dN_dxi[3, 0] = -1 / 8 * (1 + eta) * (1 - zeta)
        dN_dxi[3, 1] = 1 / 8 * (1 - xi) * (1 - zeta)
        dN_dxi[3, 2] = -1 / 8 * (1 - xi) * (1 + eta)

        dN_dxi[4, 0] = -1 / 8 * (1 - eta) * (1 + zeta)
        dN_dxi[4, 1] = -1 / 8 * (1 - xi) * (1 + zeta)
        dN_dxi[4, 2] = 1 / 8 * (1 - xi) * (1 - eta)

        dN_dxi[5, 0] = 1 / 8 * (1 - eta) * (1 + zeta)
        dN_dxi[5, 1] = -1 / 8 * (1 + xi) * (1 + zeta)
        dN_dxi[5, 2] = 1 / 8 * (1 + xi) * (1 - eta)

        dN_dxi[6, 0] = 1 / 8 * (1 + eta) * (1 + zeta)
        dN_dxi[6, 1] = 1 / 8 * (1 + xi) * (1 + zeta)
        dN_dxi[6, 2] = 1 / 8 * (1 + xi) * (1 + eta)

        dN_dxi[7, 0] = -1 / 8 * (1 + eta) * (1 + zeta)
        dN_dxi[7, 1] = 1 / 8 * (1 - xi) * (1 + zeta)
        dN_dxi[7, 2] = 1 / 8 * (1 - xi) * (1 + eta)

        return N, dN_dxi

    def __jacobian(self, dN_dxi):
        J = np.zeros((3, 3))
        for i in range(8):
            J[0, :] += dN_dxi[i, 0] * self.nodes[i, :]
            J[1, :] += dN_dxi[i, 1] * self.nodes[i, :]
            J[2, :] += dN_dxi[i, 2] * self.nodes[i, :]
        return J

    def __assemble_B_matrix(self, dN_global):
        B = np.zeros((6, 24))
        for i in range(8):
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
        """2x2x2 Gauss points and weights in [-1,1]^3."""
        g = [-1.0 / np.sqrt(3.0), 1.0 / np.sqrt(3.0)]
        w = [1.0, 1.0]
        pts = []
        for i, xi in enumerate(g):
            for j, eta in enumerate(g):
                for k, zeta in enumerate(g):
                    pts.append((xi, eta, zeta, w[i] * w[j] * w[k]))
        return pts

    # ------------------------------------------------------------
    # Linear stiffness
    # ------------------------------------------------------------
    def stiffness_matrix(self):
        D = self.material.constitutive_matrix
        ke = np.zeros((24, 24))
        B_list = self.B_matrices()
        dV = self.integration_weights()
        for B, dv in zip(B_list, dV):
            ke += B.T @ D @ B * dv
        return ke

    # ------------------------------------------------------------
    # Nonlinear integration support
    # ------------------------------------------------------------
    def B_matrices(self):
        B_list = []
        for xi, eta, zeta, _w in self._gauss_points():
            _, dN_dxi = self.__shape_function(xi, eta, zeta)
            J = self.__jacobian(dN_dxi)
            detJ = np.linalg.det(J)
            if detJ <= 0:
                raise ValueError("Jacobian determinant is non-positive, check element geometry.")
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
                raise ValueError("Jacobian determinant is non-positive, check element geometry.")
            weights.append(detJ * w)
        return np.array(weights, dtype=float)

    # ------------------------------------------------------------
    # Strain, stress, energy (unchanged interface)
    # ------------------------------------------------------------
    def compute_strain(self, displacements, xi=0.0, eta=0.0, zeta=0.0):
        u = np.array(displacements, dtype=float).flatten()
        _, dN_dxi = self.__shape_function(xi, eta, zeta)
        J = self.__jacobian(dN_dxi)
        detJ = np.linalg.det(J)
        if detJ <= 0:
            raise ValueError("Jacobian determinant is non-positive, check element geometry.")
        invJ = np.linalg.inv(J)
        dN_global = dN_dxi @ invJ.T
        B = self.__assemble_B_matrix(dN_global)
        return B @ u

    def compute_stress(self, displacements, xi=0.0, eta=0.0, zeta=0.0):
        strain = self.compute_strain(displacements, xi, eta, zeta)
        D = self.material.constitutive_matrix
        return D @ strain

    def compute_strain_energy(self, displacements):
        u = np.array(displacements, dtype=float).flatten()
        ke = self.stiffness_matrix()
        return 0.5 * u.T @ ke @ u

    # ------------------------------------------------------------
    # Von Mises
    # ------------------------------------------------------------
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
