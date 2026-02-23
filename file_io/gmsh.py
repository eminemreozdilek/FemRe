import os
import tempfile
from typing import Optional, Tuple

import numpy as np
import pyvista as pv
import gmsh
import vtk

VTK_TO_GMSH_LINEAR: dict[int, tuple[int, int]] = {
    # 1D
    3: (1, 2),  # VTK_LINE -> line2
    21: (1, 2),  # VTK_QUADRATIC_EDGE -> line2 (drop mid-node)

    # 2D
    5: (2, 3),  # VTK_TRIANGLE -> tri3
    22: (2, 3),  # VTK_QUADRATIC_TRIANGLE -> tri3
    9: (3, 4),  # VTK_QUAD -> quad4
    23: (3, 4),  # VTK_QUADRATIC_QUAD -> quad4
    28: (3, 4),  # VTK_BIQUADRATIC_QUAD -> quad4

    # 3D
    10: (4, 4),  # VTK_TETRA -> tet4
    24: (4, 4),  # VTK_QUADRATIC_TETRA -> tet4
    12: (5, 8),  # VTK_HEXAHEDRON -> hex8
    29: (5, 8),  # VTK_TRIQUADRATIC_HEXAHEDRON (27 nodes) -> hex8
    13: (6, 6),  # VTK_WEDGE -> prism6
    26: (6, 6),  # VTK_QUADRATIC_WEDGE -> prism6
    14: (7, 5),  # VTK_PYRAMID -> pyramid5
    27: (7, 5),  # VTK_QUADRATIC_PYRAMID -> pyramid5
}


def _split_unstructured_by_dimension(
        grid: pv.UnstructuredGrid,
) -> Tuple[Optional[pv.UnstructuredGrid], Optional[pv.UnstructuredGrid], Optional[pv.UnstructuredGrid]]:
    """
    Split a mixed-dimension UnstructuredGrid into 1D / 2D / 3D UnstructuredGrids.

    Dimensions are computed from VTK cell type using vtkCellTypes.GetDimension().
    Each output mesh shares the same points array as the input grid (no node
    renumbering is done; some points may be unused in a given submesh).
    """
    if not isinstance(grid, pv.UnstructuredGrid):
        grid = grid.cast_to_unstructured_grid()

    celltypes = np.asarray(grid.celltypes, dtype=np.uint8)
    n_cells = grid.n_cells
    cells = np.asarray(grid.cells, dtype=np.int64)

    # Compute cell offsets in the legacy VTK "cells" array:
    # [n0, i0_0, ..., i0_n0-1, n1, i1_0, ..., ...]
    offsets = np.empty(n_cells, dtype=np.int64)
    cursor = 0
    for i in range(n_cells):
        offsets[i] = cursor
        npts = int(cells[cursor])
        cursor += 1 + npts

    # Dimension of each cell via VTK
    dims = np.array(
        [vtk.vtkCellTypes.GetDimension(int(ct)) for ct in celltypes],
        dtype=np.int64,
    )

    result = {}
    for dim in (1, 2, 3):
        mask = np.where(dims == dim)[0]
        if mask.size == 0:
            result[dim] = None
            continue

        new_cells_segments = []
        new_celltypes = []

        for cell_id in mask:
            start = offsets[cell_id]
            npts = int(cells[start])
            seg = cells[start: start + 1 + npts]
            new_cells_segments.append(seg)
            new_celltypes.append(celltypes[cell_id])

        new_cells = np.concatenate(new_cells_segments).astype(np.int64)
        new_celltypes = np.asarray(new_celltypes, dtype=np.uint8)

        subgrid = pv.UnstructuredGrid(new_cells, new_celltypes, grid.points.copy())
        result[dim] = subgrid

    return result.get(1), result.get(2), result.get(3)


