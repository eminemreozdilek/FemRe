import numpy as np
import sympy as sp
import pyvista as pv
from scipy.interpolate import RegularGridInterpolator
from stl import mesh as npstl_mesh
from scipy.interpolate import RBFInterpolator, interp1d

SYMBOLIC_X, SYMBOLIC_Y, SYMBOLIC_Z = sp.symbols('x y z')


def _symmetry_scores(mask3d: np.ndarray) -> dict:
    sx = float(np.mean(np.abs(mask3d - mask3d[::-1, :, :])))
    sy = float(np.mean(np.abs(mask3d - mask3d[:, ::-1, :])))
    sz = float(np.mean(np.abs(mask3d - mask3d[:, :, ::-1])))
    return {"x": sx, "y": sy, "z": sz}


def _cell_center_axes(Lx, Ly, Lz, Nx, Ny, Nz):
    dx = Lx / Nx;
    dy = Ly / Ny;
    dz = Lz / Nz
    xc = (np.arange(Nx, dtype=float) + 0.5) * dx
    yc = (np.arange(Ny, dtype=float) + 0.5) * dy
    zc = (np.arange(Nz, dtype=float) + 0.5) * dz
    return (xc, yc, zc), (dx, dy, dz)


def _evaluate_periodic_field(
        f_func,
        X,
        Y,
        Z,
        *,
        k: float | None = None,
        network_phase: bool = False,
        phase_shift: float = np.pi,
):
    if k is not None:
        Xs = k * X
        Ys = k * Y
        Zs = k * Z
    else:
        Xs, Ys, Zs = X, Y, Z

    if network_phase:
        return f_func(Xs + phase_shift, Ys + phase_shift, Zs + phase_shift)
    else:
        return f_func(Xs, Ys, Zs)


def _grid_from_nodes(origin, spacing, dims):
    g = pv.ImageData()
    g.origin = origin
    g.spacing = spacing
    g.dimensions = dims
    return g


def calculate_lambdified_formula(expr: sp.Expr) -> callable:
    return sp.lambdify((SYMBOLIC_X, SYMBOLIC_Y, SYMBOLIC_Z), expr, modules='numpy')


def convert_numpy_stl_to_pyvista(stl_mesh: npstl_mesh.Mesh) -> pv.PolyData:
    vectors = stl_mesh.vectors
    tri_verts = vectors.reshape(-1, 3)

    verts, inverse_idx = np.unique(tri_verts, axis=0, return_inverse=True)
    faces = inverse_idx.reshape(-1, 3)

    faces_pv = np.c_[np.full(len(faces), 3), faces].ravel()
    return pv.PolyData(verts, faces_pv)


def convert_pyvista_to_numpy_stl(polydata_mesh: pv.PolyData) -> npstl_mesh.Mesh:
    triangulated_mesh = polydata_mesh.triangulate()
    faces = triangulated_mesh.faces.reshape(-1, 4)[:, 1:]
    vectors = triangulated_mesh.points[faces]
    stl = npstl_mesh.Mesh(np.zeros(vectors.shape[0], dtype=npstl_mesh.Mesh.dtype))
    stl.vectors[:] = vectors
    return stl


