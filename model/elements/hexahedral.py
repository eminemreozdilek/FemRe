import numpy as np
from model.material import BaseMaterial
from model.elements.finite_element import FiniteElement


class HexahedralElement(FiniteElement):
    default_formulation = "standard"
    default_hourglass_alpha = 0.05

    def __init__(
        self,
        nodes,
        material: BaseMaterial,
        formulation: str | None = None,
        hourglass_alpha: float | None = None,
        hourglass_material_modulus: float | None = None,
    ):
        if np.array(nodes, dtype=float).shape != (8, 3):
            raise ValueError("nodes must be an (8,3) array")
        super().__init__(nodes, material)

        self.formulation = formulation if formulation is not None else self.default_formulation
        self.hourglass_alpha = (
            float(hourglass_alpha)
            if hourglass_alpha is not None
            else float(self.default_hourglass_alpha)
        )
        self.hourglass_material_modulus = (
            None if hourglass_material_modulus is None else float(hourglass_material_modulus)
        )

        allowed_formulations = {"standard", "hourglass", "eas_9"}
        if self.formulation not in allowed_formulations:
            raise ValueError(f"Unknown formulation: {self.formulation}")

        self._cached_standard_stiffness = None
        self._cached_eas_data = None
        self._cached_hourglass_stiffness = None

    def _shape_function(self, xi, eta, zeta):
        shape_values = np.zeros(8, dtype=float)

        shape_values[0] = 0.125 * (1 - xi) * (1 - eta) * (1 - zeta)
        shape_values[1] = 0.125 * (1 + xi) * (1 - eta) * (1 - zeta)
        shape_values[2] = 0.125 * (1 + xi) * (1 + eta) * (1 - zeta)
        shape_values[3] = 0.125 * (1 - xi) * (1 + eta) * (1 - zeta)
        shape_values[4] = 0.125 * (1 - xi) * (1 - eta) * (1 + zeta)
        shape_values[5] = 0.125 * (1 + xi) * (1 - eta) * (1 + zeta)
        shape_values[6] = 0.125 * (1 + xi) * (1 + eta) * (1 + zeta)
        shape_values[7] = 0.125 * (1 - xi) * (1 + eta) * (1 + zeta)

        shape_gradients_natural = np.zeros((8, 3), dtype=float)

        shape_gradients_natural[0, 0] = -0.125 * (1 - eta) * (1 - zeta)
        shape_gradients_natural[0, 1] = -0.125 * (1 - xi) * (1 - zeta)
        shape_gradients_natural[0, 2] = -0.125 * (1 - xi) * (1 - eta)

        shape_gradients_natural[1, 0] = 0.125 * (1 - eta) * (1 - zeta)
        shape_gradients_natural[1, 1] = -0.125 * (1 + xi) * (1 - zeta)
        shape_gradients_natural[1, 2] = -0.125 * (1 + xi) * (1 - eta)

        shape_gradients_natural[2, 0] = 0.125 * (1 + eta) * (1 - zeta)
        shape_gradients_natural[2, 1] = 0.125 * (1 + xi) * (1 - zeta)
        shape_gradients_natural[2, 2] = -0.125 * (1 + xi) * (1 + eta)

        shape_gradients_natural[3, 0] = -0.125 * (1 + eta) * (1 - zeta)
        shape_gradients_natural[3, 1] = 0.125 * (1 - xi) * (1 - zeta)
        shape_gradients_natural[3, 2] = -0.125 * (1 - xi) * (1 + eta)

        shape_gradients_natural[4, 0] = -0.125 * (1 - eta) * (1 + zeta)
        shape_gradients_natural[4, 1] = -0.125 * (1 - xi) * (1 + zeta)
        shape_gradients_natural[4, 2] = 0.125 * (1 - xi) * (1 - eta)

        shape_gradients_natural[5, 0] = 0.125 * (1 - eta) * (1 + zeta)
        shape_gradients_natural[5, 1] = -0.125 * (1 + xi) * (1 + zeta)
        shape_gradients_natural[5, 2] = 0.125 * (1 + xi) * (1 - eta)

        shape_gradients_natural[6, 0] = 0.125 * (1 + eta) * (1 + zeta)
        shape_gradients_natural[6, 1] = 0.125 * (1 + xi) * (1 + zeta)
        shape_gradients_natural[6, 2] = 0.125 * (1 + xi) * (1 + eta)

        shape_gradients_natural[7, 0] = -0.125 * (1 + eta) * (1 + zeta)
        shape_gradients_natural[7, 1] = 0.125 * (1 - xi) * (1 + zeta)
        shape_gradients_natural[7, 2] = 0.125 * (1 - xi) * (1 + eta)

        return shape_values, shape_gradients_natural

    def _jacobian(self, shape_gradients_natural):
        jacobian_matrix = np.zeros((3, 3), dtype=float)
        for node_index in range(8):
            jacobian_matrix[0, :] += shape_gradients_natural[node_index, 0] * self.nodes[node_index, :]
            jacobian_matrix[1, :] += shape_gradients_natural[node_index, 1] * self.nodes[node_index, :]
            jacobian_matrix[2, :] += shape_gradients_natural[node_index, 2] * self.nodes[node_index, :]
        return jacobian_matrix

    def _assemble_b_matrix(self, shape_gradients_global):
        b_matrix = np.zeros((6, 24), dtype=float)
        for node_index in range(8):
            column = 3 * node_index
            d_shape_dx = shape_gradients_global[node_index, 0]
            d_shape_dy = shape_gradients_global[node_index, 1]
            d_shape_dz = shape_gradients_global[node_index, 2]

            b_matrix[0, column] = d_shape_dx
            b_matrix[1, column + 1] = d_shape_dy
            b_matrix[2, column + 2] = d_shape_dz

            b_matrix[3, column] = d_shape_dy
            b_matrix[3, column + 1] = d_shape_dx

            b_matrix[4, column + 1] = d_shape_dz
            b_matrix[4, column + 2] = d_shape_dy

            b_matrix[5, column] = d_shape_dz
            b_matrix[5, column + 2] = d_shape_dx

        return b_matrix

    def _assemble_enhanced_b_matrix(self, xi, eta, zeta, inverse_jacobian):
        scalar_mode_gradients_natural = np.array(
            [
                [-2.0 * xi, 0.0, 0.0],
                [0.0, -2.0 * eta, 0.0],
                [0.0, 0.0, -2.0 * zeta],
            ],
            dtype=float,
        )

        scalar_mode_gradients_global = scalar_mode_gradients_natural @ inverse_jacobian.T
        enhanced_b_matrix = np.zeros((6, 9), dtype=float)

        for displacement_component in range(3):
            for scalar_mode_index in range(3):
                column = 3 * displacement_component + scalar_mode_index

                gradient_x = scalar_mode_gradients_global[scalar_mode_index, 0]
                gradient_y = scalar_mode_gradients_global[scalar_mode_index, 1]
                gradient_z = scalar_mode_gradients_global[scalar_mode_index, 2]

                if displacement_component == 0:
                    enhanced_b_matrix[0, column] = gradient_x
                    enhanced_b_matrix[3, column] = gradient_y
                    enhanced_b_matrix[5, column] = gradient_z
                elif displacement_component == 1:
                    enhanced_b_matrix[1, column] = gradient_y
                    enhanced_b_matrix[3, column] = gradient_x
                    enhanced_b_matrix[4, column] = gradient_z
                else:
                    enhanced_b_matrix[2, column] = gradient_z
                    enhanced_b_matrix[4, column] = gradient_y
                    enhanced_b_matrix[5, column] = gradient_x

        return enhanced_b_matrix

    def _full_gauss_points(self):
        gauss_coordinate = 1.0 / np.sqrt(3.0)
        values = [-gauss_coordinate, gauss_coordinate]
        points = []
        for xi in values:
            for eta in values:
                for zeta in values:
                    points.append((xi, eta, zeta, 1.0))
        return points

    def _reduced_gauss_points(self):
        return [(0.0, 0.0, 0.0, 8.0)]

    def _compute_kinematic_matrices(self, xi, eta, zeta, weight):
        _, shape_gradients_natural = self._shape_function(xi, eta, zeta)
        jacobian_matrix = self._jacobian(shape_gradients_natural)
        jacobian_determinant = np.linalg.det(jacobian_matrix)

        if jacobian_determinant <= 0.0:
            raise ValueError("Jacobian determinant is non-positive, check element geometry.")

        inverse_jacobian = np.linalg.inv(jacobian_matrix)
        shape_gradients_global = shape_gradients_natural @ inverse_jacobian.T

        compatible_b_matrix = self._assemble_b_matrix(shape_gradients_global)
        enhanced_b_matrix = self._assemble_enhanced_b_matrix(xi, eta, zeta, inverse_jacobian)
        differential_volume = jacobian_determinant * weight

        return compatible_b_matrix, enhanced_b_matrix, differential_volume

    def _compute_standard_stiffness(self):
        if self._cached_standard_stiffness is not None:
            return self._cached_standard_stiffness

        constitutive_matrix = np.asarray(self.material.constitutive_matrix, dtype=float)
        standard_stiffness = np.zeros((24, 24), dtype=float)

        for xi, eta, zeta, weight in self._full_gauss_points():
            compatible_b_matrix, _, differential_volume = self._compute_kinematic_matrices(xi, eta, zeta, weight)
            standard_stiffness += compatible_b_matrix.T @ constitutive_matrix @ compatible_b_matrix * differential_volume

        standard_stiffness = 0.5 * (standard_stiffness + standard_stiffness.T)
        self._cached_standard_stiffness = standard_stiffness
        return standard_stiffness

    def _compute_eas_data(self):
        if self._cached_eas_data is not None:
            return self._cached_eas_data

        constitutive_matrix = np.asarray(self.material.constitutive_matrix, dtype=float)

        compatible_stiffness = np.zeros((24, 24), dtype=float)
        coupling_stiffness = np.zeros((24, 9), dtype=float)
        internal_stiffness = np.zeros((9, 9), dtype=float)

        for xi, eta, zeta, weight in self._full_gauss_points():
            compatible_b_matrix, enhanced_b_matrix, differential_volume = self._compute_kinematic_matrices(
                xi, eta, zeta, weight
            )

            compatible_stiffness += compatible_b_matrix.T @ constitutive_matrix @ compatible_b_matrix * differential_volume
            coupling_stiffness += compatible_b_matrix.T @ constitutive_matrix @ enhanced_b_matrix * differential_volume
            internal_stiffness += enhanced_b_matrix.T @ constitutive_matrix @ enhanced_b_matrix * differential_volume

        compatible_stiffness = 0.5 * (compatible_stiffness + compatible_stiffness.T)
        internal_stiffness = 0.5 * (internal_stiffness + internal_stiffness.T)

        internal_condition = np.linalg.cond(internal_stiffness)
        if not np.isfinite(internal_condition) or internal_condition > 1.0e12:
            internal_stiffness_inverse = np.linalg.pinv(internal_stiffness)
        else:
            internal_stiffness_inverse = np.linalg.inv(internal_stiffness)

        condensed_stiffness = compatible_stiffness - coupling_stiffness @ internal_stiffness_inverse @ coupling_stiffness.T
        condensed_stiffness = 0.5 * (condensed_stiffness + condensed_stiffness.T)

        self._cached_eas_data = {
            "compatible_stiffness": compatible_stiffness,
            "coupling_stiffness": coupling_stiffness,
            "internal_stiffness": internal_stiffness,
            "internal_stiffness_inverse": internal_stiffness_inverse,
            "condensed_stiffness": condensed_stiffness,
        }
        return self._cached_eas_data

    def _compute_enhanced_parameters(self, displacement_vector):
        if self.formulation != "eas_9":
            return np.zeros(9, dtype=float)

        eas_data = self._compute_eas_data()
        coupling_stiffness = eas_data["coupling_stiffness"]
        internal_stiffness_inverse = eas_data["internal_stiffness_inverse"]

        enhanced_parameters = -internal_stiffness_inverse @ coupling_stiffness.T @ displacement_vector
        return enhanced_parameters

    def _compute_volume(self):
        volume = 0.0
        for xi, eta, zeta, weight in self._full_gauss_points():
            _, _, differential_volume = self._compute_kinematic_matrices(xi, eta, zeta, weight)
            volume += differential_volume
        return volume

    def _compute_characteristic_length(self):
        volume = self._compute_volume()
        return max(volume ** (1.0 / 3.0), 1.0e-12)

    def _build_affine_mode_basis(self):
        centered_nodes = self.nodes - np.mean(self.nodes, axis=0)
        basis_vectors = []

        for displacement_component in range(3):
            mode = np.zeros(24, dtype=float)
            mode[displacement_component::3] = 1.0
            basis_vectors.append(mode)

        for displacement_component in range(3):
            for coordinate_component in range(3):
                mode = np.zeros(24, dtype=float)
                mode[displacement_component::3] = centered_nodes[:, coordinate_component]
                basis_vectors.append(mode)

        basis_matrix = np.column_stack(basis_vectors)
        q_matrix, _ = np.linalg.qr(basis_matrix)
        return q_matrix

    def _compute_hourglass_material_scale(self):
        if self.hourglass_material_modulus is not None:
            if self.hourglass_material_modulus <= 0.0:
                raise ValueError("hourglass_material_modulus must be positive.")
            return self.hourglass_material_modulus

        constitutive_matrix = np.asarray(self.material.constitutive_matrix, dtype=float)
        if constitutive_matrix.shape != (6, 6):
            raise ValueError("constitutive_matrix must have shape (6, 6).")

        constitutive_matrix = 0.5 * (constitutive_matrix + constitutive_matrix.T)

        shear_block = constitutive_matrix[3:6, 3:6]
        shear_block = 0.5 * (shear_block + shear_block.T)

        try:
            shear_eigenvalues = np.linalg.eigvalsh(shear_block)
        except np.linalg.LinAlgError:
            shear_eigenvalues = np.real(np.linalg.eigvals(shear_block))

        positive_shear_eigenvalues = shear_eigenvalues[shear_eigenvalues > 1.0e-12]
        if positive_shear_eigenvalues.size > 0:
            return float(np.mean(positive_shear_eigenvalues))

        try:
            full_eigenvalues = np.linalg.eigvalsh(constitutive_matrix)
        except np.linalg.LinAlgError:
            full_eigenvalues = np.real(np.linalg.eigvals(constitutive_matrix))

        positive_full_eigenvalues = full_eigenvalues[full_eigenvalues > 1.0e-12]
        if positive_full_eigenvalues.size > 0:
            return float(np.min(positive_full_eigenvalues))

        positive_diagonal_terms = np.diag(constitutive_matrix)
        positive_diagonal_terms = positive_diagonal_terms[positive_diagonal_terms > 1.0e-12]
        if positive_diagonal_terms.size > 0:
            return float(np.mean(positive_diagonal_terms))

        raise ValueError(
            "Could not determine a positive hourglass stabilization modulus from constitutive_matrix."
        )

    def _compute_hourglass_stiffness(self):
        if self._cached_hourglass_stiffness is not None:
            return self._cached_hourglass_stiffness

        affine_basis = self._build_affine_mode_basis()
        hourglass_projector = np.eye(24, dtype=float) - affine_basis @ affine_basis.T
        hourglass_projector = 0.5 * (hourglass_projector + hourglass_projector.T)

        volume = self._compute_volume()
        characteristic_length = self._compute_characteristic_length()
        material_scale = self._compute_hourglass_material_scale()

        stiffness_scale = self.hourglass_alpha * material_scale * volume / (characteristic_length ** 2)
        hourglass_stiffness = stiffness_scale * hourglass_projector
        hourglass_stiffness = 0.5 * (hourglass_stiffness + hourglass_stiffness.T)

        self._cached_hourglass_stiffness = hourglass_stiffness
        return hourglass_stiffness

    def _compute_hourglass_formulation_stiffness(self):
        constitutive_matrix = np.asarray(self.material.constitutive_matrix, dtype=float)
        reduced_stiffness = np.zeros((24, 24), dtype=float)

        for xi, eta, zeta, weight in self._reduced_gauss_points():
            compatible_b_matrix, _, differential_volume = self._compute_kinematic_matrices(xi, eta, zeta, weight)
            reduced_stiffness += compatible_b_matrix.T @ constitutive_matrix @ compatible_b_matrix * differential_volume

        reduced_stiffness += self._compute_hourglass_stiffness()
        reduced_stiffness = 0.5 * (reduced_stiffness + reduced_stiffness.T)
        return reduced_stiffness

    def stiffness_matrix(self):
        if self.formulation == "standard":
            return self._compute_standard_stiffness()

        if self.formulation == "hourglass":
            return self._compute_hourglass_formulation_stiffness()

        if self.formulation == "eas_9":
            return self._compute_eas_data()["condensed_stiffness"]

        raise ValueError(f"Unknown formulation: {self.formulation}")

    def B_matrices(self):
        compatible_b_matrices = []

        if self.formulation == "hourglass":
            integration_points = self._reduced_gauss_points()
        else:
            integration_points = self._full_gauss_points()

        for xi, eta, zeta, weight in integration_points:
            compatible_b_matrix, _, _ = self._compute_kinematic_matrices(xi, eta, zeta, weight)
            compatible_b_matrices.append(compatible_b_matrix)

        return compatible_b_matrices

    def integration_weights(self) -> np.ndarray:
        differential_volumes = []

        if self.formulation == "hourglass":
            integration_points = self._reduced_gauss_points()
        else:
            integration_points = self._full_gauss_points()

        for xi, eta, zeta, weight in integration_points:
            _, _, differential_volume = self._compute_kinematic_matrices(xi, eta, zeta, weight)
            differential_volumes.append(differential_volume)

        return np.array(differential_volumes, dtype=float)

    def compute_strain(self, displacements, xi=0.0, eta=0.0, zeta=0.0):
        displacement_vector = np.array(displacements, dtype=float).flatten()
        compatible_b_matrix, enhanced_b_matrix, _ = self._compute_kinematic_matrices(xi, eta, zeta, 1.0)

        if self.formulation == "eas_9":
            enhanced_parameters = self._compute_enhanced_parameters(displacement_vector)
            return compatible_b_matrix @ displacement_vector + enhanced_b_matrix @ enhanced_parameters

        return compatible_b_matrix @ displacement_vector

    def compute_stress(self, displacements, xi=0.0, eta=0.0, zeta=0.0):
        strain = self.compute_strain(displacements, xi, eta, zeta)
        return np.asarray(self.material.constitutive_matrix, dtype=float) @ strain

    def compute_strain_energy(self, displacements):
        displacement_vector = np.array(displacements, dtype=float).flatten()
        element_stiffness = self.stiffness_matrix()
        return 0.5 * displacement_vector.T @ element_stiffness @ displacement_vector

    @staticmethod
    def von_mises_stress(stress):
        sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_zx = stress
        return np.sqrt(
            (
                (sigma_x - sigma_y) ** 2
                + (sigma_y - sigma_z) ** 2
                + (sigma_z - sigma_x) ** 2
                + 6.0 * (tau_xy ** 2 + tau_yz ** 2 + tau_zx ** 2)
            ) / 2.0
        )

    @staticmethod
    def von_mises_strain(strain):
        eps_x, eps_y, eps_z, gamma_xy, gamma_yz, gamma_zx = strain
        return np.sqrt(
            (
                (eps_x - eps_y) ** 2
                + (eps_y - eps_z) ** 2
                + (eps_z - eps_x) ** 2
                + 3.0 * (gamma_xy ** 2 + gamma_yz ** 2 + gamma_zx ** 2)
            ) / 2.0
        )