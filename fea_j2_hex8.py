import numpy as np
import scipy.sparse as sp
from dataclasses import dataclass
from pypardiso import spsolve as pardiso_spsolve
import matplotlib.pyplot as plt
import pyvista as pv


def voigt_dev_projector():
    """Deviatoric projector in 6x6 (Mandel basis will reuse same structure)."""
    P = np.eye(6)
    P[:3, :3] -= (1.0 / 3.0) * np.ones((3, 3))
    return P

@dataclass
class Material:
    E: float
    nu: float
    Sy: float
    Hiso: float

    @property
    def mu(self):
        return self.E / (2.0 * (1.0 + self.nu))

    @property
    def lam(self):
        return self.E * self.nu / ((1.0 + self.nu) * (1.0 - 2.0 * self.nu))

    def D_elastic_voigt(self):
        """Voigt with engineering shear: [exx eyy ezz gxy gyz gzx] -> [sxx syy szz txy tyz tzx]."""
        mu = self.mu
        lam = self.lam
        D = np.zeros((6, 6), dtype=float)
        D[:3, :3] = lam * np.ones((3, 3)) + 2.0 * mu * np.eye(3)
        D[3:, 3:] = mu * np.eye(3)
        return D


def J2_return_mandel(eps_v, epsp_v_old, epbar_old, D_el_v, mu, Sy, Hiso):
    """
    Mandel-based J2 return mapping (matches your MATLAB function).

    Inputs:
      eps_v       : (6,) total strain in Voigt with engineering shear
      epsp_v_old  : (6,) plastic strain in Voigt (engineering shear)
      epbar_old   : scalar equivalent plastic strain
      D_el_v      : (6,6) elastic matrix (Voigt engineering shear)
      mu, Sy, Hiso

    Returns:
      sigma_v     : (6,) stress Voigt
      Dalg_v      : (6,6) algorithmic tangent Voigt
      epsp_v_new  : (6,) updated plastic strain Voigt
      epbar_new   : scalar updated epbar
    """
    # Transforms (Voigt engineering shear) <-> Mandel
    T_eps_v2m = np.diag([1, 1, 1, 1 / np.sqrt(2), 1 / np.sqrt(2), 1 / np.sqrt(2)])
    T_eps_m2v = np.diag([1, 1, 1, np.sqrt(2), np.sqrt(2), np.sqrt(2)])

    T_sig_v2m = np.diag([1, 1, 1, np.sqrt(2), np.sqrt(2), np.sqrt(2)])
    T_sig_m2v = np.diag([1, 1, 1, 1 / np.sqrt(2), 1 / np.sqrt(2), 1 / np.sqrt(2)])

    eps_m = T_eps_v2m @ eps_v
    epsp_m_o = T_eps_v2m @ epsp_v_old

    # D_el in Mandel: sigma_m = D_el_m * eps_m
    D_el_m = T_sig_v2m @ D_el_v @ T_eps_m2v

    # Trial
    ee_tr_m = eps_m - epsp_m_o
    sig_tr_m = D_el_m @ ee_tr_m

    # Deviatoric projector in Mandel basis
    Pdev = voigt_dev_projector()
    s_tr_m = Pdev @ sig_tr_m
    s_norm = np.linalg.norm(s_tr_m)

    q_tr = 0.0 if s_norm < 1e-16 else np.sqrt(3 / 2) * s_norm

    Sy_cur = Sy + Hiso * epbar_old
    f = q_tr - Sy_cur

    if f <= 0.0:
        sigma_m = sig_tr_m
        Dalg_m = D_el_m
        epsp_m_new = epsp_m_o
        epbar_new = epbar_old
    else:
        dgamma = f / (3.0 * mu + Hiso)
        n_dev = s_tr_m / s_norm
        N_m = np.sqrt(3 / 2) * n_dev

        sigma_m = sig_tr_m - 2.0 * mu * dgamma * N_m
        epsp_m_new = epsp_m_o + dgamma * N_m
        epbar_new = epbar_old + dgamma

        # Algorithmic tangent (rank-one update)
        A = D_el_m @ N_m
        denom = (N_m @ A) + Hiso
        Dalg_m = D_el_m - np.outer(A, A) / denom

    sigma_v = T_sig_m2v @ sigma_m
    Dalg_v = T_sig_m2v @ Dalg_m @ T_eps_v2m
    epsp_v_new = T_eps_m2v @ epsp_m_new
    return sigma_v, Dalg_v, epsp_v_new, epbar_new