def extract_isosurface_mesh(
        total_structure_size: tuple[float, float, float],
        unit_cell_size: float,
        formula_str: str,
        resolution: int = 50,
        isovalue: float = 0.0,
        sample: str = "nodes",
) -> pv.PolyData:
    expr = sp.sympify(formula_str)
    f_func = calculate_lambdified_formula(expr)

    Lx, Ly, Lz = map(float, total_structure_size)
    Nx = max(int(np.ceil((Lx / unit_cell_size) * resolution)), 1)
    Ny = max(int(np.ceil((Ly / unit_cell_size) * resolution)), 1)
    Nz = max(int(np.ceil((Lz / unit_cell_size) * resolution)), 1)

    k = 2.0 * np.pi / float(unit_cell_size)

    if sample == "centers":
        # sample at cell centers, then C2P for contour
        (xc, yc, zc), (dx, dy, dz) = _cell_center_axes(Lx, Ly, Lz, Nx, Ny, Nz)
        Xc, Yc, Zc = np.meshgrid(xc, yc, zc, indexing='ij')
        vals = f_func(k * Xc, k * Yc, k * Zc).astype(np.float32, copy=False)

        grid = _grid_from_nodes(origin=(0, 0, 0),
                                spacing=(dx, dy, dz),
                                dims=(Nx + 1, Ny + 1, Nz + 1))
        grid.cell_data["values"] = vals.ravel(order="F")
        grid = grid.cell_data_to_point_data()  # interpolate centers -> nodes

    else:  # "nodes" (original)
        xs = np.linspace(0.0, Lx, Nx + 1, dtype=np.float32)
        ys = np.linspace(0.0, Ly, Ny + 1, dtype=np.float32)
        zs = np.linspace(0.0, Lz, Nz + 1, dtype=np.float32)
        X, Y, Z = np.meshgrid(xs, ys, zs, indexing='ij')
        vals = f_func(k * X, k * Y, k * Z).astype(np.float32, copy=False)

        grid = _grid_from_nodes(origin=(0, 0, 0),
                                spacing=(Lx / Nx, Ly / Ny, Lz / Nz),
                                dims=(Nx + 1, Ny + 1, Nz + 1))
        grid.point_data["values"] = vals.ravel(order="F")

    mesh = grid.contour(isosurfaces=[isovalue], scalars="values").triangulate()
    mesh.clear_data()
    mesh.active_scalars_name = None
    return mesh


def extract_volumetric_lattice_mesh(
        total_structure_size: tuple[float, float, float],
        unit_cell_size: float,
        formula_str: str,
        thickness,
        resolution: int = 50,
        network_phase: bool = False,
        grading: bool = False,
        sample: str = "nodes",
) -> pv.PolyData:
    expr = sp.sympify(formula_str)
    f_func = calculate_lambdified_formula(expr)

    Lx, Ly, Lz = map(float, total_structure_size)
    Nx = max(int(np.ceil((Lx / unit_cell_size) * resolution)), 1)
    Ny = max(int(np.ceil((Ly / unit_cell_size) * resolution)), 1)
    Nz = max(int(np.ceil((Lz / unit_cell_size) * resolution)), 1)
    k = 2.0 * np.pi / float(unit_cell_size)

    if sample == "centers":
        (xc, yc, zc), (dx, dy, dz) = _cell_center_axes(Lx, Ly, Lz, Nx, Ny, Nz)
        Xc, Yc, Zc = np.meshgrid(xc, yc, zc, indexing="ij")

        base = _evaluate_periodic_field(
            f_func, Xc, Yc, Zc, k=k, network_phase=network_phase
        ).astype(np.float32, copy=False)

        if grading:
            tgrid = np.asarray(thickness(Xc, Yc, Zc), dtype=np.float32)
        else:
            t = np.asarray(thickness, dtype=np.float32)
            tgrid = t if t.ndim else np.broadcast_to(t, base.shape).astype(np.float32, copy=False)

        field = (tgrid * 0.5 - base) if network_phase else (np.abs(base) - tgrid * 0.5)
        eps = 1e-5
        outside = (Xc < eps) | (Xc > Lx - eps) | (Yc < eps) | (Yc > Ly - eps) | (Zc < eps) | (Zc > Lz - eps)
        field[outside] = 1.0

        grid = _grid_from_nodes((0, 0, 0), (dx, dy, dz), (Nx + 1, Ny + 1, Nz + 1))
        grid.cell_data["values"] = field.ravel(order="F")
        grid = grid.cell_data_to_point_data()

    else:
        xs = np.linspace(0.0, Lx, Nx + 1, dtype=np.float32)
        ys = np.linspace(0.0, Ly, Ny + 1, dtype=np.float32)
        zs = np.linspace(0.0, Lz, Nz + 1, dtype=np.float32)
        X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")

        base = _evaluate_periodic_field(
            f_func, X, Y, Z, k=k, network_phase=network_phase
        ).astype(np.float32, copy=False)

        if grading:
            tgrid = np.asarray(thickness(X, Y, Z), dtype=np.float32)
        else:
            t = np.asarray(thickness, dtype=np.float32)
            tgrid = t if t.ndim else np.broadcast_to(t, base.shape).astype(np.float32, copy=False)

        field = (tgrid * 0.5 - base) if network_phase else (np.abs(base) - tgrid * 0.5)
        eps = 1e-5
        outside = (X < eps) | (X > Lx - eps) | (Y < eps) | (Y > Ly - eps) | (Z < eps) | (Z > Lz - eps)
        field[outside] = 1.0

        grid = _grid_from_nodes((0, 0, 0), (Lx / Nx, Ly / Ny, Lz / Nz), (Nx + 1, Ny + 1, Nz + 1))
        grid.point_data["values"] = field.ravel(order="F")

    mesh = grid.contour(isosurfaces=[0.0], scalars="values").clean().triangulate()
    mesh.clear_data()
    mesh.active_scalars_name = None
    return mesh


