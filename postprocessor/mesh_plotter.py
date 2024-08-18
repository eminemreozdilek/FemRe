import numpy as np
import pyvista as pv
import pandas as pd

import applications.application_static.model_storage as asms


def plot_mesh_static_case_mesh(data: asms.Storage, scale: float = 1.0):
    nodes = data.node_storage.data
    hexahedrons = data.element_brick_eight_storage.data
    tetrahedrons = data.element_tetra_four_storage.data

    node_coordinates = nodes[["X", "Y", "Z"]].values
    node_displacements = nodes[["DisplacementX", "DisplacementY", "DisplacementZ"]].values
    node_forces = nodes[["ForceX", "ForceY", "ForceZ"]].values
    node_ids = nodes["NodeID"].values

    result_displacements = nodes[["ResultDisplacementX", "ResultDisplacementY", "ResultDisplacementZ"]].values
    result_forces = nodes[["ResultForceX", "ResultForceY", "ResultForceZ"]].values
    node_restrictions = nodes[["RestX", "RestY", "RestZ"]].values

    new_coordinates = result_displacements * scale + node_coordinates

    tetrahedron_cells = tetrahedrons[["Node1", "Node2", "Node3", "Node4"]].values - 1
    tetrahedron_cells = np.hstack((np.full((tetrahedron_cells.shape[0], 1), 4), tetrahedron_cells)).astype(int)
    hexahedron_cells = hexahedrons[["Node1", "Node2", "Node3", "Node4", "Node5", "Node6", "Node7", "Node8"]].values - 1
    hexahedron_cells = np.hstack((np.full((hexahedron_cells.shape[0], 1), 8), hexahedron_cells)).astype(int)

    tetrahedron_cell_type = np.full(tetrahedron_cells.shape[0], pv.CellType.TETRA, dtype=np.uint8)
    hexahedron_cell_type = np.full(hexahedron_cells.shape[0], pv.CellType.HEXAHEDRON, dtype=np.uint8)
    tetrahedron_mesh = pv.UnstructuredGrid(tetrahedron_cells, tetrahedron_cell_type, new_coordinates)
    hexahedron_mesh = pv.UnstructuredGrid(hexahedron_cells, hexahedron_cell_type, new_coordinates)

    return ([tetrahedron_mesh, hexahedron_mesh],
            [tetrahedron_mesh.extract_all_edges(), hexahedron_mesh.extract_all_edges()])


def plot_points(data: asms.Storage, point_ids, scale: float = 1.0):
    mask = data.node_storage.data["NodeID"].isin(point_ids)
    coordinates = data.node_storage.data.loc[mask, ["X", "Y", "Z"]].values
    result_displacements = data.node_storage.data.loc[
        mask, ["ResultDisplacementX", "ResultDisplacementY", "ResultDisplacementX"]].values

    return pv.PolyData(result_displacements * scale + coordinates)


def plot_voxel_with_pyvista(voxel: np.ndarray, model_size: tuple = (1.0, 1.0, 1.0)):
    data = voxel
    ei = data.shape[0]
    ej = data.shape[1]
    ek = data.shape[2]

    ni = ei + 1
    nj = ej + 1
    nk = ek + 1

    si = model_size[0] / ei
    sj = model_size[1] / ej
    sk = model_size[2] / ek

    nodes = []
    for k in range(nk):
        for j in range(nj):
            for i in range(ni):
                nodes.append(
                    [i * si,
                     j * sj,
                     k * sk])
    nodes = np.array(nodes)

    elements = []
    for k in range(ek):
        for j in range(ej):
            for i in range(ei):
                if data[i, j, k] == 1:
                    elements += [8,
                                 i + j * ni + k * nj * ni,
                                 (i + 1) + j * ni + k * nj * ni,
                                 (i + 1) + (j + 1) * ni + k * nj * ni,
                                 i + (j + 1) * ni + k * nj * ni,
                                 i + j * ni + (k + 1) * nj * ni,
                                 (i + 1) + j * ni + (k + 1) * nj * ni,
                                 (i + 1) + (j + 1) * ni + (k + 1) * nj * ni,
                                 i + (j + 1) * ni + (k + 1) * nj * ni]
    elements = np.array(elements)
    cell_type = np.array([pv.CellType.HEXAHEDRON] * np.count_nonzero(data))
    grid_mesh = pv.UnstructuredGrid(elements, cell_type, nodes)

    return grid_mesh


def create_strut_lines_with_pyvista(nodes: dict, struts: dict, model_size: tuple = (1.0, 1.0, 1.0)):
    node_coordinates = []
    lines = []

    for index, node in nodes.items():
        node_coordinates.append(node.get_coordinate_array() * np.array(model_size))

    for index, strut in struts.items():
        n1 = strut.start_node.node_id - 1
        n2 = strut.end_node.node_id - 1
        lines.append([2, n1, n2])

    lines = np.hstack(lines)
    mesh = pv.PolyData(node_coordinates, lines=lines)

    return mesh


def plot_nodal_points(plotter: pv.plotter, nodes: dict, label="", model_size: tuple = (1.0, 1.0, 1.0)):
    labels = []
    coordinates = []
    for index, node in nodes.items():
        if label == "ID":
            labels.append(str(node.node_id))
        elif label == "Coordinates":
            labels.append(str(node.get_coordinate_array() * np.array(model_size)))
        coordinates.append(node.get_coordinate_array() * np.array(model_size))

    plotter.add_point_labels(np.array(coordinates),
                             labels,
                             italic=True,
                             font_size=20,
                             point_color='red',
                             point_size=20,
                             render_points_as_spheres=True,
                             always_visible=True,
                             shadow=True,
                             )


def plot_strut_labels(plotter: pv.plotter, struts: dict, model_size: tuple = (1.0, 1.0, 1.0)):
    labels = []
    coordinates = []
    for index, strut in struts.items():
        n1 = strut.start_node.get_coordinate_array() * np.array(model_size)
        n2 = strut.end_node.get_coordinate_array() * np.array(model_size)
        coordinates.append((n1 + n2) * 0.5)
        labels.append(str(strut.strut_id))

    plotter.add_point_labels(np.array(coordinates),
                             labels,
                             italic=True,
                             font_size=20,
                             point_size=0.001,
                             render_points_as_spheres=True,
                             always_visible=True,
                             shadow=False,
                             )
