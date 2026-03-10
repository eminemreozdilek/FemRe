import numpy as np
import scipy.sparse as sparse
import pypardiso as pypardiso_solver


def collect_prescribed_displacements_from_model(model) -> np.ndarray:
    total_number_of_degrees_of_freedom = int(model.total_number_of_dofs())
    prescribed_displacement_vector = np.full(total_number_of_degrees_of_freedom, np.nan, dtype=float)
    for node_id_value, node_data_instance in model.nodes_by_id.items():
        base_dof_index = 3 * (int(node_id_value) - 1)
        prescribed_values = np.asarray(node_data_instance.prescribed_displacement, dtype=float).reshape(3)
        if not np.isnan(prescribed_values[0]):
            prescribed_displacement_vector[base_dof_index + 0] = float(prescribed_values[0])
        if not np.isnan(prescribed_values[1]):
            prescribed_displacement_vector[base_dof_index + 1] = float(prescribed_values[1])
        if not np.isnan(prescribed_values[2]):
            prescribed_displacement_vector[base_dof_index + 2] = float(prescribed_values[2])
    return prescribed_displacement_vector


def map_prescribed_displacements_with_contacts(
    full_prescribed_displacement_vector: np.ndarray,
    full_to_reduced_dof_mapping: np.ndarray,
    reduced_number_of_degrees_of_freedom: int,
    conflict_tolerance: float = 1e-12,
) -> np.ndarray:
    full_prescribed_displacement_vector = np.asarray(full_prescribed_displacement_vector, dtype=float)
    full_to_reduced_dof_mapping = np.asarray(full_to_reduced_dof_mapping, dtype=np.int64)

    reduced_prescribed_displacement_vector = np.full(int(reduced_number_of_degrees_of_freedom), np.nan, dtype=float)

    full_fixed_index_array = np.where(~np.isnan(full_prescribed_displacement_vector))[0]
    if full_fixed_index_array.size == 0:
        return reduced_prescribed_displacement_vector

    reduced_index_array = full_to_reduced_dof_mapping[full_fixed_index_array].astype(np.int64, copy=False)
    prescribed_value_array = full_prescribed_displacement_vector[full_fixed_index_array].astype(float, copy=False)

    ordering_index_array = np.argsort(reduced_index_array)
    reduced_index_array = reduced_index_array[ordering_index_array]
    prescribed_value_array = prescribed_value_array[ordering_index_array]

    boundary_index_array = np.r_[0, np.where(reduced_index_array[1:] != reduced_index_array[:-1])[0] + 1]
    minimum_value_array = np.minimum.reduceat(prescribed_value_array, boundary_index_array)
    maximum_value_array = np.maximum.reduceat(prescribed_value_array, boundary_index_array)

    conflict_group_index_array = np.where(np.abs(maximum_value_array - minimum_value_array) > conflict_tolerance)[0]
    if conflict_group_index_array.size:
        conflict_group_index_value = int(conflict_group_index_array[0])
        conflicting_reduced_dof_index = int(reduced_index_array[boundary_index_array[conflict_group_index_value]])
        raise ValueError(f"Contact-coupled DOF conflict on reduced index {conflicting_reduced_dof_index}")

    reduced_prescribed_displacement_vector[reduced_index_array[boundary_index_array]] = prescribed_value_array[boundary_index_array]
    return reduced_prescribed_displacement_vector


def __element_degree_of_freedom_indices_from_node_ids(node_id_array: np.ndarray) -> np.ndarray:
    node_id_array = np.asarray(node_id_array, dtype=np.int64).reshape(-1)
    base_index_array = 3 * (node_id_array - 1)
    offset_array = np.array([0, 1, 2], dtype=np.int64)
    return (base_index_array[:, None] + offset_array[None, :]).ravel()


