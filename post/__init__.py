"""
Post-processing utilities for the FEA Model.

What you get here (high-level):
- Nodal: displacements, reaction forces (supports), residual/constraint forces
- Element (Gauss + reduced-to-element): strains, stresses, von Mises, principal values,
  strain energy density, element strain energy
- Mesh attachment helpers (cell_data / point_data) + a simple PyVista plotter

Conventions:
- Voigt vectors are assumed as: [xx, yy, zz, xy, yz, xz]
- Strain shear components are assumed to be *engineering* shear strains (gamma_xy, ...).
  If your element uses tensor shear strains instead, change the shear conversion factors
  in voigt_strain_to_tensor().
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Literal, Optional, Sequence, Tuple, Union

import numpy as np


# -----------------------------
# Basics / helpers
# -----------------------------

Voigt6 = np.ndarray
ArrayLike = Union[np.ndarray, Sequence[float]]

REDUCE = Literal["mean", "max", "min", "absmax", "gp0"]


def element_dof_ids(node_ids: np.ndarray) -> np.ndarray:
    """Map element node ids -> global dof ids for 3D (ux,uy,uz) per node."""
    node_ids = np.asarray(node_ids, dtype=np.int64)
    base = 3 * (node_ids - 1)
    return (base[:, None] + np.array([0, 1, 2], dtype=np.int64)[None, :]).ravel()


def _sorted_node_ids(model) -> np.ndarray:
    return np.array(sorted(model.nodes_by_id.keys()), dtype=int)


def _sorted_element_ids(model) -> np.ndarray:
    return np.array(sorted(model.elements_by_id.keys()), dtype=int)


def _ensure_u(model, u: Optional[np.ndarray]) -> np.ndarray:
    if u is None:
        if getattr(model, "u", None) is None:
            model.solve_linear()
        u = model.u
    u = np.asarray(u, dtype=float).reshape(-1)
    return u


def _reduce_gauss(arr: np.ndarray, how: REDUCE) -> np.ndarray:
    """
    Reduce a (n_elem, n_gp, ...) array to (n_elem, ...) according to `how`.
    """
    if arr.ndim < 2:
        raise ValueError("Expected gauss array with shape (n_elem, n_gp, ...)")
    if how == "mean":
        return np.nanmean(arr, axis=1)
    if how == "max":
        return np.nanmax(arr, axis=1)
    if how == "min":
        return np.nanmin(arr, axis=1)
    if how == "absmax":
        a = np.abs(arr)
        idx = np.nanargmax(a, axis=1)
        # fancy take along axis=1
        return np.take_along_axis(arr, idx[:, None, ...], axis=1).squeeze(axis=1)
    if how == "gp0":
        return arr[:, 0, ...]
    raise ValueError(f"Unknown reduction: {how}")


# -----------------------------
# Voigt <-> tensor & invariants
# -----------------------------

def voigt_stress_to_tensor(sig6: np.ndarray) -> np.ndarray:
    """[xx,yy,zz,xy,yz,xz] -> symmetric 3x3 stress tensor."""
    s = np.asarray(sig6, dtype=float)
    t = np.zeros(s.shape[:-1] + (3, 3), dtype=float)
    t[..., 0, 0] = s[..., 0]
    t[..., 1, 1] = s[..., 1]
    t[..., 2, 2] = s[..., 2]
    t[..., 0, 1] = t[..., 1, 0] = s[..., 3]
    t[..., 1, 2] = t[..., 2, 1] = s[..., 4]
    t[..., 0, 2] = t[..., 2, 0] = s[..., 5]
    return t


def voigt_strain_to_tensor(eps6: np.ndarray, engineering_shear: bool = True) -> np.ndarray:
    """
    [xx,yy,zz,xy,yz,xz] -> symmetric 3x3 strain tensor.

    If engineering_shear=True, eps6[3:] are gamma_xy, gamma_yz, gamma_xz
    and we convert to tensor shear strains: eps_xy = gamma_xy/2.
    """
    e = np.asarray(eps6, dtype=float)
    t = np.zeros(e.shape[:-1] + (3, 3), dtype=float)
    t[..., 0, 0] = e[..., 0]
    t[..., 1, 1] = e[..., 1]
    t[..., 2, 2] = e[..., 2]
    shear_scale = 0.5 if engineering_shear else 1.0
    t[..., 0, 1] = t[..., 1, 0] = shear_scale * e[..., 3]
    t[..., 1, 2] = t[..., 2, 1] = shear_scale * e[..., 4]
    t[..., 0, 2] = t[..., 2, 0] = shear_scale * e[..., 5]
    return t


def von_mises_stress(sig6: np.ndarray) -> np.ndarray:
    s = np.asarray(sig6, dtype=float)
    sx, sy, sz, txy, tyz, txz = (s[..., 0], s[..., 1], s[..., 2], s[..., 3], s[..., 4], s[..., 5])
    return np.sqrt(
        0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2)
        + 3.0 * (txy ** 2 + tyz ** 2 + txz ** 2)
    )


def principal_values_sym33(t: np.ndarray) -> np.ndarray:
    """Eigenvalues of symmetric 3x3 tensors, returned as (s1>=s2>=s3)."""
    vals = np.linalg.eigvalsh(t)
    return vals[..., ::-1]


def strain_energy_density(sig6: np.ndarray, eps6: np.ndarray) -> np.ndarray:
    """
    Energy density w = 0.5 * sigma : epsilon

    Assumes eps6 shear components are engineering shear strains.
    With that convention, w = 0.5*(sx*ex + sy*ey + sz*ez + txy*gxy + tyz*gyz + txz*gxz).
    """
    s = np.asarray(sig6, dtype=float)
    e = np.asarray(eps6, dtype=float)
    return 0.5 * np.sum(s * e, axis=-1)


# -----------------------------
# Element Gauss results (strain, stress, yielded)
# -----------------------------

def bilinear_von_mises_stress(material, von_mises_strain: np.ndarray) -> np.ndarray:
    """
    Simple bilinear mapping: sigma_vm = E*eps_vm (elastic) then Et*(eps_vm-eps_y) + sigma_y (plastic)
    Used by your existing code path.
    """
    von_mises_strain = np.asarray(von_mises_strain, dtype=float)
    yield_strain = material.yield_strength / material.youngs_modulus
    elastic_part = np.minimum(von_mises_strain, yield_strain)
    plastic_part = np.maximum(von_mises_strain - yield_strain, 0.0)
    return material.youngs_modulus * elastic_part + material.tangent_modulus * plastic_part


def _von_mises_strain_fallback(eps6: np.ndarray) -> np.ndarray:
    """
    Fallback von-Mises-like strain (from strain tensor deviatoric invariant).
    This is only used if your FiniteElement doesn't implement von_mises_strain().
    """
    E = voigt_strain_to_tensor(eps6, engineering_shear=True)
    tr = np.trace(E, axis1=-2, axis2=-1) / 3.0
    dev = E.copy()
    dev[..., 0, 0] -= tr
    dev[..., 1, 1] -= tr
    dev[..., 2, 2] -= tr
    # J2 = 0.5*dev:dev
    j2 = 0.5 * np.sum(dev * dev, axis=(-2, -1))
    return np.sqrt(2.0 / 3.0) * np.sqrt(2.0 * j2)


def element_gauss_strain_stress_yield(finite_element, u_element: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns:
      strains_gp: (n_gp, 6)
      stresses_gp: (n_gp, 6)
      yielded_gp: (n_gp,)
    """
    B_list = finite_element.B_matrices()
    strains = np.vstack([np.asarray(B, dtype=float) @ u_element for B in B_list])  # (n_gp, 6)

    D = np.asarray(finite_element.material.constitutive_matrix, dtype=float)  # (6,6)
    stress_trial = strains @ D.T  # (n_gp, 6)

    if hasattr(finite_element, "von_mises_strain"):
        vm_strain = np.array([finite_element.von_mises_strain(e) for e in strains], dtype=float)
    else:
        vm_strain = _von_mises_strain_fallback(strains)

    yield_strain = finite_element.material.yield_strength / finite_element.material.youngs_modulus
    yielded = vm_strain > yield_strain
    target_vm_stress = bilinear_von_mises_stress(finite_element.material, vm_strain)

    # Radial return on deviatoric part (your original approach)
    p = (stress_trial[:, 0] + stress_trial[:, 1] + stress_trial[:, 2]) / 3.0
    dev = stress_trial.copy()
    dev[:, 0] -= p
    dev[:, 1] -= p
    dev[:, 2] -= p

    if hasattr(finite_element, "von_mises_stress"):
        vm_trial = np.array([finite_element.von_mises_stress(s) for s in stress_trial], dtype=float)
    else:
        vm_trial = von_mises_stress(stress_trial)

    scale = np.ones_like(vm_trial)
    scale[yielded] = target_vm_stress[yielded] / np.maximum(vm_trial[yielded], 1e-30)

    stresses = dev * scale[:, None]
    stresses[:, 0] += p
    stresses[:, 1] += p
    stresses[:, 2] += p

    return strains, stresses, yielded


