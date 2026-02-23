import numpy as np
import scipy.sparse as sp
import pypardiso as pp

from solver.result_editor import element_dof_ids, element_gauss_strain_stress_yield, model_element_fields


def isotropic_constitutive_matrix(E: float, nu: float) -> np.ndarray:
    lam = E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
    mu = E / (2.0 * (1.0 + nu))
    D = np.zeros((6, 6), dtype=float)
    D[0, 0] = lam + 2.0 * mu
    D[1, 1] = lam + 2.0 * mu
    D[2, 2] = lam + 2.0 * mu
    D[0, 1] = lam
    D[0, 2] = lam
    D[1, 0] = lam
    D[1, 2] = lam
    D[2, 0] = lam
    D[2, 1] = lam
    D[3, 3] = mu
    D[4, 4] = mu
    D[5, 5] = mu
    return D


def collect_prescribed_displacements(model) -> np.ndarray:
    n = model.total_number_of_dofs()
    prescribed = np.full(n, np.nan, dtype=float)
    for node_id, node in model.nodes_by_id.items():
        base = 3 * (int(node_id) - 1)
        v = node.prescribed_displacement
        if not np.isnan(v[0]):
            prescribed[base + 0] = float(v[0])
        if not np.isnan(v[1]):
            prescribed[base + 1] = float(v[1])
        if not np.isnan(v[2]):
            prescribed[base + 2] = float(v[2])
    return prescribed


def partition_solve(K, rhs: np.ndarray, prescribed: np.ndarray) -> np.ndarray:
    K = K if sp.isspmatrix_csr(K) else sp.csr_matrix(K)
    rhs = np.asarray(rhs, dtype=float)
    n = int(K.shape[0])
    fixed = np.where(~np.isnan(prescribed))[0]
    free = np.where(np.isnan(prescribed))[0]
    x = np.zeros(n, dtype=float)
    if fixed.size:
        x[fixed] = prescribed[fixed]
    if free.size:
        K_ff = K[free, :][:, free]
        if fixed.size:
            K_fc = K[free, :][:, fixed]
            b = rhs[free] - K_fc @ x[fixed]
        else:
            b = rhs[free]
        x[free] = pp.spsolve(K_ff, b)
    return x