def __assemble_global_tangent_stiffness_and_internal_force(
    model,
    full_displacement_vector: np.ndarray,
    old_state_by_element_id: dict[int, list],
) -> tuple[sparse.csr_matrix, np.ndarray, dict[int, list]]:
    full_displacement_vector = np.asarray(full_displacement_vector, dtype=float).reshape(-1)
    total_number_of_degrees_of_freedom = int(model.total_number_of_dofs())

    global_internal_force_vector = np.zeros(total_number_of_degrees_of_freedom, dtype=float)

    global_row_index_chunks = []
    global_column_index_chunks = []
    global_value_chunks = []

    new_state_by_element_id: dict[int, list] = {}

    dof_offset_array = np.arange(3, dtype=np.int64)

    for element_id_value, element_data_instance in model.elements_by_id.items():
        element_node_id_array = np.asarray(element_data_instance.node_ids, dtype=np.int64).reshape(-1)
        element_degree_of_freedom_index_array = (3 * (element_node_id_array - 1)[:, None] + dof_offset_array[None, :]).ravel()
        element_displacement_vector = full_displacement_vector[element_degree_of_freedom_index_array]

        finite_element_instance = element_data_instance.finite_element
        element_old_state_list = old_state_by_element_id.get(int(element_id_value), None)

        element_tangent_stiffness_matrix, element_internal_force_vector, element_new_state_list = finite_element_instance.tangent_stiffness_and_internal_force(
            element_displacement_vector,
            element_old_state_list,
        )

        new_state_by_element_id[int(element_id_value)] = element_new_state_list

        global_internal_force_vector[element_degree_of_freedom_index_array] += np.asarray(element_internal_force_vector, dtype=float).reshape(-1)

        number_of_local_dofs = int(element_degree_of_freedom_index_array.size)
        global_row_index_chunks.append(np.repeat(element_degree_of_freedom_index_array, number_of_local_dofs))
        global_column_index_chunks.append(np.tile(element_degree_of_freedom_index_array, number_of_local_dofs))
        global_value_chunks.append(np.asarray(element_tangent_stiffness_matrix, dtype=float).reshape(-1))

    if not global_row_index_chunks:
        empty_stiffness_matrix = sparse.csr_matrix((total_number_of_degrees_of_freedom, total_number_of_degrees_of_freedom), dtype=float)
        return empty_stiffness_matrix, global_internal_force_vector, new_state_by_element_id

    global_row_index_array = np.concatenate(global_row_index_chunks).astype(np.int64, copy=False)
    global_column_index_array = np.concatenate(global_column_index_chunks).astype(np.int64, copy=False)
    global_value_array = np.concatenate(global_value_chunks).astype(float, copy=False)

    global_tangent_stiffness_matrix = sparse.coo_matrix(
        (global_value_array, (global_row_index_array, global_column_index_array)),
        shape=(total_number_of_degrees_of_freedom, total_number_of_degrees_of_freedom),
    ).tocsr()
    global_tangent_stiffness_matrix.sum_duplicates()

    return global_tangent_stiffness_matrix, global_internal_force_vector, new_state_by_element_id