# =========================
# Hex8 shape functions
# =========================
def hex8_dN_dxi(ksi, eta, zeta):
    """
    Returns derivatives w.r.t (ksi,eta,zeta) in arrays shape (3,8).
    Ordering matches your MATLAB code.
    """
    dN_dksi = np.array([
        -(1 - eta) * (1 - zeta),
        (1 - eta) * (1 - zeta),
        (1 + eta) * (1 - zeta),
        -(1 + eta) * (1 - zeta),
        -(1 - eta) * (1 + zeta),
        (1 - eta) * (1 + zeta),
        (1 + eta) * (1 + zeta),
        -(1 + eta) * (1 + zeta)
    ], dtype=float) / 8.0

    dN_deta = np.array([
        -(1 - ksi) * (1 - zeta),
        -(1 + ksi) * (1 - zeta),
        (1 + ksi) * (1 - zeta),
        (1 - ksi) * (1 - zeta),
        -(1 - ksi) * (1 + zeta),
        -(1 + ksi) * (1 + zeta),
        (1 + ksi) * (1 + zeta),
        (1 - ksi) * (1 + zeta)
    ], dtype=float) / 8.0

    dN_dzeta = np.array([
        -(1 - ksi) * (1 - eta),
        -(1 + ksi) * (1 - eta),
        -(1 + ksi) * (1 + eta),
        -(1 - ksi) * (1 + eta),
        (1 - ksi) * (1 - eta),
        (1 + ksi) * (1 - eta),
        (1 + ksi) * (1 + eta),
        (1 - ksi) * (1 + eta)
    ], dtype=float) / 8.0

    return np.vstack([dN_dksi, dN_deta, dN_dzeta])


def build_B(dN_dX):
    """
    dN_dX: (3,8) derivatives w.r.t global coords (X,Y,Z)
    Returns B: (6,24) for Voigt strain [exx eyy ezz gxy gyz gzx]
    """
    B = np.zeros((6, 24), dtype=float)
    for a in range(8):
        ia = 3 * a
        dNx, dNy, dNz = dN_dX[:, a]
        # normal
        B[0, ia + 0] = dNx
        B[1, ia + 1] = dNy
        B[2, ia + 2] = dNz
        # engineering shear
        B[3, ia + 0] = dNy
        B[3, ia + 1] = dNx
        B[4, ia + 1] = dNz
        B[4, ia + 2] = dNy
        B[5, ia + 0] = dNz
        B[5, ia + 2] = dNx
    return B


# =========================
# Mesh generation (ndgrid)
# =========================
def generate_mesh(L, W, Hgeo, le):
    xs = np.arange(0, L + 1e-12, le, dtype=float)
    ys = np.arange(0, W + 1e-12, le, dtype=float)
    zs = np.arange(0, Hgeo + 1e-12, le, dtype=float)

    # MATLAB ndgrid eşleniği: indexing='ij'
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing='ij')  # shape: (nx+1, ny+1, nz+1)

    # MATLAB X(:) column-major => Fortran-order flatten şart
    nodes = np.column_stack([
        X.ravel(order='F'),
        Y.ravel(order='F'),
        Z.ravel(order='F')
    ])

    nx = len(xs) - 1
    ny = len(ys) - 1
    nz = len(zs) - 1

    elements = []
    for k in range(1, nz + 1):
        for j in range(1, ny + 1):
            for i in range(1, nx + 1):
                n1 = (i - 1) + (j - 1) * (nx + 1) + (k - 1) * (nx + 1) * (ny + 1)
                n2 = n1 + 1
                n3 = n2 + (nx + 1)
                n4 = n1 + (nx + 1)
                n5 = n1 + (nx + 1) * (ny + 1)
                n6 = n2 + (nx + 1) * (ny + 1)
                n7 = n3 + (nx + 1) * (ny + 1)
                n8 = n4 + (nx + 1) * (ny + 1)
                elements.append([n1, n2, n3, n4, n5, n6, n7, n8])

    return nodes, np.array(elements, dtype=int), nx, ny, nz


