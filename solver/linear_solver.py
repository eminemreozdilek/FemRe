import numpy as np
import scipy.sparse as sp
import pypardiso as pp


def __collect_prescribed_displacements(
        model
) -> np.ndarray:
    number_of_dofs = model.total_number_of_dofs()
    prescribed = np.full(number_of_dofs, np.nan, dtype=float)
    for node_id, node in model.nodes_by_id.items():
        base = 3 * (int(node_id) - 1)
        # node.prescribed_displacement is length-3
        v = node.prescribed_displacement
        if not np.isnan(v[0]):
            prescribed[base + 0] = float(v[0])
        if not np.isnan(v[1]):
            prescribed[base + 1] = float(v[1])
        if not np.isnan(v[2]):
            prescribed[base + 2] = float(v[2])
    return prescribed


def __partition_solve(
        stiffness_matrix,
        force_vector: np.ndarray,
        prescribed_displacements: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    k_global = stiffness_matrix if sp.isspmatrix_csr(stiffness_matrix) else sp.csr_matrix(stiffness_matrix)
    force_vector = np.asarray(force_vector, dtype=float)

    n = int(k_global.shape[0])
    is_fixed = ~np.isnan(prescribed_displacements)
    fixed = np.where(is_fixed)[0]
    free = np.where(~is_fixed)[0]

    u = np.zeros(n, dtype=float)
    if fixed.size:
        u[fixed] = prescribed_displacements[fixed]

    if free.size:
        k_ff = k_global[free, :][:, free]
        if fixed.size:
            k_fc = k_global[free, :][:, fixed]
            rhs = force_vector[free] - k_fc @ u[fixed]
        else:
            rhs = force_vector[free]
        u[free] = pp.spsolve(k_ff, rhs)

    reaction = k_global @ u - force_vector
    return reaction, u


def __map_prescribed_displacements_with_contacts_fast(
        full_prescribed: np.ndarray,
        dof_mapping: np.ndarray,
        n_reduced: int | None = None,
        tol: float = 1e-12,
) -> np.ndarray:
    if n_reduced is None:
        n_reduced = int(dof_mapping.max()) + 1

    reduced = np.full(int(n_reduced), np.nan, dtype=float)

    idx = np.where(~np.isnan(full_prescribed))[0]
    if idx.size == 0:
        return reduced

    r = dof_mapping[idx].astype(np.int64, copy=False)
    v = full_prescribed[idx].astype(float, copy=False)

    order = np.argsort(r)
    r = r[order]
    v = v[order]

    # group boundaries where reduced index changes
    starts = np.r_[0, np.where(r[1:] != r[:-1])[0] + 1]

    vmin = np.minimum.reduceat(v, starts)
    vmax = np.maximum.reduceat(v, starts)

    bad = np.where(np.abs(vmax - vmin) > tol)[0]
    if bad.size:
        b = int(bad[0])
        rr = int(r[starts[b]])
        raise ValueError(
            f"Conflicting prescribed displacements on contact-coupled reduced DOF {rr}: {vmin[b]} vs {vmax[b]}")

    reduced[r[starts]] = v[starts]
    return reduced


def __build_constraint_matrix(
        model,
        number_of_dofs: int,
) -> tuple[sp.csr_matrix, np.ndarray, np.ndarray]:
    constraint_data_list = getattr(model, "constraint_equation_data_list", None)
    if not constraint_data_list:
        return (
            sp.csr_matrix((0, int(number_of_dofs)), dtype=float),
            np.zeros(0, dtype=float),
            np.zeros(0, dtype=np.int64),
        )

    ordered_constraint_list = sorted(
        constraint_data_list,
        key=lambda equation_data: int(equation_data.constraint_eq_id),
    )

    dof_chunks = []
    coefficient_chunks = []
    rhs_values = []
    equation_ids = []

    for equation_data in ordered_constraint_list:
        dof_indices = np.asarray(equation_data.dof_indices, dtype=np.int64).reshape(-1)
        coefficients = np.asarray(equation_data.coefficients, dtype=float).reshape(-1)

        if dof_indices.size == 0:
            raise ValueError(f"Constraint equation {equation_data.constraint_eq_id} has no terms")
        if dof_indices.size != coefficients.size:
            raise ValueError(
                f"Constraint equation {equation_data.constraint_eq_id} has mismatched dof_indices and coefficients lengths"
            )

        dof_chunks.append(dof_indices)
        coefficient_chunks.append(coefficients)
        rhs_values.append(float(equation_data.equation_constant))
        equation_ids.append(int(equation_data.constraint_eq_id))

    term_counts = np.array([chunk.size for chunk in dof_chunks], dtype=np.int64)
    rows = np.repeat(np.arange(len(dof_chunks), dtype=np.int64), term_counts)
    cols = np.concatenate(dof_chunks).astype(np.int64, copy=False)
    data = np.concatenate(coefficient_chunks).astype(float, copy=False)

    if cols.size and (int(cols.min()) < 0 or int(cols.max()) >= int(number_of_dofs)):
        raise ValueError("Constraint equation references dof index outside the global system")

    g_matrix = sp.coo_matrix(
        (data, (rows, cols)),
        shape=(len(dof_chunks), int(number_of_dofs)),
    ).tocsr()
    g_matrix.sum_duplicates()

    c_vector = np.asarray(rhs_values, dtype=float)
    equation_id_array = np.asarray(equation_ids, dtype=np.int64)
    return g_matrix, c_vector, equation_id_array


def __remove_trivial_constraint_rows(
        constraint_matrix: sp.csr_matrix,
        constraint_rhs: np.ndarray,
        equation_ids: np.ndarray,
        tolerance: float = 1e-14,
) -> tuple[sp.csr_matrix, np.ndarray, np.ndarray]:
    if constraint_matrix.shape[0] == 0:
        return constraint_matrix, constraint_rhs, equation_ids

    row_l1_norm = np.asarray(np.abs(constraint_matrix).sum(axis=1)).ravel()
    keep_mask = row_l1_norm > float(tolerance)
    if np.all(keep_mask):
        return constraint_matrix, constraint_rhs, equation_ids

    dropped_indices = np.where(~keep_mask)[0]
    inconsistent_indices = dropped_indices[np.abs(constraint_rhs[dropped_indices]) > float(tolerance)]
    if inconsistent_indices.size:
        bad_index = int(inconsistent_indices[0])
        bad_equation_id = int(equation_ids[bad_index])
        raise ValueError(
            f"Constraint equation {bad_equation_id} collapses to an inconsistent zero row after dof mapping"
        )

    filtered_matrix = constraint_matrix[keep_mask, :].tocsr()
    filtered_rhs = np.asarray(constraint_rhs[keep_mask], dtype=float)
    filtered_equation_ids = np.asarray(equation_ids[keep_mask], dtype=np.int64)
    return filtered_matrix, filtered_rhs, filtered_equation_ids


def __augment_system_with_lagrange(
        stiffness_matrix: sp.csr_matrix,
        force_vector: np.ndarray,
        constraint_matrix: sp.csr_matrix,
        constraint_rhs: np.ndarray,
) -> tuple[sp.csr_matrix, np.ndarray]:
    k_global = stiffness_matrix if sp.isspmatrix_csr(stiffness_matrix) else sp.csr_matrix(stiffness_matrix)
    force_vector = np.asarray(force_vector, dtype=float)
    constraint_rhs = np.asarray(constraint_rhs, dtype=float)

    number_of_constraints = int(constraint_matrix.shape[0])
    if number_of_constraints == 0:
        return k_global, force_vector

    zero_block = sp.csr_matrix((number_of_constraints, number_of_constraints), dtype=float)
    k_augmented = sp.bmat(
        [[k_global, constraint_matrix.T], [constraint_matrix, zero_block]],
        format="csr",
    )
    k_augmented.sum_duplicates()

    f_augmented = np.concatenate([force_vector, constraint_rhs])
    return k_augmented, f_augmented


def __store_constraint_lagrange_multipliers(
        model,
        equation_ids: np.ndarray,
        multiplier_values: np.ndarray,
) -> None:
    model.lambda_constraint_equations = {
        int(equation_id): float(multiplier_values[index])
        for index, equation_id in enumerate(np.asarray(equation_ids, dtype=np.int64))
    }


def solve_model(model) -> tuple[np.ndarray, np.ndarray]:
    k_full = model.build_global_stiffness_matrix()
    f_full = model.build_global_force_vector()
    prescribed_full = __collect_prescribed_displacements(model)
    model.lambda_constraint_equations = {}

    has_contact_constraints = bool(getattr(model, "contact_constraint_sets", None))
    has_constraint_equations = bool(getattr(model, "constraint_equation_data_list", None))

    # No contacts -> plain solve
    if not has_contact_constraints:
        if not has_constraint_equations:
            return __partition_solve(k_full, f_full, prescribed_full)

        g_full, c_vector, equation_ids = __build_constraint_matrix(
            model=model,
            number_of_dofs=int(k_full.shape[0]),
        )
        g_full, c_vector, equation_ids = __remove_trivial_constraint_rows(
            constraint_matrix=g_full,
            constraint_rhs=c_vector,
            equation_ids=equation_ids,
        )

        if g_full.shape[0] == 0:
            return __partition_solve(k_full, f_full, prescribed_full)

        k_augmented, f_augmented = __augment_system_with_lagrange(
            stiffness_matrix=k_full,
            force_vector=f_full,
            constraint_matrix=g_full,
            constraint_rhs=c_vector,
        )
        prescribed_augmented = np.concatenate(
            [prescribed_full, np.full(g_full.shape[0], np.nan, dtype=float)]
        )

        _, solution_augmented = __partition_solve(
            stiffness_matrix=k_augmented,
            force_vector=f_augmented,
            prescribed_displacements=prescribed_augmented,
        )

        number_of_dofs = int(k_full.shape[0])
        u_full = np.asarray(solution_augmented[:number_of_dofs], dtype=float)
        lambda_values = np.asarray(solution_augmented[number_of_dofs:], dtype=float)
        __store_constraint_lagrange_multipliers(
            model=model,
            equation_ids=equation_ids,
            multiplier_values=lambda_values,
        )

        reaction_full = k_full @ u_full - f_full
        return reaction_full, u_full

    else:
        dof_mapping = model.build_dof_mapping_with_contacts()

        dof_mapping = np.asarray(dof_mapping, dtype=np.int64)
        n_full = int(dof_mapping.shape[0])
        n_reduced = int(dof_mapping.max()) + 1

        P = sp.csr_matrix(
            (np.ones(n_full, dtype=float), (np.arange(n_full, dtype=np.int64), dof_mapping)),
            shape=(n_full, n_reduced), )

        tmp = k_full @ P
        k_reduced = (P.T @ tmp).tocsr()
        k_reduced.sum_duplicates()

        f_reduced = np.bincount(dof_mapping, weights=np.asarray(f_full, dtype=float), minlength=n_reduced).astype(float)
        prescribed_reduced = __map_prescribed_displacements_with_contacts_fast(
            prescribed_full, dof_mapping, n_reduced=n_reduced)

        if not has_constraint_equations:
            _, u_reduced = __partition_solve(k_reduced, f_reduced, prescribed_reduced)
        else:
            g_full, c_vector, equation_ids = __build_constraint_matrix(
                model=model,
                number_of_dofs=n_full,
            )
            g_reduced = (g_full @ P).tocsr()
            g_reduced.sum_duplicates()
            g_reduced, c_vector, equation_ids = __remove_trivial_constraint_rows(
                constraint_matrix=g_reduced,
                constraint_rhs=c_vector,
                equation_ids=equation_ids,
            )

            if g_reduced.shape[0] == 0:
                _, u_reduced = __partition_solve(k_reduced, f_reduced, prescribed_reduced)
            else:
                k_augmented, f_augmented = __augment_system_with_lagrange(
                    stiffness_matrix=k_reduced,
                    force_vector=f_reduced,
                    constraint_matrix=g_reduced,
                    constraint_rhs=c_vector,
                )
                prescribed_augmented = np.concatenate(
                    [prescribed_reduced, np.full(g_reduced.shape[0], np.nan, dtype=float)]
                )

                _, solution_augmented = __partition_solve(
                    stiffness_matrix=k_augmented,
                    force_vector=f_augmented,
                    prescribed_displacements=prescribed_augmented,
                )

                u_reduced = np.asarray(solution_augmented[:n_reduced], dtype=float)
                lambda_values = np.asarray(solution_augmented[n_reduced:], dtype=float)
                __store_constraint_lagrange_multipliers(
                    model=model,
                    equation_ids=equation_ids,
                    multiplier_values=lambda_values,
                )

        u_full = u_reduced[dof_mapping]
        reaction_full = k_full @ u_full - f_full
        return reaction_full, u_full