def solve_one_displacement_step_newton(
    model,
    target_full_prescribed_displacement_vector: np.ndarray,
    initial_full_displacement_vector: np.ndarray,
    old_state_by_element_id: dict[int, list],
    newton_residual_tolerance: float,
    newton_increment_tolerance: float,
    maximum_newton_iterations: int,
) -> tuple[bool, np.ndarray, dict[int, list], np.ndarray, int]:
    external_force_vector_full = np.asarray(model.build_global_force_vector(), dtype=float).reshape(-1)

    contact_exists = bool(getattr(model, "contact_constraint_sets", None))
    if not contact_exists:
        full_displacement_vector = np.asarray(initial_full_displacement_vector, dtype=float).copy()
        prescribed_full = np.asarray(target_full_prescribed_displacement_vector, dtype=float).copy()

        fixed_full_index_array = np.where(~np.isnan(prescribed_full))[0]
        free_full_index_array = np.where(np.isnan(prescribed_full))[0]
        if fixed_full_index_array.size:
            full_displacement_vector[fixed_full_index_array] = prescribed_full[fixed_full_index_array]

        residual_reference_norm_value = None

        for iteration_index in range(1, int(maximum_newton_iterations) + 1):
            global_tangent_stiffness_matrix, global_internal_force_vector, trial_state_by_element_id = __assemble_global_tangent_stiffness_and_internal_force(
                model=model,
                full_displacement_vector=full_displacement_vector,
                old_state_by_element_id=old_state_by_element_id,
            )

            full_residual_vector = external_force_vector_full - global_internal_force_vector
            free_residual_vector = full_residual_vector[free_full_index_array]
            free_residual_norm_value = float(np.linalg.norm(free_residual_vector))

            if residual_reference_norm_value is None:
                residual_reference_norm_value = max(free_residual_norm_value, 1.0)

            if (free_residual_norm_value / residual_reference_norm_value) < float(newton_residual_tolerance) or free_residual_norm_value < 1e-8:
                reaction_vector_full = global_internal_force_vector - external_force_vector_full
                return True, full_displacement_vector, trial_state_by_element_id, reaction_vector_full, int(iteration_index)

            free_free_tangent_stiffness_matrix = global_tangent_stiffness_matrix[free_full_index_array, :][:, free_full_index_array]
            displacement_increment_free = pypardiso_solver.spsolve(free_free_tangent_stiffness_matrix, free_residual_vector)
            displacement_increment_norm_value = float(np.linalg.norm(displacement_increment_free))

            damping_factor_value = 1.0
            if displacement_increment_norm_value > 1.0:
                damping_factor_value = min(1.0, 1.0 / displacement_increment_norm_value)

            full_displacement_vector[free_full_index_array] += damping_factor_value * displacement_increment_free

            if displacement_increment_norm_value < float(newton_increment_tolerance):
                reaction_vector_full = global_internal_force_vector - external_force_vector_full
                return True, full_displacement_vector, trial_state_by_element_id, reaction_vector_full, int(iteration_index)

        return False, np.asarray(initial_full_displacement_vector, dtype=float), old_state_by_element_id, np.zeros_like(external_force_vector_full), int(maximum_newton_iterations)

    full_to_reduced_dof_mapping = np.asarray(model.build_dof_mapping_with_contacts(), dtype=np.int64).reshape(-1)
    full_number_of_degrees_of_freedom = int(full_to_reduced_dof_mapping.size)
    reduced_number_of_degrees_of_freedom = int(full_to_reduced_dof_mapping.max()) + 1

    projection_matrix = sparse.csr_matrix(
        (np.ones(full_number_of_degrees_of_freedom, dtype=float), (np.arange(full_number_of_degrees_of_freedom, dtype=np.int64), full_to_reduced_dof_mapping)),
        shape=(full_number_of_degrees_of_freedom, reduced_number_of_degrees_of_freedom),
    )

    external_force_vector_reduced = np.bincount(
        full_to_reduced_dof_mapping,
        weights=np.asarray(external_force_vector_full, dtype=float),
        minlength=reduced_number_of_degrees_of_freedom,
    ).astype(float)

    prescribed_reduced = map_prescribed_displacements_with_contacts(
        full_prescribed_displacement_vector=target_full_prescribed_displacement_vector,
        full_to_reduced_dof_mapping=full_to_reduced_dof_mapping,
        reduced_number_of_degrees_of_freedom=reduced_number_of_degrees_of_freedom,
    )

    reduced_displacement_vector = np.zeros(reduced_number_of_degrees_of_freedom, dtype=float)
    fixed_reduced_index_array = np.where(~np.isnan(prescribed_reduced))[0]
    free_reduced_index_array = np.where(np.isnan(prescribed_reduced))[0]
    if fixed_reduced_index_array.size:
        reduced_displacement_vector[fixed_reduced_index_array] = prescribed_reduced[fixed_reduced_index_array]

    residual_reference_norm_value = None

    for iteration_index in range(1, int(maximum_newton_iterations) + 1):
        full_displacement_vector = reduced_displacement_vector[full_to_reduced_dof_mapping]

        global_tangent_stiffness_matrix_full, global_internal_force_vector_full, trial_state_by_element_id = __assemble_global_tangent_stiffness_and_internal_force(
            model=model,
            full_displacement_vector=full_displacement_vector,
            old_state_by_element_id=old_state_by_element_id,
        )

        internal_force_vector_reduced = np.bincount(
            full_to_reduced_dof_mapping,
            weights=np.asarray(global_internal_force_vector_full, dtype=float),
            minlength=reduced_number_of_degrees_of_freedom,
        ).astype(float)

        reduced_residual_vector = external_force_vector_reduced - internal_force_vector_reduced
        free_residual_vector = reduced_residual_vector[free_reduced_index_array]
        free_residual_norm_value = float(np.linalg.norm(free_residual_vector))

        if residual_reference_norm_value is None:
            residual_reference_norm_value = max(free_residual_norm_value, 1.0)

        if (free_residual_norm_value / residual_reference_norm_value) < float(newton_residual_tolerance) or free_residual_norm_value < 1e-8:
            reaction_vector_full = global_internal_force_vector_full - external_force_vector_full
            return True, full_displacement_vector, trial_state_by_element_id, reaction_vector_full, int(iteration_index)

        temporary_matrix_full = global_tangent_stiffness_matrix_full @ projection_matrix
        reduced_tangent_stiffness_matrix = (projection_matrix.T @ temporary_matrix_full).tocsr()
        reduced_tangent_stiffness_matrix.sum_duplicates()

        reduced_free_free_tangent_matrix = reduced_tangent_stiffness_matrix[free_reduced_index_array, :][:, free_reduced_index_array]
        displacement_increment_free = pypardiso_solver.spsolve(reduced_free_free_tangent_matrix, free_residual_vector)
        displacement_increment_norm_value = float(np.linalg.norm(displacement_increment_free))

        damping_factor_value = 1.0
        if displacement_increment_norm_value > 1.0:
            damping_factor_value = min(1.0, 1.0 / displacement_increment_norm_value)

        reduced_displacement_vector[free_reduced_index_array] += damping_factor_value * displacement_increment_free

        if displacement_increment_norm_value < float(newton_increment_tolerance):
            reaction_vector_full = global_internal_force_vector_full - external_force_vector_full
            return True, full_displacement_vector, trial_state_by_element_id, reaction_vector_full, int(iteration_index)

    return False, np.asarray(initial_full_displacement_vector, dtype=float), old_state_by_element_id, np.zeros(full_number_of_degrees_of_freedom, dtype=float), int(maximum_newton_iterations)