def generate_voxel_mesh(voxel_array: np.ndarray, repeats=(1,1,1), scale=1.0):
    nx, ny, nz = voxel_array.shape
    grid = pv.ImageData(dimensions=(nx + 1, ny + 1, nz + 1))
    grid.cell_data["active_voxels"] = voxel_array.flatten(order="F")
    hex_mesh = grid.threshold([0.9, 1.1])
    hex_mesh.clear_data()
    hex_mesh.active_scalars_name = None
    grid.points = scale /np.max(grid.points)
    return convert_voxel_to_hex_numpy(hex_mesh)

def convert_voxel_to_hex_numpy(mesh: pv.UnstructuredGrid) -> pv.UnstructuredGrid:
    cells = np.asarray(mesh.cells)
    cells_2d = cells.reshape(-1, 9)
    conn = cells_2d[:, 1:9]
    hex_conn = conn[:, [0, 1, 3, 2, 4, 5, 7, 6]]

    new_cells = np.hstack(
        [np.full((hex_conn.shape[0], 1), 8, dtype=cells.dtype), hex_conn]).ravel()

    new_celltypes = np.full(mesh.n_cells, pv.CellType.HEXAHEDRON, dtype=mesh.celltypes.dtype)
    new_mesh = pv.UnstructuredGrid(new_cells, new_celltypes, mesh.points.copy())

    for key in mesh.point_data:
        new_mesh.point_data[key] = mesh.point_data[key].copy()

    for key in mesh.cell_data:
        new_mesh.cell_data[key] = mesh.cell_data[key].copy()
    return new_mesh

def calculate_thickness(
        formula_str: str,
        target_vf: float,
        resolution: int,
        network_phase: bool = False,
        boundaries: tuple[float, float] = (0, 2 * np.pi),
        atol: float = 1e-3,
        rtol: float = 1e-3,
        max_iter: int = 200,
) -> tuple[float, np.ndarray]:
    f_func = calculate_lambdified_formula(sp.sympify(formula_str))

    lower_boundary, upper_boundary = boundaries
    coords = np.linspace(lower_boundary, upper_boundary, resolution)
    grid_X, grid_Y, grid_Z = np.meshgrid(coords, coords, coords, indexing="ij")

    field_values = np.asarray(
        _evaluate_periodic_field(f_func, grid_X, grid_Y, grid_Z, k=None, network_phase=network_phase))

    max_val = float(np.max(np.abs(field_values)))
    if not np.isfinite(max_val):
        raise ValueError("Field has non-finite values; check your formula/grid.")

    def vf_for_t(t: float) -> float:
        if network_phase:
            mask = field_values > (t / 2.0)
        else:
            mask = np.abs(field_values) <= (t / 2.0)
        return float(mask.sum()) / mask.size

    if not (0.0 < target_vf < 1.0):
        if target_vf == 0.0:
            target_vf = 1 / resolution ** 3
        elif target_vf == 1.0:
            target_vf = 1.0 - 1 / resolution ** 3
        else:
            raise ValueError(f"target_vf must be in (0,1), got {target_vf}")

    if not network_phase:
        v0 = vf_for_t(0.0)
        if target_vf < v0 - 1e-12:
            return v0, np.zeros((resolution, resolution, resolution))

    T = 10.0 * max_val if max_val > 0 else 1.0
    t_lo, t_hi = (-T, T) if network_phase else (0.0, T)

    v_lo, v_hi = vf_for_t(t_lo), vf_for_t(t_hi)

    def close(a, b):
        return np.isclose(a, b, atol=atol, rtol=rtol)

    if close(v_lo, target_vf):
        t_star = t_lo
        mask = (field_values > (t_star / 2.0)) if network_phase else (np.abs(field_values) <= (t_star / 2.0))
        return float(t_star), mask.astype(np.int32)
    if close(v_hi, target_vf):
        t_star = t_hi
        mask = (field_values > (t_star / 2.0)) if network_phase else (np.abs(field_values) <= (t_star / 2.0))
        return float(t_star), mask.astype(np.int32)

    decreasing = network_phase

    for _ in range(max_iter):
        t_mid = 0.5 * (t_lo + t_hi)
        v_mid = vf_for_t(t_mid)

        if close(v_mid, target_vf) or (abs(t_hi - t_lo) <= max(1e-12, 1e-6 * max(1.0, abs(t_mid)))):
            t_star = t_mid
            mask = (field_values > (t_star / 2.0)) if network_phase else (np.abs(field_values) <= (t_star / 2.0))
            return float(t_star), mask.astype(np.int32)

        if decreasing:
            if v_mid < target_vf:
                t_hi = t_mid
            else:
                t_lo = t_mid
        else:
            if v_mid < target_vf:
                t_lo = t_mid
            else:
                t_hi = t_mid

    t_star = 0.5 * (t_lo + t_hi)
    mask = (field_values > (t_star / 2.0)) if network_phase else (np.abs(field_values) <= (t_star / 2.0))
    return float(t_star), mask.astype(np.int32)