# =========================
# BC definition
# =========================
def build_bcs(nodes, L, W):
    tol = 1e-12
    nodesX0 = np.where(np.abs(nodes[:, 0] - 0.0) < tol)[0]
    nodesXL = np.where(np.abs(nodes[:, 0] - L) < tol)[0]

    # dof indexing: node i => [3*i, 3*i+1, 3*i+2]
    prescribed = set()

    # x=0 fix ux
    for n in nodesX0:
        prescribed.add(3 * n + 0)

    # rigid body constraints
    origin = np.where((np.abs(nodes[:, 0]) < tol) &
                      (np.abs(nodes[:, 1]) < tol) &
                      (np.abs(nodes[:, 2]) < tol))[0]
    yaxis = np.where((np.abs(nodes[:, 0]) < tol) &
                     (np.abs(nodes[:, 1] - W) < tol) &
                     (np.abs(nodes[:, 2]) < tol))[0]
    if origin.size == 0 or yaxis.size == 0:
        raise RuntimeError("Rigid-body constraint nodes not found.")
    origin = int(origin[0])
    yaxis = int(yaxis[0])

    # uy, uz at origin
    prescribed.add(3 * origin + 1)
    prescribed.add(3 * origin + 2)
    # uz at another node
    prescribed.add(3 * yaxis + 2)

    driven = np.array([3 * n + 0 for n in nodesXL], dtype=int)  # ux on x=L
    for d in driven:
        prescribed.add(int(d))

    prescribed = np.array(sorted(prescribed), dtype=int)
    all_dofs = np.arange(nodes.shape[0] * 3, dtype=int)
    free = np.setdiff1d(all_dofs, prescribed, assume_unique=False)

    return prescribed, free, driven


# =========================
# Gauss points (2x2x2)
# =========================
def gauss_2x2x2():
    gp = [-1.0 / np.sqrt(3.0), 1.0 / np.sqrt(3.0)]
    pts = []
    for r in gp:
        for s in gp:
            for t in gp:
                pts.append((r, s, t, 1.0))
    return np.array(pts, dtype=float)  # (8,4)


# =========================
# Assembly and step solver
# =========================
@dataclass
class History:
    eps_p: np.ndarray  # (6,8,nelems)
    ep_eq: np.ndarray  # (8,nelems)


def solve_linear_system(K_ff, R_free):
    return pardiso_spsolve(K_ff, R_free)


