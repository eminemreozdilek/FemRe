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


def solve_model(model) -> tuple[np.ndarray, np.ndarray]:
    k_full = model.build_global_stiffness_matrix()
    f_full = model.build_global_force_vector()
    prescribed_full = __collect_prescribed_displacements(model)

    # No contacts -> plain solve
    if not getattr(model, "contact_constraint_sets", None):
        return __partition_solve(k_full, f_full, prescribed_full)

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

        _, u_reduced = __partition_solve(k_reduced, f_reduced, prescribed_reduced)

        u_full = u_reduced[dof_mapping]
        reaction_full = k_full @ u_full - f_full
        return reaction_full, u_full