def fill_structure_with_lattice(
        stl_mesh,
        unit_cell_size: float,
        formula_str: str,
        thickness,
        resolution: int = 30,
        network_phase: bool = False,
        grading: bool = False,
        oversample: float = 1.0,
        sample: str = "nodes",  # NEW
) -> pv.PolyData:
    if isinstance(stl_mesh, pv.PolyData):
        solid_polydata = stl_mesh
    else:
        solid_polydata = convert_numpy_stl_to_pyvista(stl_mesh)
    if not solid_polydata.is_all_triangles:
        solid_polydata = solid_polydata.triangulate()
    if solid_polydata.n_faces_strict == 0:
        raise ValueError("Input surface has no faces.")

    xmin, xmax, ymin, ymax, zmin, zmax = solid_polydata.bounds
    bb_min = np.array([xmin, ymin, zmin], float)
    bb_max = np.array([xmax, ymax, zmax], float)
    Lx, Ly, Lz = (bb_max - bb_min).astype(float)

    repeats = np.array([Lx, Ly, Lz]) / float(unit_cell_size)
    Nc = np.ceil(repeats * resolution).astype(int).clip(min=2)
    dims = np.maximum((Nc.astype(float) * float(oversample)).astype(int), 2)
    Nx, Ny, Nz = dims.tolist()

    expr = sp.sympify(formula_str)
    f_func = calculate_lambdified_formula(expr)
    k = 2.0 * np.pi / float(unit_cell_size)

    if sample == "centers":
        (xc, yc, zc), (dx, dy, dz) = _cell_center_axes(Lx, Ly, Lz, Nx, Ny, Nz)
        Xc, Yc, Zc = np.meshgrid(xc + bb_min[0], yc + bb_min[1], zc + bb_min[2], indexing='ij')

        base = _evaluate_periodic_field(
            f_func,
            Xc - bb_min[0],
            Yc - bb_min[1],
            Zc - bb_min[2],
            k=k,
            network_phase=network_phase,
        )

        if grading:
            tgrid = thickness(Xc, Yc, Zc)
        else:
            t = float(thickness)
            tgrid = t

        field = (tgrid / 2.0 - base) if network_phase else (np.abs(base) - tgrid / 2.0)

        pts = np.column_stack([Xc.ravel(order='F'), Yc.ravel(order='F'), Zc.ravel(order='F')])
        inside = pv.PolyData(pts).select_enclosed_points(solid_polydata, tolerance=0.0, check_surface=True)
        in_mask = inside.point_data['SelectedPoints'].astype(bool).reshape((Nx, Ny, Nz), order='F')
        field = np.where(in_mask, field, 1.0)  # positive outside

        grid = _grid_from_nodes(origin=(bb_min[0], bb_min[1], bb_min[2]),
                                spacing=(dx, dy, dz),
                                dims=(Nx + 1, Ny + 1, Nz + 1))
        grid.cell_data["values"] = field.astype(float).ravel(order='F')
        grid = grid.cell_data_to_point_data()

    else:
        xs = np.linspace(bb_min[0], bb_max[0], Nx, dtype=np.float32)
        ys = np.linspace(bb_min[1], bb_max[1], Ny, dtype=np.float32)
        zs = np.linspace(bb_min[2], bb_max[2], Nz, dtype=np.float32)
        X, Y, Z = np.meshgrid(xs, ys, zs, indexing='ij')

        base = _evaluate_periodic_field(f_func, X - bb_min[0], Y - bb_min[1], Z - bb_min[2], k=k,
                                        network_phase=network_phase, )

        tgrid = thickness(X, Y, Z) if grading else float(thickness)
        field = (tgrid / 2.0 - base) if network_phase else (np.abs(base) - tgrid / 2.0)

        grid = _grid_from_nodes(origin=(bb_min[0], bb_min[1], bb_min[2]),
                                spacing=(Lx / max(Nx - 1, 1), Ly / max(Ny - 1, 1), Lz / max(Nz - 1, 1)),
                                dims=(Nx, Ny, Nz))
        grid.point_data['values'] = field.astype(float).ravel(order='F')

    surface = grid.contour(isosurfaces=[0.0], scalars='values').clean().triangulate()
    surface.clear_data()
    surface.active_scalars_name = None
    return surface