def solve_one_displacement_step(target_disp, U_in, hist_in,
                                nodes, elements, gauss_pts,
                                D_el, mat: Material,
                                free_dofs, driven_dofs,
                                tol_NR=1e-6, tol_dU=1e-8, max_iter=40):
    """
    Returns:
      ok, U_out, hist_out, sigma_nom, nIter, last_gp_stress (optional for viz)
    """
    U = U_in.copy()
    hist = History(eps_p=hist_in.eps_p.copy(), ep_eq=hist_in.ep_eq.copy())

    # impose displacement on driven dofs
    U[driven_dofs] = target_disp

    ne = elements.shape[0]
    ndofs = U.size

    converged = False
    sigma_nom = np.nan
    iter_out = max_iter

    # For visualization: store last converged gauss stress per element/gp
    last_stress = None  # (6,8,ne)

    for it in range(1, max_iter + 1):
        # triplet assembly
        rows = []
        cols = []
        data = []
        F_int = np.zeros(ndofs, dtype=float)

        new_eps_p = hist.eps_p.copy()
        new_ep_eq = hist.ep_eq.copy()

        # element loop
        for el in range(ne):
            en = elements[el]  # (8,)
            Xel = nodes[en, :]  # (8,3)

            # eldofs (24,)
            eldofs = np.empty(24, dtype=int)
            eldofs[0::3] = 3 * en + 0
            eldofs[1::3] = 3 * en + 1
            eldofs[2::3] = 3 * en + 2

            Uel = U[eldofs]
            Kel = np.zeros((24, 24), dtype=float)
            Fel_int = np.zeros(24, dtype=float)

            for g in range(8):
                ksi, eta, zeta, w = gauss_pts[g]
                dN_par = hex8_dN_dxi(ksi, eta, zeta)  # (3,8)

                J = dN_par @ Xel  # (3,3)
                detJ = np.linalg.det(J)
                if detJ <= 0.0:
                    raise RuntimeError(f"Invalid Jacobian detJ<=0 at element {el}, gp {g}")
                dN_dX = np.linalg.solve(J, dN_par)  # (3,8)

                B = build_B(dN_dX)  # (6,24)
                strain = B @ Uel  # (6,)

                eps_p_old = hist.eps_p[:, g, el]
                ep_eq_old = hist.ep_eq[g, el]

                stress, D_ep, eps_p_new, ep_eq_new = J2_return_mandel(
                    strain, eps_p_old, ep_eq_old, D_el, mat.mu, mat.Sy, mat.Hiso
                )

                new_eps_p[:, g, el] = eps_p_new
                new_ep_eq[g, el] = ep_eq_new

                dV = detJ * w
                Kel += (B.T @ D_ep @ B) * dV
                Fel_int += (B.T @ stress) * dV

            # scatter Kel into global triplets
            rr = np.repeat(eldofs, 24)
            cc = np.tile(eldofs, 24)
            rows.append(rr)
            cols.append(cc)
            data.append(Kel.ravel())

            # scatter internal force
            F_int[eldofs] += Fel_int

        rows = np.concatenate(rows)
        cols = np.concatenate(cols)
        data = np.concatenate(data)
        K = sp.coo_matrix((data, (rows, cols)), shape=(ndofs, ndofs)).tocsr()

        # residual on free dofs (no external forces, displacement control)
        R_free = -F_int[free_dofs]
        R_norm = np.linalg.norm(R_free)

        if it == 1:
            r0 = max(R_norm, 1.0)

        if (R_norm / r0 < tol_NR) or (R_norm < 1e-8):
            hist.eps_p = new_eps_p
            hist.ep_eq = new_ep_eq

            # compute nominal reaction and stress
            R_reac = np.sum(F_int[driven_dofs])
            A = (nodes[:, 1].max() - nodes[:, 1].min()) * (nodes[:, 2].max() - nodes[:, 2].min())
            sigma_nom = R_reac / A

            converged = True
            iter_out = it
            last_stress = None  # you can compute/store if you want per gp; omitted for speed
            return True, U, hist, sigma_nom, iter_out, last_stress

        # solve correction
        K_ff = K[free_dofs, :][:, free_dofs]
        dU_f = solve_linear_system(K_ff, R_free)

        # simple damping like your code
        dU_norm = np.linalg.norm(dU_f)
        alpha = 1.0
        if dU_norm > 1.0:
            alpha = min(1.0, 1.0 / dU_norm)

        U[free_dofs] += alpha * dU_f

        # secondary check on increment size (matches your idea)
        if dU_norm < tol_dU:
            hist.eps_p = new_eps_p
            hist.ep_eq = new_ep_eq

            R_reac = np.sum(F_int[driven_dofs])
            A = (nodes[:, 1].max() - nodes[:, 1].min()) * (nodes[:, 2].max() - nodes[:, 2].min())
            sigma_nom = R_reac / A

            converged = True
            iter_out = it
            last_stress = None
            return True, U, hist, sigma_nom, iter_out, last_stress

    # no convergence
    return False, U_in, hist_in, np.nan, max_iter, None