def solve_model_nonlinear_displacement_control(
        model: object,
        driven_node_id_array: np.ndarray,
        driven_component_index: int,
        target_total_displacement: float,
        number_of_initial_steps: int = 21,
        maximum_subdivisions: int = 5,
        newton_residual_tolerance: float = 1e-6,
        newton_increment_tolerance: float = 1e-8,
        maximum_newton_iterations: int = 40,
) -> dict:
    driven_node_id_array = np.asarray(driven_node_id_array, dtype=int).reshape(-1)
    driven_component_index = int(driven_component_index)

    total_number_of_degrees_of_freedom = int(model.total_number_of_dofs())
    current_full_displacement_vector = np.zeros(total_number_of_degrees_of_freedom, dtype=float)

    old_state_by_element_id: dict[int, list] = {}
    for element_id_value, element_data_instance in model.elements_by_id.items():
        finite_element_instance = element_data_instance.finite_element
        old_state_by_element_id[int(element_id_value)] = [finite_element_instance.material.initial_state() for _ in range(int(finite_element_instance.num_integration_points()))]

    accepted_target_displacement_history = []
    reaction_history = []
    newton_iteration_history = []

    step_target_displacement_array = np.linspace(float(target_total_displacement) / float(number_of_initial_steps), float(target_total_displacement), int(number_of_initial_steps))
    current_target_value = 0.0

    for target_displacement_value in step_target_displacement_array:
        full_prescribed_displacement_vector = collect_prescribed_displacements_from_model(model)
        driven_degree_of_freedom_index_array = 3 * (driven_node_id_array - 1) + int(driven_component_index)
        full_prescribed_displacement_vector[driven_degree_of_freedom_index_array] = float(target_displacement_value)

        is_converged, updated_full_displacement_vector, trial_state_by_element_id, reaction_vector_full, number_of_iterations = solve_one_displacement_step_newton(
            model=model,
            target_full_prescribed_displacement_vector=full_prescribed_displacement_vector,
            initial_full_displacement_vector=current_full_displacement_vector,
            old_state_by_element_id=old_state_by_element_id,
            newton_residual_tolerance=float(newton_residual_tolerance),
            newton_increment_tolerance=float(newton_increment_tolerance),
            maximum_newton_iterations=int(maximum_newton_iterations),
        )

        if is_converged:
            current_full_displacement_vector = updated_full_displacement_vector
            old_state_by_element_id = trial_state_by_element_id
            current_target_value = float(target_displacement_value)

            accepted_target_displacement_history.append(current_target_value)
            reaction_history.append(reaction_vector_full.copy())
            newton_iteration_history.append(int(number_of_iterations))
            continue

        interval_start_value = float(current_target_value)
        interval_end_value = float(target_displacement_value)
        success_flag = False

        for _subdivision_level in range(1, int(maximum_subdivisions) + 1):
            midpoint_value = 0.5 * (interval_start_value + interval_end_value)

            full_prescribed_displacement_vector = collect_prescribed_displacements_from_model(model)
            driven_degree_of_freedom_index_array = 3 * (driven_node_id_array - 1) + int(driven_component_index)
            full_prescribed_displacement_vector[driven_degree_of_freedom_index_array] = float(midpoint_value)

            ok_mid, u_mid, state_mid, reaction_mid, iterations_mid = solve_one_displacement_step_newton(
                model=model,
                target_full_prescribed_displacement_vector=full_prescribed_displacement_vector,
                initial_full_displacement_vector=current_full_displacement_vector,
                old_state_by_element_id=old_state_by_element_id,
                newton_residual_tolerance=float(newton_residual_tolerance),
                newton_increment_tolerance=float(newton_increment_tolerance),
                maximum_newton_iterations=int(maximum_newton_iterations),
            )

            if not ok_mid:
                interval_end_value = float(midpoint_value)
                continue

            current_full_displacement_vector = u_mid
            old_state_by_element_id = state_mid
            current_target_value = float(midpoint_value)

            accepted_target_displacement_history.append(current_target_value)
            reaction_history.append(reaction_mid.copy())
            newton_iteration_history.append(int(iterations_mid))

            full_prescribed_displacement_vector = collect_prescribed_displacements_from_model(model)
            full_prescribed_displacement_vector[driven_degree_of_freedom_index_array] = float(target_displacement_value)

            ok_end, u_end, state_end, reaction_end, iterations_end = solve_one_displacement_step_newton(
                model=model,
                target_full_prescribed_displacement_vector=full_prescribed_displacement_vector,
                initial_full_displacement_vector=current_full_displacement_vector,
                old_state_by_element_id=old_state_by_element_id,
                newton_residual_tolerance=float(newton_residual_tolerance),
                newton_increment_tolerance=float(newton_increment_tolerance),
                maximum_newton_iterations=int(maximum_newton_iterations),
            )

            if ok_end:
                current_full_displacement_vector = u_end
                old_state_by_element_id = state_end
                current_target_value = float(target_displacement_value)

                accepted_target_displacement_history.append(current_target_value)
                reaction_history.append(reaction_end.copy())
                newton_iteration_history.append(int(iterations_end))
                success_flag = True
                break

            interval_start_value = float(current_target_value)

        if not success_flag:
            raise RuntimeError("Adaptive cutback failed. Increase number_of_initial_steps or maximum_subdivisions.")

    model.u = current_full_displacement_vector
    model.f = reaction_history[-1] if reaction_history else np.zeros(total_number_of_degrees_of_freedom, dtype=float)
    model.nonlinear_state_by_element_id = old_state_by_element_id

    return {
        "accepted_target_displacement_history": np.asarray(accepted_target_displacement_history, dtype=float),
        "reaction_history": reaction_history,
        "newton_iteration_history": np.asarray(newton_iteration_history, dtype=int),
        "final_displacement_vector": current_full_displacement_vector,
        "final_state_by_element_id": old_state_by_element_id,
    }