def calculate_thickness_interpolator(lattice_formula, resolution_of_reconstruction, lattice_phase):
    volume_fraction_array = np.linspace(0, 1, 11)
    thickness_array = [
        calculate_thickness(
            lattice_formula, volume_fraction,
            resolution=resolution_of_reconstruction,
            network_phase=lattice_phase == "Network"
        )[0]
        for volume_fraction in volume_fraction_array
    ]
    return interp1d(volume_fraction_array, thickness_array, kind='cubic', fill_value='extrapolate')


def calculate_volume_fraction_mapper(points_1d, values_3d, eppe: int, tol: float = 1e-9):
    x1d, y1d, z1d = points_1d

    # for name, a in (("x", x1d), ("y", y1d), ("z", z1d)):
    #     if a.ndim != 1:
    #         raise ValueError(f"{name}-axis must be 1D; got shape {a.shape}")
    #     if not np.all(np.diff(a) > 0):
    #         raise ValueError(f"{name}-axis must be strictly increasing")

    expected = (x1d.size, y1d.size, z1d.size)
    if values_3d.shape != expected:
        raise ValueError(f"values_3d shape {values_3d.shape} must equal {expected}")

    vf_interp = RegularGridInterpolator(
        (x1d, y1d, z1d), values_3d, method="linear",
        bounds_error=False, fill_value=np.nan
    )

    ny = y1d.size - 1
    k = min(max(eppe, 0), ny)
    if k == 0:
        def coord_to_vf(coords, Y=None, Z=None):
            if Y is None and Z is None:
                pts = np.asarray(coords, float)
                if pts.ndim == 1: pts = pts[None, :]
                return vf_interp(pts)
            X = np.asarray(coords, float)
            Y = np.asarray(Y, float)
            Z = np.asarray(Z, float)
            pts = np.column_stack([X.ravel(order='F'), Y.ravel(order='F'), Z.ravel(order='F')])
            field_values = vf_interp(pts)
            return field_values.reshape(X.shape, order='F')

        return coord_to_vf

    y_bot_max = y1d[k]
    y_top_min = y1d[-(k + 1)]

    def _map_points(pts):
        pts = np.asarray(pts, float)
        squeeze = False
        if pts.ndim == 1:
            pts = pts[None, :]
            squeeze = True

        eps = np.finfo(float).eps * max(1.0, abs(y1d[-1] - y1d[0]))
        pts[:, 0] = np.clip(pts[:, 0], x1d[0], x1d[-1])
        pts[:, 1] = np.clip(pts[:, 1], y1d[0] - eps, y1d[-1] + eps)
        pts[:, 2] = np.clip(pts[:, 2], z1d[0], z1d[-1])

        yq = pts[:, 1]
        in_bottom_band = yq <= y_bot_max + tol
        in_top_band = yq >= y_top_min - tol
        in_band = in_bottom_band | in_top_band

        out = np.empty(pts.shape[0], float)
        out[in_band] = 1.0
        if np.any(~in_band):
            out[~in_band] = vf_interp(pts[~in_band])
        return out[0] if squeeze else out

    def coord_to_vf(coords, Y=None, Z=None):
        if Y is None and Z is None:
            return _map_points(coords)
        X = np.asarray(coords, float)
        Y = np.asarray(Y, float)
        Z = np.asarray(Z, float)
        pts = np.column_stack([X.ravel(order='F'), Y.ravel(order='F'), Z.ravel(order='F')])
        field_values = _map_points(pts)
        return field_values.reshape(X.shape, order='F')

    return coord_to_vf


