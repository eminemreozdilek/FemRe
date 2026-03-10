import numpy as np


def compute_deviatoric_projector_mandel() -> np.ndarray:
    deviatoric_projector_matrix = np.eye(6, dtype=float)
    deviatoric_projector_matrix[:3, :3] -= (1.0 / 3.0) * np.ones((3, 3), dtype=float)
    return deviatoric_projector_matrix


def compute_j2_return_mapping_mandel(
    total_strain_voigt: np.ndarray,
    plastic_strain_voigt_old: np.ndarray,
    equivalent_plastic_strain_old: float,
    elastic_matrix_voigt: np.ndarray,
    shear_modulus_value: float,
    yield_strength_value: float,
    isotropic_hardening_modulus_value: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    total_strain_voigt = np.asarray(total_strain_voigt, dtype=float).reshape(6)
    plastic_strain_voigt_old = np.asarray(plastic_strain_voigt_old, dtype=float).reshape(6)
    elastic_matrix_voigt = np.asarray(elastic_matrix_voigt, dtype=float).reshape(6, 6)

    voigt_strain_to_mandel_transform = np.diag(
        [1.0, 1.0, 1.0, 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)]
    )
    mandel_strain_to_voigt_transform = np.diag(
        [1.0, 1.0, 1.0, np.sqrt(2.0), np.sqrt(2.0), np.sqrt(2.0)]
    )

    voigt_stress_to_mandel_transform = np.diag(
        [1.0, 1.0, 1.0, np.sqrt(2.0), np.sqrt(2.0), np.sqrt(2.0)]
    )
    mandel_stress_to_voigt_transform = np.diag(
        [1.0, 1.0, 1.0, 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)]
    )

    total_strain_mandel = voigt_strain_to_mandel_transform @ total_strain_voigt
    plastic_strain_mandel_old = voigt_strain_to_mandel_transform @ plastic_strain_voigt_old
    elastic_matrix_mandel = voigt_stress_to_mandel_transform @ elastic_matrix_voigt @ mandel_strain_to_voigt_transform

    elastic_strain_trial_mandel = total_strain_mandel - plastic_strain_mandel_old
    trial_stress_mandel = elastic_matrix_mandel @ elastic_strain_trial_mandel

    deviatoric_projector_matrix = compute_deviatoric_projector_mandel()
    trial_deviatoric_stress_mandel = deviatoric_projector_matrix @ trial_stress_mandel
    trial_deviatoric_stress_norm_value = float(np.linalg.norm(trial_deviatoric_stress_mandel))

    if trial_deviatoric_stress_norm_value < 1e-16:
        trial_von_mises_value = 0.0
    else:
        trial_von_mises_value = np.sqrt(3.0 / 2.0) * trial_deviatoric_stress_norm_value

    current_yield_strength_value = float(yield_strength_value + isotropic_hardening_modulus_value * equivalent_plastic_strain_old)
    yield_function_value = trial_von_mises_value - current_yield_strength_value

    if yield_function_value <= 0.0:
        updated_stress_mandel = trial_stress_mandel
        algorithmic_tangent_mandel = elastic_matrix_mandel
        updated_plastic_strain_mandel = plastic_strain_mandel_old
        updated_equivalent_plastic_strain = float(equivalent_plastic_strain_old)
    else:
        plastic_multiplier_increment_value = float(yield_function_value / (3.0 * shear_modulus_value + isotropic_hardening_modulus_value))

        flow_direction_deviatoric_mandel = trial_deviatoric_stress_mandel / trial_deviatoric_stress_norm_value
        flow_direction_mandel = np.sqrt(3.0 / 2.0) * flow_direction_deviatoric_mandel

        updated_stress_mandel = trial_stress_mandel - 2.0 * shear_modulus_value * plastic_multiplier_increment_value * flow_direction_mandel
        updated_plastic_strain_mandel = plastic_strain_mandel_old + plastic_multiplier_increment_value * flow_direction_mandel
        updated_equivalent_plastic_strain = float(equivalent_plastic_strain_old + plastic_multiplier_increment_value)

        algorithmic_direction_vector = elastic_matrix_mandel @ flow_direction_mandel
        denominator_value = float(flow_direction_mandel @ algorithmic_direction_vector + isotropic_hardening_modulus_value)
        algorithmic_tangent_mandel = elastic_matrix_mandel - np.outer(algorithmic_direction_vector, algorithmic_direction_vector) / denominator_value

    updated_stress_voigt = mandel_stress_to_voigt_transform @ updated_stress_mandel
    algorithmic_tangent_voigt = mandel_stress_to_voigt_transform @ algorithmic_tangent_mandel @ voigt_strain_to_mandel_transform
    updated_plastic_strain_voigt = mandel_strain_to_voigt_transform @ updated_plastic_strain_mandel

    return updated_stress_voigt, algorithmic_tangent_voigt, updated_plastic_strain_voigt, updated_equivalent_plastic_strain