# =========================
# Postprocessing (PyVista)
# =========================
def hex8_to_vtk_unstructured(nodes, elements):
    """
    Build a PyVista UnstructuredGrid from nodes (N,3) and elements (E,8).
    VTK_HEXAHEDRON cell type = 12
    """

    n_cells = elements.shape[0]
    # VTK expects a "cells" array: [8, n0, n1, ..., n7, 8, ...]
    cells = np.hstack([np.full((n_cells, 1), 8, dtype=np.int64), elements.astype(np.int64)]).ravel()
    celltypes = np.full(n_cells, 12, dtype=np.uint8)
    grid = pv.UnstructuredGrid(cells, celltypes, nodes)
    return grid


def add_displacement_to_grid(grid, U):
    n = grid.points.shape[0]
    disp = U.reshape((n, 3))
    grid.point_data["U"] = disp
    grid.point_data["U_mag"] = np.linalg.norm(disp, axis=1)
    return grid


# =========================
# Main
# =========================
def main():
    # --- Material and geometry (match your MATLAB values) ---
    E = 200e3  # MPa
    nu = 0.3
    Sy = 250.0  # MPa
    Hiso = 20e3  # MPa

    L = 200.0
    W = 30.0
    Hgeo = 30.0
    le = 5.0

    mat = Material(E=E, nu=nu, Sy=Sy, Hiso=Hiso)
    D_el = mat.D_elastic_voigt()

    # --- Mesh ---
    nodes, elements, nx, ny, nz = generate_mesh(L, W, Hgeo, le)
    nn = nodes.shape[0]
    ndofs = nn * 3
    ne = elements.shape[0]
    print(f"Mesh: nodes={nn}, elements={ne}, dofs={ndofs} (nx,ny,nz)=({nx},{ny},{nz})")

    # --- BCs ---
    prescribed, free, driven = build_bcs(nodes, L, W)
    print(f"BC: prescribed dofs={prescribed.size}, free dofs={free.size}, driven dofs={driven.size}")

    # --- Gauss points ---
    gauss_pts = gauss_2x2x2()

    # --- Nonlinear settings ---
    target_total_strain = 0.01
    total_disp = target_total_strain * L

    num_steps_initial = 21
    max_subdivisions = 5

    tol_NR = 1e-6
    tol_dU = 1e-8
    max_iter = 40

    # --- State ---
    U = np.zeros(ndofs, dtype=float)
    hist = History(
        eps_p=np.zeros((6, 8, ne), dtype=float),
        ep_eq=np.zeros((8, ne), dtype=float)
    )

    eps_nom_hist = []
    sigma_nom_hist = []
    iter_hist = []

    print("Starting Newton-Raphson Solver...")

    step_targets = np.linspace(total_disp / num_steps_initial, total_disp, num_steps_initial)
    current_target = 0.0
    accepted = 0

    for iStep, uT in enumerate(step_targets, start=1):
        ok, U_new, hist_new, sigma_nom, nIter, _ = solve_one_displacement_step(
            uT, U, hist,
            nodes, elements, gauss_pts,
            D_el, mat,
            free, driven,
            tol_NR=tol_NR, tol_dU=tol_dU, max_iter=max_iter
        )

        if ok:
            accepted += 1
            U, hist = U_new, hist_new
            current_target = uT
            eps_nom_hist.append(current_target / L)
            sigma_nom_hist.append(sigma_nom)
            iter_hist.append(nIter)
            print(
                f"Accepted step {accepted}: u={current_target:.6f} mm, eps={current_target / L:.6f}, sigma={sigma_nom:.3f} MPa")
        else:
            print(f"Step to u={uT:.6f} mm failed. Starting cutback...")

            u_start = current_target
            u_end = uT
            success = False

            for sub in range(1, max_subdivisions + 1):
                umid = 0.5 * (u_start + u_end)

                ok1, U1, H1, s1, it1, _ = solve_one_displacement_step(
                    umid, U, hist,
                    nodes, elements, gauss_pts,
                    D_el, mat,
                    free, driven,
                    tol_NR=tol_NR, tol_dU=tol_dU, max_iter=max_iter
                )
                if not ok1:
                    u_end = umid
                    print(f"  Cutback level {sub}: midpoint failed (u={umid:.6f}). Shrinking interval.")
                    continue

                # accept midpoint
                accepted += 1
                U, hist = U1, H1
                current_target = umid
                eps_nom_hist.append(current_target / L)
                sigma_nom_hist.append(s1)
                iter_hist.append(it1)
                print(f"  Cutback level {sub}: accepted midpoint u={umid:.6f} mm")

                # try endpoint again from midpoint state
                ok2, U2, H2, s2, it2, _ = solve_one_displacement_step(
                    uT, U, hist,
                    nodes, elements, gauss_pts,
                    D_el, mat,
                    free, driven,
                    tol_NR=tol_NR, tol_dU=tol_dU, max_iter=max_iter
                )

                if ok2:
                    accepted += 1
                    U, hist = U2, H2
                    current_target = uT
                    eps_nom_hist.append(current_target / L)
                    sigma_nom_hist.append(s2)
                    iter_hist.append(it2)
                    print(f"  Cutback succeeded: endpoint u={uT:.6f} mm accepted.")
                    success = True
                    break
                else:
                    u_start = current_target
                    print(f"  Endpoint still failed at cutback level {sub}. Continue bisecting.")

            if not success:
                raise RuntimeError(
                    f"Adaptive cutback failed near target displacement {uT:.6f} mm. "
                    f"Increase num_steps_initial or max_subdivisions."
                )

    print("\nAnalysis Complete!")

    eps_nom_hist = np.array(eps_nom_hist, dtype=float)
    sigma_nom_hist = np.array(sigma_nom_hist, dtype=float)
    iter_hist = np.array(iter_hist, dtype=int)

    # --- Analytical bilinear comparison (same as your MATLAB) ---
    Et = (E * Hiso) / (E + Hiso)
    eps_y = Sy / E

    eps_ana = np.linspace(0.0, float(eps_nom_hist.max() if eps_nom_hist.size else 0.0), 500)
    sigma_ana = np.where(eps_ana <= eps_y, E * eps_ana, Sy + Et * (eps_ana - eps_y))

    # --- Plots ---
    plt.figure()
    plt.plot(eps_nom_hist, sigma_nom_hist, "o-", linewidth=1.5, markersize=4, label="3D FEA (nominal)")
    plt.plot(eps_ana, sigma_ana, "--", linewidth=1.8, label="Ideal Bilinear (uniaxial)")
    plt.grid(True)
    plt.xlabel(r"Nominal Strain, $\epsilon = u/L$")
    plt.ylabel(r"Nominal Stress, $\sigma = F/A$ (MPa)")
    plt.title("3D FEA vs Initial Bilinear Material Definition (Uniaxial)")
    plt.legend()

    plt.figure()
    plt.plot(np.arange(1, len(iter_hist) + 1), iter_hist, "o-", linewidth=1.2, markersize=4)
    plt.grid(True)
    plt.xlabel("Accepted Increment Index")
    plt.ylabel("Newton Iterations")
    plt.title("Newton Iterations per Accepted Increment")

    print("\nAcceptedStep | eps_nom | sigma_nom(MPa) | NR_iters")
    for i in range(len(eps_nom_hist)):
        print(f"{i + 1:4d} | {eps_nom_hist[i]:.6e} | {sigma_nom_hist[i]:.6f} | {iter_hist[i]:3d}")

    print("\nMaterial comparison info:")
    print(f"Yield strain eps_y = {eps_y:.6f}")
    print(f"Uniaxial post-yield tangent Et = {Et:.2f} MPa")
    print(f"Linear solver: pypardiso")

    grid = hex8_to_vtk_unstructured(nodes, elements)
    grid = add_displacement_to_grid(grid, U)

    # Deform (scaled)
    scale = 1.0
    warped = grid.warp_by_vector("U", factor=scale)

    pl = pv.Plotter()
    pl.add_text("Deformed mesh (warp by displacement)", font_size=12)
    pl.add_mesh(warped, scalars="U_mag", show_edges=True)
    pl.show()

    plt.show()


if __name__ == "__main__":
    main()