def build_y_heights(ny: int, eppe: int, t: float, interior_height: float = 10.0) -> np.ndarray:
    if ny <= 0:
        raise ValueError("ny must be positive")
    y_heights = np.full(ny, float(interior_height), dtype=float)
    k = min(eppe, ny)
    if k > 0:
        y_heights[:k] = float(t)
        y_heights[-k:] = float(t)
    return y_heights


def calculate_node_values_from_cell_values(volume_fraction: np.ndarray) -> np.ndarray:
    count_x, count_y, count_z = volume_fraction.shape
    node = np.zeros((count_x + 1, count_y + 1, count_z + 1), dtype=float)
    cnt = np.zeros_like(node, dtype=int)

    for i in range(count_x):
        for j in range(count_y):
            for k in range(count_z):
                node[i:i + 2, j:j + 2, k:k + 2] += volume_fraction[i, j, k]
                cnt[i:i + 2, j:j + 2, k:k + 2] += 1

    cnt = np.maximum(cnt, 1)
    return node / cnt


def reconstruct(lattice_formula,
                resolution,
                phase: bool,
                element_densities,
                mesh_density,
                size,
                element_per_plate,
                thickness_of_plate,
                unit_cell_size,
                symetric: bool = False):
    voxel_size = unit_cell_size / mesh_density

    if element_per_plate is None or thickness_of_plate is None:
        element_per_plate = 0
        thickness_of_plate = 0.0

    element_densities = np.transpose(
        np.reshape(
            element_densities,
            (
                round(size[1] * mesh_density) + element_per_plate * 2,
                round(size[0] * mesh_density),
                round(size[2] * mesh_density),
            ), order="F", ), (1, 0, 2), )[:, ::-1, :]

    if symetric:
        element_densities = np.concatenate((element_densities, element_densities[::-1, :, :]), axis=0)
    count_x, count_y, count_z = element_densities.shape
    x = np.arange(count_x + 1, dtype=float) * voxel_size
    z = np.arange(count_z + 1, dtype=float) * voxel_size
    y_heights = build_y_heights(count_y, element_per_plate, thickness_of_plate, interior_height=voxel_size)
    y = np.concatenate(([0.0], np.cumsum(y_heights)))

    grid_nodes_X, grid_nodes_Y, grid_nodes_Z = np.meshgrid(x, y, z, indexing="ij")
    structured_grid = pv.StructuredGrid(grid_nodes_X, grid_nodes_Y, grid_nodes_Z)
    unstructured_grid = structured_grid.cast_to_unstructured_grid()
    unstructured_grid.cell_data["values"] = element_densities.ravel(order="F")

    node_vals = calculate_node_values_from_cell_values(element_densities)
    if phase:
        phase_str = "Network"
    else:
        phase_str = "Matrix"
    thickness_from_volume_fraction = calculate_thickness_interpolator(lattice_formula, resolution, phase_str)
    volume_fraction_mapper = calculate_volume_fraction_mapper((x, y, z), node_vals, eppe=element_per_plate)

    def calculate_thickness_at(coords_or_X, Y=None, Z=None):
        if Y is None and Z is None:
            return thickness_from_volume_fraction(volume_fraction_mapper(coords_or_X))
        return thickness_from_volume_fraction(volume_fraction_mapper(coords_or_X, Y, Z))

    unstructured_grid.point_data["values_point_avg"] = node_vals.ravel(order="F")
    size_x, size_y, size_z = x[-1], y[-1], z[-1]
    reconstructed_mesh = extract_volumetric_lattice_mesh(
        total_structure_size=(size_x, size_y, size_z),
        unit_cell_size=unit_cell_size,
        formula_str=lattice_formula,
        thickness=calculate_thickness_at,
        resolution=resolution,
        network_phase=phase,
        grading=True,
    )
    return reconstructed_mesh