def map_prescribed_with_contacts(full_prescribed: np.ndarray, dof_mapping: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    dof_mapping = np.asarray(dof_mapping, dtype=np.int64)
    n_reduced = int(dof_mapping.max()) + 1
    reduced = np.full(n_reduced, np.nan, dtype=float)
    idx = np.where(~np.isnan(full_prescribed))[0]
    if idx.size == 0:
        return reduced
    r = dof_mapping[idx]
    v = full_prescribed[idx].astype(float, copy=False)
    order = np.argsort(r)
    r = r[order]
    v = v[order]
    starts = np.r_[0, np.where(r[1:] != r[:-1])[0] + 1]
    vmin = np.minimum.reduceat(v, starts)
    vmax = np.maximum.reduceat(v, starts)
    bad = np.where(np.abs(vmax - vmin) > tol)[0]
    if bad.size:
        b = int(bad[0])
        rr = int(r[starts[b]])
        raise ValueError(f"Conflicting prescribed displacements on reduced DOF {rr}: {vmin[b]} vs {vmax[b]}")
    reduced[r[starts]] = v[starts]
    return reduced


def reduce_vector_with_contacts(v_full: np.ndarray, dof_mapping: np.ndarray) -> np.ndarray:
    dof_mapping = np.asarray(dof_mapping, dtype=np.int64)
    n_reduced = int(dof_mapping.max()) + 1
    return np.bincount(dof_mapping, weights=np.asarray(v_full, dtype=float), minlength=n_reduced).astype(float)


def solve_increment(model, K_full, rhs_full: np.ndarray, prescribed_inc_full: np.ndarray) -> np.ndarray:
    if not getattr(model, "contact_constraint_sets", None):
        du = partition_solve(K_full, rhs_full, prescribed_inc_full)
        return du

    dof_mapping = model.build_dof_mapping_with_contacts().astype(np.int64)
    n_full = int(dof_mapping.shape[0])
    n_reduced = int(dof_mapping.max()) + 1

    P = sp.csr_matrix(
        (np.ones(n_full, dtype=float), (np.arange(n_full, dtype=np.int64), dof_mapping)),
        shape=(n_full, n_reduced),
    )

    K_full = K_full if sp.isspmatrix_csr(K_full) else sp.csr_matrix(K_full)
    K_red = (P.T @ (K_full @ P)).tocsr()
    K_red.sum_duplicates()

    rhs_red = reduce_vector_with_contacts(rhs_full, dof_mapping)
    prescribed_inc_red = map_prescribed_with_contacts(prescribed_inc_full, dof_mapping)

    du_red = partition_solve(K_red, rhs_red, prescribed_inc_red)
    return du_red[dof_mapping]


def build_global_tangent_stiffness(model, u: np.ndarray) -> sp.csr_matrix:
    u = np.asarray(u, dtype=float)
    ndof = model.total_number_of_dofs()
    rows_chunks, cols_chunks, data_chunks = [], [], []

    element_ids = np.array(sorted(model.elements_by_id.keys()), dtype=int)

    for eid in element_ids:
        element_data = model.elements_by_id[int(eid)]
        fe = element_data.finite_element
        dofs = element_dof_ids(element_data.node_ids)
        u_e = u[dofs]

        B_list = fe.B_matrices()
        dV = fe.integration_weights()

        strains = np.vstack([B @ u_e for B in B_list])
        eps_vm = np.array([fe.von_mises_strain(e) for e in strains], dtype=float)

        E0 = float(fe.material.youngs_modulus)
        Et = float(fe.material.tangent_modulus)
        nu = float(fe.material.poissons_ratio)
        eps_y = float(fe.material.yield_strength) / E0

        E_use = Et if np.any(eps_vm > eps_y) else E0
        D = isotropic_constitutive_matrix(E_use, nu)

        nloc = int(dofs.size)
        ke = np.zeros((nloc, nloc), dtype=float)
        for B, dv in zip(B_list, dV):
            ke += (B.T @ D @ B) * float(dv)

        rows_chunks.append(np.repeat(dofs, nloc))
        cols_chunks.append(np.tile(dofs, nloc))
        data_chunks.append(ke.reshape(-1))

    rows = np.concatenate(rows_chunks).astype(np.int64, copy=False)
    cols = np.concatenate(cols_chunks).astype(np.int64, copy=False)
    data = np.concatenate(data_chunks).astype(float, copy=False)

    K = sp.coo_matrix((data, (rows, cols)), shape=(ndof, ndof)).tocsr()
    K.sum_duplicates()
    return K


def build_global_internal_force(model, u: np.ndarray) -> np.ndarray:
    u = np.asarray(u, dtype=float)
    ndof = model.total_number_of_dofs()
    f_int = np.zeros(ndof, dtype=float)

    element_ids = np.array(sorted(model.elements_by_id.keys()), dtype=int)

    for eid in element_ids:
        element_data = model.elements_by_id[int(eid)]
        fe = element_data.finite_element
        dofs = element_dof_ids(element_data.node_ids)
        u_e = u[dofs]

        strains, stresses, _yielded = element_gauss_strain_stress_yield(fe, u_e)

        B_list = fe.B_matrices()
        dV = fe.integration_weights()

        f_e = np.zeros_like(u_e, dtype=float)
        for B, s, dv in zip(B_list, stresses, dV):
            f_e += (B.T @ s) * float(dv)

        f_int[dofs] += f_e

    return f_int


def convergence_metrics(model, residual_full: np.ndarray, fext_full: np.ndarray, du_full: np.ndarray, u_full: np.ndarray, prescribed_full: np.ndarray):
    if not getattr(model, "contact_constraint_sets", None):
        free = np.where(np.isnan(prescribed_full))[0]
        r = residual_full[free]
        f = fext_full[free]
        du = du_full[free]
        uu = u_full[free]
        denom_f = np.linalg.norm(f)
        denom_u = np.linalg.norm(uu)
        return (
            np.linalg.norm(r) / (denom_f if denom_f > 0.0 else 1.0),
            np.linalg.norm(du) / (denom_u if denom_u > 0.0 else 1.0),
            free.size,
        )

    dof_mapping = model.build_dof_mapping_with_contacts().astype(np.int64)
    r_red = reduce_vector_with_contacts(residual_full, dof_mapping)
    f_red = reduce_vector_with_contacts(fext_full, dof_mapping)
    du_red = reduce_vector_with_contacts(du_full, dof_mapping)
    u_red = reduce_vector_with_contacts(u_full, dof_mapping)

    prescribed_inc_full = np.where(np.isnan(prescribed_full), np.nan, 0.0)
    prescribed_inc_red = map_prescribed_with_contacts(prescribed_inc_full, dof_mapping)
    free = np.where(np.isnan(prescribed_inc_red))[0]

    denom_f = np.linalg.norm(f_red[free])
    denom_u = np.linalg.norm(u_red[free])

    return (
        np.linalg.norm(r_red[free]) / (denom_f if denom_f > 0.0 else 1.0),
        np.linalg.norm(du_red[free]) / (denom_u if denom_u > 0.0 else 1.0),
        free.size,
    )


def solve_nonlinear_model(model, tol_f=1e-9, tol_u=1e-9, max_iter=30):
    f_ext = model.build_global_force_vector()
    prescribed_full = collect_prescribed_displacements(model)
    fixed = np.where(~np.isnan(prescribed_full))[0]

    u = np.zeros(model.total_number_of_dofs(), dtype=float)
    if fixed.size:
        u[fixed] = prescribed_full[fixed]

    residual = f_ext.copy()

    for it in range(1, max_iter + 1):
        K = build_global_tangent_stiffness(model, u)
        prescribed_inc = np.where(np.isnan(prescribed_full), np.nan, 0.0)

        du = solve_increment(model, K, residual, prescribed_inc)
        u = u + du
        if fixed.size:
            u[fixed] = prescribed_full[fixed]

        f_int = build_global_internal_force(model, u)
        residual = f_ext - f_int

        err_f, err_u, nfree = convergence_metrics(model, residual, f_ext, du, u, prescribed_full)

        print(f"iter {it:2d} |free|={nfree:6d}  err_f={err_f:.3e}  err_u={err_u:.3e}  ||R||={np.linalg.norm(residual):.3e}  ||du||={np.linalg.norm(du):.3e}")

        if err_f < tol_f and err_u < tol_u:
            break

    element_ids, element_strain, element_stress, element_yielded = model_element_fields(model, u)
    reaction = f_int - f_ext
    return reaction, u, element_ids, element_strain, element_stress, element_yielded