def model_element_fields(model, u: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Matches your Model.get_elemental_results() expectations:
    element_ids, element_strain, element_stress, element_yielded
    where strain/stress are GAUSS values: (n_elem, n_gp, 6) and yielded: (n_elem, n_gp)
    """
    u = np.asarray(u, dtype=float).reshape(-1)
    element_ids = _sorted_element_ids(model)
    if element_ids.size == 0:
        return element_ids, np.zeros((0, 0, 6)), np.zeros((0, 0, 6)), np.zeros((0, 0), dtype=bool)

    first_element = model.elements_by_id[int(element_ids[0])].finite_element
    n_gp = len(first_element.B_matrices())

    strains = np.zeros((element_ids.size, n_gp, 6), dtype=float)
    stresses = np.zeros((element_ids.size, n_gp, 6), dtype=float)
    yielded = np.zeros((element_ids.size, n_gp), dtype=bool)

    for e_i, eid in enumerate(element_ids):
        element_data = model.elements_by_id[int(eid)]
        dofs = element_dof_ids(element_data.node_ids)
        u_element = u[dofs]
        fe = element_data.finite_element
        eps_gp, sig_gp, yld_gp = element_gauss_strain_stress_yield(fe, u_element)
        strains[e_i] = eps_gp
        stresses[e_i] = sig_gp
        yielded[e_i] = yld_gp

    return element_ids, strains, stresses, yielded


# -----------------------------
# Nodal results
# -----------------------------

def nodal_displacements(model, u: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns:
      node_ids: (n_nodes,)
      U: (n_nodes, 3)
      U_mag: (n_nodes,)
    """
    u = _ensure_u(model, u)
    node_ids = _sorted_node_ids(model)
    # node ids are created sequentially starting at 1 (see Model._register_component_nodes)
    U = u.reshape(node_ids.size, 3)
    U_mag = np.linalg.norm(U, axis=1)
    return node_ids, U, U_mag


def _prescribed_dof_mask(model) -> np.ndarray:
    ndof = model.total_number_of_dofs()
    mask = np.zeros(ndof, dtype=bool)
    for node_id, node in model.nodes_by_id.items():
        base = 3 * (int(node_id) - 1)
        pd = np.asarray(node.prescribed_displacement, dtype=float)
        for c in range(3):
            if np.isfinite(pd[c]):
                mask[base + c] = True
    return mask


def nodal_reaction_forces(
    model,
    u: Optional[np.ndarray] = None,
    *,
    return_full_vector: bool = False,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Reaction forces from residual: r = K*u - f_ext

    Returns:
      node_ids: (n_nodes,)
      R: (n_nodes, 3)   (reactions at prescribed DOFs; zeros elsewhere unless return_full_vector=True)
      R_mag: (n_nodes,)
    """
    u = _ensure_u(model, u)
    K = model.build_global_stiffness_matrix()
    f_ext = model.build_global_force_vector()

    residual = (K @ u) - f_ext  # (ndof,)

    if not return_full_vector:
        mask = _prescribed_dof_mask(model)
        residual = residual * mask.astype(float)

    node_ids = _sorted_node_ids(model)
    R = residual.reshape(node_ids.size, 3)
    R_mag = np.linalg.norm(R, axis=1)
    return node_ids, R, R_mag


# -----------------------------
# Element results (reduced + invariants)
# -----------------------------

@dataclass(frozen=True)
class ElementGaussResults:
    element_ids: np.ndarray  # (n_elem,)
    strain_gp: np.ndarray    # (n_elem, n_gp, 6)
    stress_gp: np.ndarray    # (n_elem, n_gp, 6)
    yielded_gp: np.ndarray   # (n_elem, n_gp)


def element_gauss_results(model, u: Optional[np.ndarray] = None) -> ElementGaussResults:
    u = _ensure_u(model, u)
    element_ids, eps, sig, yld = model_element_fields(model, u)
    return ElementGaussResults(element_ids=element_ids, strain_gp=eps, stress_gp=sig, yielded_gp=yld)


def element_reduced_results(model, u: Optional[np.ndarray] = None, *, reduce: REDUCE = "mean") -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns per-element (reduced from Gauss points):
      element_ids: (n_elem,)
      strain_e: (n_elem, 6)
      stress_e: (n_elem, 6)
      yielded_e: (n_elem,)  (any gauss point yielded)
    """
    g = element_gauss_results(model, u)
    strain_e = _reduce_gauss(g.strain_gp, reduce)
    stress_e = _reduce_gauss(g.stress_gp, reduce)
    yielded_e = np.any(g.yielded_gp, axis=1)
    return g.element_ids, strain_e, stress_e, yielded_e


def element_von_mises(model, u: Optional[np.ndarray] = None, *, reduce: REDUCE = "mean") -> Tuple[np.ndarray, np.ndarray]:
    g = element_gauss_results(model, u)
    vm_gp = von_mises_stress(g.stress_gp)  # (n_elem, n_gp)
    vm_e = _reduce_gauss(vm_gp, reduce)
    return g.element_ids, vm_e


def element_principal_stresses(model, u: Optional[np.ndarray] = None, *, reduce: REDUCE = "mean") -> Tuple[np.ndarray, np.ndarray]:
    g = element_gauss_results(model, u)
    t_gp = voigt_stress_to_tensor(g.stress_gp)  # (n_elem, n_gp, 3, 3)
    p_gp = principal_values_sym33(t_gp)         # (n_elem, n_gp, 3)
    p_e = _reduce_gauss(p_gp, reduce)           # (n_elem, 3)
    return g.element_ids, p_e


def element_principal_strains(model, u: Optional[np.ndarray] = None, *, reduce: REDUCE = "mean") -> Tuple[np.ndarray, np.ndarray]:
    g = element_gauss_results(model, u)
    t_gp = voigt_strain_to_tensor(g.strain_gp, engineering_shear=True)
    p_gp = principal_values_sym33(t_gp)
    p_e = _reduce_gauss(p_gp, reduce)
    return g.element_ids, p_e


def element_strain_energy(model, u: Optional[np.ndarray] = None, *, reduce: REDUCE = "mean") -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns:
      element_ids: (n_elem,)
      w_density: (n_elem,)  (reduced energy density)
      w_element: (n_elem,)  (energy density * element volume; volume estimated from PyVista)
    """
    g = element_gauss_results(model, u)
    w_gp = strain_energy_density(g.stress_gp, g.strain_gp)  # (n_elem, n_gp)
    w_e = _reduce_gauss(w_gp, reduce)                       # (n_elem,)

    volumes = estimate_element_volumes_from_components(model)  # dict element_id -> volume
    w_elem = np.array([w_e[i] * volumes.get(int(eid), np.nan) for i, eid in enumerate(g.element_ids)], dtype=float)
    return g.element_ids, w_e, w_elem


# -----------------------------
# Mapping results to component meshes
# -----------------------------

def estimate_element_volumes_from_components(model) -> Dict[int, float]:
    """
    Uses each component mesh's cell volumes (PyVista compute_cell_sizes) and maps by global_element_id.

    Requires Model._register_component_elements to have set mesh.cell_data["global_element_id"].
    """
    import pyvista as pv  # local import to keep non-plot usage light

    out: Dict[int, float] = {}
    for comp in model.components:
        mesh = comp.mesh
        if "global_element_id" not in mesh.cell_data:
            continue
        eid_cell = np.asarray(mesh.cell_data["global_element_id"], dtype=int)
        if mesh.n_cells == 0:
            continue
        # compute cell volumes
        sized = mesh.compute_cell_sizes(length=False, area=False, volume=True)
        vol = np.asarray(sized.cell_data["Volume"], dtype=float)
        for eid, v in zip(eid_cell, vol):
            if int(eid) > 0 and int(eid) not in out:
                out[int(eid)] = float(v)
    return out


def attach_point_data_by_node_id(model, name: str, values_by_node: np.ndarray) -> None:
    """
    Attach point data to each component mesh using mesh.point_data["global_node_id"] mapping.
    """
    values_by_node = np.asarray(values_by_node)
    # allow (n_nodes,) or (n_nodes, k)
    for comp in model.components:
        mesh = comp.mesh
        if "global_node_id" not in mesh.point_data:
            continue
        gids = np.asarray(mesh.point_data["global_node_id"], dtype=int)
        mesh.point_data[name] = values_by_node[gids - 1]


def attach_cell_data_by_element_id(model, name: str, values_by_element_id: Dict[int, ArrayLike], fill_value=np.nan) -> None:
    """
    Attach cell data to each component mesh using mesh.cell_data["global_element_id"] mapping.
    values_by_element_id: dict {element_id: scalar or vector}
    """
    for comp in model.components:
        mesh = comp.mesh
        if "global_element_id" not in mesh.cell_data:
            continue
        eids = np.asarray(mesh.cell_data["global_element_id"], dtype=int)
        if eids.size == 0:
            continue

        # infer value shape
        sample = None
        for eid in eids:
            if int(eid) > 0 and int(eid) in values_by_element_id:
                sample = np.asarray(values_by_element_id[int(eid)])
                break
        if sample is None:
            # nothing to attach
            mesh.cell_data[name] = np.full(mesh.n_cells, fill_value, dtype=float)
            continue

        out = np.full((mesh.n_cells,) + sample.shape, fill_value, dtype=float)
        for i, eid in enumerate(eids):
            eid_i = int(eid)
            if eid_i > 0 and eid_i in values_by_element_id:
                out[i] = np.asarray(values_by_element_id[eid_i], dtype=float)
        mesh.cell_data[name] = out


def _dict_from_ids_values(ids: np.ndarray, vals: np.ndarray) -> Dict[int, np.ndarray]:
    ids = np.asarray(ids, dtype=int).reshape(-1)
    vals = np.asarray(vals)
    return {int(i): np.asarray(v) for i, v in zip(ids, vals)}


# -----------------------------
# High-level "compute + attach"
# -----------------------------

def attach_nodal_displacements(model, u: Optional[np.ndarray] = None, *, prefix: str = "U") -> None:
    node_ids, U, U_mag = nodal_displacements(model, u)
    attach_point_data_by_node_id(model, prefix, U)
    attach_point_data_by_node_id(model, f"{prefix}_mag", U_mag)


def attach_nodal_reactions(model, u: Optional[np.ndarray] = None, *, prefix: str = "R", full_vector: bool = False) -> None:
    node_ids, R, R_mag = nodal_reaction_forces(model, u, return_full_vector=full_vector)
    attach_point_data_by_node_id(model, prefix, R)
    attach_point_data_by_node_id(model, f"{prefix}_mag", R_mag)


def attach_element_stress_strain(model, u: Optional[np.ndarray] = None, *, reduce: REDUCE = "mean", prefix_stress: str = "S", prefix_strain: str = "E") -> None:
    eids, eps_e, sig_e, yld = element_reduced_results(model, u, reduce=reduce)
    attach_cell_data_by_element_id(model, prefix_strain, _dict_from_ids_values(eids, eps_e))
    attach_cell_data_by_element_id(model, prefix_stress, _dict_from_ids_values(eids, sig_e))
    attach_cell_data_by_element_id(model, "yielded", _dict_from_ids_values(eids, yld.astype(float)))


def attach_element_von_mises(model, u: Optional[np.ndarray] = None, *, reduce: REDUCE = "mean", name: str = "S_vm") -> None:
    eids, vm = element_von_mises(model, u, reduce=reduce)
    attach_cell_data_by_element_id(model, name, _dict_from_ids_values(eids, vm))


def attach_element_principal_stresses(model, u: Optional[np.ndarray] = None, *, reduce: REDUCE = "mean", name: str = "S_principal") -> None:
    eids, ps = element_principal_stresses(model, u, reduce=reduce)
    attach_cell_data_by_element_id(model, name, _dict_from_ids_values(eids, ps))


def attach_element_strain_energy(model, u: Optional[np.ndarray] = None, *, reduce: REDUCE = "mean", name_density: str = "W_density", name_total: str = "W_element") -> None:
    eids, w_den, w_elem = element_strain_energy(model, u, reduce=reduce)
    attach_cell_data_by_element_id(model, name_density, _dict_from_ids_values(eids, w_den))
    attach_cell_data_by_element_id(model, name_total, _dict_from_ids_values(eids, w_elem))




# -----------------------------
# Convenience: split Voigt vectors into named scalar components
# -----------------------------

_VOIGT_SUFFIXES = ("xx", "yy", "zz", "xy", "yz", "xz")


def attach_element_voigt_components(model, base_name: str, *, prefix: Optional[str] = None) -> None:
    """
    If you already attached a (n_cells,6) array to cell_data[base_name],
    this helper creates 6 scalar cell arrays:
      {prefix or base_name}_{xx,yy,zz,xy,yz,xz}

    Example:
      attach_element_stress_strain(model)  # creates cell_data["S"]
      attach_element_voigt_components(model, "S")  # creates S_xx, S_yy, ...
    """
    out_prefix = prefix if prefix is not None else base_name
    for comp in model.components:
        mesh = comp.mesh
        if base_name not in mesh.cell_data:
            continue
        V = np.asarray(mesh.cell_data[base_name], dtype=float)
        if V.ndim != 2 or V.shape[1] != 6:
            raise ValueError(f"{base_name} must be a (n_cells, 6) array; got {V.shape}")
        for j, suf in enumerate(_VOIGT_SUFFIXES):
            mesh.cell_data[f"{out_prefix}_{suf}"] = V[:, j]


def attach_nodal_vector_components(model, base_name: str, *, prefix: Optional[str] = None) -> None:
    """
    If you already attached a (n_points,3) array to point_data[base_name],
    this helper creates 3 scalar point arrays:
      {prefix or base_name}_{x,y,z}
    """
    out_prefix = prefix if prefix is not None else base_name
    for comp in model.components:
        mesh = comp.mesh
        if base_name not in mesh.point_data:
            continue
        V = np.asarray(mesh.point_data[base_name], dtype=float)
        if V.ndim != 2 or V.shape[1] != 3:
            raise ValueError(f"{base_name} must be a (n_points, 3) array; got {V.shape}")
        mesh.point_data[f"{out_prefix}_x"] = V[:, 0]
        mesh.point_data[f"{out_prefix}_y"] = V[:, 1]
        mesh.point_data[f"{out_prefix}_z"] = V[:, 2]


# -----------------------------
# Plotting (PyVista)
# -----------------------------

def plot_on_components(
    model,
    *,
    scalars: Optional[str] = None,
    vectors: Optional[str] = None,
    association: Literal["point", "cell"] = "cell",

    # Deformation / warping (visualization only)
    # Backward compatible: if you already pass warp_by/warp_factor, it still works.
    deformation_scale: Optional[float] = None,
    deformation_field: str = "U",
    warp_by: Optional[str] = None,
    warp_factor: float = 1.0,

    component_ids: Optional[Sequence[int]] = None,
    show_edges: bool = False,
):
    """
    Generic plotter:
      - scalars: name in point_data or cell_data (according to association)
      - vectors: optional vector field name for glyphing (point_data)
      - warp_by: vector field name (point_data) to warp geometry (typical: "U")
    """
    import pyvista as pv  # local import

    pl = pv.Plotter()
    comps = model.components
    if component_ids is not None:
        component_ids = set(int(c) for c in component_ids)
        comps = [c for c in comps if int(c.component_id) in component_ids]

    for comp in comps:
        if deformation_scale is not None:
            warp_by = deformation_field
            warp_factor = float(deformation_scale)

            mesh = comp.mesh
            m = mesh.copy(deep=True)

            if warp_by is not None:
                if warp_by not in m.point_data:
                    raise KeyError(f"warp_by='{warp_by}' not found in point_data of component {comp.component_id}")
                m = m.warp_by_vector(warp_by, factor=float(warp_factor))

            kwargs = {"show_edges": bool(show_edges)}
            if scalars is not None:
                kwargs["scalars"] = scalars

            pl.add_mesh(m, **kwargs)

            if vectors is not None:
                if vectors not in m.point_data:
                    raise KeyError(f"vectors='{vectors}' not found in point_data of component {comp.component_id}")
                glyphs = m.glyph(orient=vectors, scale=False, factor=1.0)
                pl.add_mesh(glyphs)

    pl.show()
    return pl


def compute_and_plot(
    model,
    field: str,
    *,
    reduce: REDUCE = "mean",

    # Visualization deformation scale (alias of warp_factor)
    deformation_scale: Optional[float] = None,
    warp_factor: float = 1.0,

    show_edges: bool = False,
):
    """
    Convenience: compute common fields, attach to meshes, plot.

    Supported `field` examples:
      - "U_mag", "R_mag"
      - "S_vm"
      - "W_density", "W_element"
      - "S_principal" (vector with 3 components)
      - "S" or "E" (full Voigt vectors; you can then plot components manually)
    """
    # Always attach displacements first (useful for warping)
    attach_nodal_displacements(model, prefix="U")
    if deformation_scale is not None:
        warp_factor = float(deformation_scale)

    # Allow scalar component selections like "S_xx", "E_xy", "U_z", "R_mag", ...
    if "_" in field:
        base, suf = field.split("_", 1)
        if base in ("S", "E"):
            attach_element_stress_strain(model, reduce=reduce, prefix_stress="S", prefix_strain="E")
            attach_element_voigt_components(model, base)
            assoc = "cell"
            return plot_on_components(model, scalars=field, association=assoc, warp_by="U", warp_factor=warp_factor, show_edges=show_edges)
        if base in ("U", "R"):
            if base == "U":
                attach_nodal_displacements(model, prefix="U")
            else:
                attach_nodal_reactions(model, prefix="R")
            attach_nodal_vector_components(model, base)
            assoc = "point"
            return plot_on_components(model, scalars=field, association=assoc, warp_by="U", warp_factor=warp_factor, show_edges=show_edges)

    # Field-specific attach
    if field in ("R", "R_mag"):
        attach_nodal_reactions(model, prefix="R")
        assoc = "point"
    elif field in ("U", "U_mag"):
        assoc = "point"
    elif field in ("S", "E", "yielded"):
        attach_element_stress_strain(model, reduce=reduce, prefix_stress="S", prefix_strain="E")
        assoc = "cell"
    elif field == "S_vm":
        attach_element_von_mises(model, reduce=reduce, name="S_vm")
        assoc = "cell"
    elif field == "S_principal":
        attach_element_principal_stresses(model, reduce=reduce, name="S_principal")
        assoc = "cell"
    elif field in ("W_density", "W_element"):
        attach_element_strain_energy(model, reduce=reduce, name_density="W_density", name_total="W_element")
        assoc = "cell"
    else:
        raise ValueError(f"Unknown field '{field}'. Add a mapping in compute_and_plot().")

    return plot_on_components(
        model,
        scalars=field,
        association=assoc,
        warp_by="U",
        warp_factor=warp_factor,
        show_edges=show_edges,
    )