def _gmsh_convert_msh_to_vtk(msh_filename: str) -> str:
    """
    Use gmsh to convert an input .msh file to a temporary .vtk file,
    and return the path to that .vtk file.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".vtk", delete=False)
    tmp_vtk = tmp.name
    tmp.close()

    gmsh.initialize()
    try:
        gmsh.open(msh_filename)
        gmsh.write(tmp_vtk)  # <- now extension is .vtk
    finally:
        gmsh.finalize()

    return tmp_vtk



def read_msh(
        filename: str,
) -> Tuple[Optional[pv.UnstructuredGrid], Optional[pv.UnstructuredGrid], Optional[pv.UnstructuredGrid]]:
    """
    Read a Gmsh .msh file and return separate PyVista UnstructuredGrids
    for 1D, 2D and 3D parts.

    Parameters
    ----------
    filename:
        Path to the .msh file (any Gmsh-supported version; gmsh will
        internally convert it to VTK XML UnstructuredGrid).

    Returns
    -------
    mesh_1d, mesh_2d, mesh_3d:
        Each is either a `pyvista.UnstructuredGrid` or `None` if no
        cells of that topological dimension are present.

    Notes
    -----
    * This uses gmsh to translate `.msh` -> `.vtu`, then reads the `.vtu`
      with pyvista.
    * All gmsh element types that gmsh can export to VTK end up supported
      here (including mixed and high-order cells).
    """
    tmp_vtu = _gmsh_convert_msh_to_vtk(filename)
    try:
        grid = pv.read(tmp_vtu).cast_to_unstructured_grid()
    finally:
        # Make best effort to remove the temporary file
        try:
            os.remove(tmp_vtu)
        except OSError:
            pass

    return _split_unstructured_by_dimension(grid)


def write_msh(
        filename: str,
        mesh_1D: Optional[pv.UnstructuredGrid] = None,
        mesh_2D: Optional[pv.UnstructuredGrid] = None,
        mesh_3D: Optional[pv.UnstructuredGrid] = None,
) -> None:
    """
    Write up to three PyVista UnstructuredGrids (1D/2D/3D) to a single
    Gmsh 2.2 ASCII .msh file.

    The meshes are assumed to use VTK cell types (as usual in pyvista).
    All nodes are renumbered globally from 1..N. Cells are written as
    *linear* Gmsh elements; any higher-order VTK cells are downgraded
    by keeping only the corner vertices.

    Parameters
    ----------
    filename:
        Target ".msh" path. Existing files will be overwritten.
    mesh_1D, mesh_2D, mesh_3D:
        Optional `pyvista.UnstructuredGrid` objects holding 1D / 2D / 3D
        cells. You can pass any subset; dimensions are only used to set
        a simple element tag (the first element tag is the topological
        dimension 1/2/3).

    Limitations
    -----------
    * High-order elements are converted to linear elements:
      - Quadratic lines, triangles, tets, hexes, etc. lose their
        mid-edge/mid-face nodes, but cell connectivity and topology
        are preserved.
    * Only common 1D/2D/3D shapes are handled (lines, tri/quad,
      tet/hex/wedge/pyramid). If an unsupported VTK cell type is
      encountered, a ValueError is raised.
    """
    # Collect meshes in (dim, grid) list, ignoring Nones
    dim_meshes: list[tuple[int, pv.UnstructuredGrid]] = []
    for dim, mesh in ((1, mesh_1D), (2, mesh_2D), (3, mesh_3D)):
        if mesh is None:
            continue
        if not isinstance(mesh, pv.UnstructuredGrid):
            mesh = mesh.cast_to_unstructured_grid()
        dim_meshes.append((dim, mesh))

    if not dim_meshes:
        raise ValueError("No meshes provided to write_msh().")

    # ------------------------------------------------------------------
    # Assign global node IDs
    # ------------------------------------------------------------------
    # For simplicity we just concatenate the point arrays of each mesh
    # and give unique node IDs; we do NOT attempt to detect shared
    # coordinates across dimensions.
    coords: list[tuple[float, float, float]] = []
    mesh_point_to_node: dict[int, np.ndarray] = {}
    next_node_id = 1

    for _, grid in dim_meshes:
        n_pts = grid.number_of_points
        local_to_global = np.empty(n_pts, dtype=np.int64)
        for i, p in enumerate(grid.points):
            x, y, z = float(p[0]), float(p[1]), float(p[2])
            coords.append((x, y, z))
            local_to_global[i] = next_node_id
            next_node_id += 1
        mesh_point_to_node[id(grid)] = local_to_global

    num_nodes = next_node_id - 1

    # ------------------------------------------------------------------
    # Build element records
    # ------------------------------------------------------------------
    # Each record: (elm_number, gmsh_type, dim, node_tags_list)
    elements: list[tuple[int, int, int, list[int]]] = []
    elm_number = 1

    for dim, grid in dim_meshes:
        cells = np.asarray(grid.cells, dtype=np.int64)
        celltypes = np.asarray(grid.celltypes, dtype=np.int64)
        n_cells = grid.n_cells

        local_to_global = mesh_point_to_node[id(grid)]

        # Parse legacy VTK cell layout
        cursor = 0
        for c in range(n_cells):
            npts = int(cells[cursor])
            conn_local = cells[cursor + 1: cursor + 1 + npts]
            cursor += 1 + npts

            vtk_type = int(celltypes[c])
            if vtk_type not in VTK_TO_GMSH_LINEAR:
                raise ValueError(
                    f"Unsupported VTK cell type {vtk_type} (dim={dim}). "
                    "Extend VTK_TO_GMSH_LINEAR if needed."
                )

            gmsh_type, n_corner = VTK_TO_GMSH_LINEAR[vtk_type]

            if n_corner > npts:
                raise ValueError(
                    f"Cell {c} has only {npts} points, but mapping "
                    f"expects {n_corner} corner vertices."
                )

            # Downgrade to linear by keeping only the first n_corner nodes
            conn_corner = conn_local[:n_corner]
            node_tags = [int(local_to_global[idx]) for idx in conn_corner]

            elements.append((elm_number, gmsh_type, dim, node_tags))
            elm_number += 1

    # ------------------------------------------------------------------
    # Write Gmsh 2.2 ASCII file
    # ------------------------------------------------------------------
    with open(filename, "w") as f:
        # MeshFormat
        f.write("$MeshFormat\n")
        # version 2.2, file-type 0 (ASCII), data-size 8 (size of double)
        f.write("2.2 0 8\n")
        f.write("$EndMeshFormat\n")

        # Nodes section
        f.write("$Nodes\n")
        f.write(f"{num_nodes}\n")
        for node_id, (x, y, z) in enumerate(coords, start=1):
            # Use high precision to avoid roundoff surprises
            f.write(f"{node_id} {x:.16g} {y:.16g} {z:.16g}\n")
        f.write("$EndNodes\n")

        # Elements section
        f.write("$Elements\n")
        f.write(f"{len(elements)}\n")

        # By convention: we write two tags per element:
        #   tag1 = topological dimension (1, 2 or 3)
        #   tag2 = same as tag1 (can be interpreted as "elementary entity")
        for elm_number, gmsh_type, dim, node_tags in elements:
            num_tags = 2
            tag1 = dim
            tag2 = dim
            nodes_str = " ".join(str(int(t)) for t in node_tags)
            f.write(f"{elm_number} {gmsh_type} {num_tags} {tag1} {tag2} {nodes_str}\n")

        f.write("$EndElements\n")
