import numpy as np
from model.material import BaseMaterial
from model.elements.finite_element import FiniteElement


class SecondOrderTetrahedralElement(FiniteElement):
    def __init__(self, nodes: np.ndarray, material: BaseMaterial):
        if np.array(nodes, dtype=float).shape != (10, 3):
            raise ValueError("For a second-order tetrahedron, nodes must be a (10,3) array.")
        super().__init__(nodes, material)

    def __shape_function(self, r, s, t):
        L1 = 1 - r - s - t
        L2 = r
        L3 = s
        L4 = t

        N = np.zeros(10)
        N[0] = L1 * (2 * L1 - 1)
        N[1] = L2 * (2 * L2 - 1)
        N[2] = L3 * (2 * L3 - 1)
        N[3] = L4 * (2 * L4 - 1)
        N[4] = 4 * L1 * L2
        N[5] = 4 * L2 * L3
        N[6] = 4 * L3 * L1
        N[7] = 4 * L1 * L4
        N[8] = 4 * L2 * L4
        N[9] = 4 * L3 * L4

        dL1 = np.array([-1, -1, -1])
        dL2 = np.array([1, 0, 0])
        dL3 = np.array([0, 1, 0])
        dL4 = np.array([0, 0, 1])

        dN = np.zeros((10, 3))
        dN[0, :] = (4 * L1 - 1) * dL1
        dN[1, :] = (4 * L2 - 1) * dL2
        dN[2, :] = (4 * L3 - 1) * dL3
        dN[3, :] = (4 * L4 - 1) * dL4
        dN[4, :] = 4 * (L2 * dL1 + L1 * dL2)
        dN[5, :] = 4 * (L3 * dL2 + L2 * dL3)
        dN[6, :] = 4 * (L1 * dL3 + L3 * dL1)
        dN[7, :] = 4 * (L4 * dL1 + L1 * dL4)
        dN[8, :] = 4 * (L4 * dL2 + L2 * dL4)
        dN[9, :] = 4 * (L4 * dL3 + L3 * dL4)

        return N, dN

    def __jacobian(self, dN_dxi):
        J = np.zeros((3, 3))
        for i in range(10):
            J += np.outer(dN_dxi[i, :], self.nodes[i, :])
        return J

    def __assemble_B_matrix(self, dN_global):
        B = np.zeros((6, 30))
        for i in range(10):
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

    # ----- linear stiffness -----
    def stiffness_matrix(self):
        r = s = t = 1 / 4
        _, dN = self.__shape_function(r, s, t)
        J = self.__jacobian(dN)
        detJ = np.linalg.det(J)
        if detJ <= 0:
            raise ValueError("Jacobian determinant is non-positive.")
        invJ = np.linalg.inv(J)
        dN_global = dN @ invJ.T
        B = self.__assemble_B_matrix(dN_global)
        D = self.material.constitutive_matrix
        return detJ * (B.T @ D @ B)

    # ----- nonlinear integration support -----
    def B_matrices(self):
        r = s = t = 1 / 4
        _, dN = self.__shape_function(r, s, t)
        J = self.__jacobian(dN)
        detJ = np.linalg.det(J)
        if detJ <= 0:
            raise ValueError("Jacobian determinant is non-positive.")
        invJ = np.linalg.inv(J)
        dN_global = dN @ invJ.T
        B = self.__assemble_B_matrix(dN_global)
        return [B]

    def integration_weights(self) -> np.ndarray:
        r = s = t = 1 / 4
        _, dN = self.__shape_function(r, s, t)
        J = self.__jacobian(dN)
        detJ = np.linalg.det(J)
        if detJ <= 0:
            raise ValueError("Jacobian determinant is non-positive.")
        return np.array([detJ], dtype=float)

    # ----- strain / stress / energy -----
    def compute_strain(self, displacements, **kwargs):
        u = np.array(displacements, dtype=float).flatten()
        r = kwargs.get("r", 1 / 4)
        s = kwargs.get("s", 1 / 4)
        t = kwargs.get("t", 1 / 4)
        _, dN = self.__shape_function(r, s, t)
        J = self.__jacobian(dN)
        detJ = np.linalg.det(J)
        if detJ <= 0:
            raise ValueError("Jacobian determinant is non-positive.")
        invJ = np.linalg.inv(J)
        dN_global = dN @ invJ.T
        B = self.__assemble_B_matrix(dN_global)
        return B @ u

    def compute_stress(self, displacements, **kwargs):
        strain = self.compute_strain(displacements, **kwargs)
        D = self.material.constitutive_matrix
        return D @ strain

    def compute_strain_energy(self, displacements):
        strain = self.compute_strain(displacements)
        stress = self.compute_stress(displacements)
        energy_density = 0.5 * np.dot(strain, stress)
        J = self.__jacobian(self.__shape_function(1 / 4, 1 / 4, 1 / 4)[1])
        detJ = np.linalg.det(J)
        return energy_density * detJ

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
