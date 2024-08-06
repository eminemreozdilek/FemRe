import numpy as np
import pyvista as pv


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
