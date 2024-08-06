import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QVBoxLayout

from ui import ui_static_interface
import preprocessor.models.elements as el
import preprocessor.models.nodes as nd


class FunctionsGraph(object):
    def __init__(self,
                 function_communication,
                 main_widget,
                 ui: ui_static_interface.Ui_CellulozStatic):
        self.__function_communication = function_communication
        self.__main_widget = main_widget
        self.__ui = ui

        self.__flag_showed_mesh_type = "VoxelMesh"
        self.__flag_show_nodes = True
        self.__flag_show_edges_labels = True

        self.__set_vtk()

    def __set_vtk(self):
        vlayout1 = QVBoxLayout()
        self.__plotter = QtInteractor(self.__ui.frame_vista)
        light = pv.Light(light_type='camera light')
        self.__plotter.add_light(light)
        self.__plotter.set_background('#BCD2E8', top='#03002E')
        vlayout1.addWidget(self.__plotter.interactor)
        self.__ui.frame_vista.setLayout(vlayout1)

    def show_mesh(self):
        if self.__flag_showed_mesh_type == "StrutMesh":
            self.show_strut_mesh()
        elif self.__flag_showed_mesh_type == "VoxelMesh":
            self.plot_solid_system()


    def clear_showed_models(self):
        self.__plotter.clear()
        self.__plotter.add_light(pv.Light(light_type='camera light'))

    def set_isometric_view(self):
        self.__plotter.view_isometric()

    def set_front_view(self):
        self.__plotter.view_xz(False)

    def set_back_view(self):
        self.__plotter.view_xz(True)

    def set_right_view(self):
        self.__plotter.view_yz(True)

    def set_left_view(self):
        self.__plotter.view_yz(False)

    def set_top_view(self):
        self.__plotter.view_xy(True)

    def set_bottom_view(self):
        self.__plotter.view_xy(False)

    def plot_solid_system(self, scale=1.0, label=""):
        self.clear_showed_models()

        data = self.__function_communication.static_case_editor.model_storage
        label = label.lower()
        plotter = self.__plotter
        elements = data.element_storage

        node_coordinates = []
        node_displacements = []
        node_forces = []
        node_ids = []
        for index, row in data.node_storage.iterrows():
            node: nd.NodeSolid = row["Node"]
            node_coordinates.append(node.coordinates)
            node_displacements.append(node.result_displacements)
            node_forces.append(node.result_forces)
            node_ids.append(str(node.node_id))

        if node_displacements[0] is not None:
            result_node_coordinates = {}
            result_node_ids = {}
            for index, row in data.node_storage.iterrows():
                node: nd.NodeSolid = row["Node"]
                result_displacements = node_displacements[index - 1]
                new_coords = result_displacements[0:3] * scale + node.coordinates
                result_node_coordinates[node.node_id] = new_coords

                if label == "id":
                    result_node_ids[node.node_id] = str(node.node_id) + "\'"

                elif label == "displacements":
                    result_node_ids[node.node_id] = (str(node.node_id) + "\'" +
                                                     "\nx: " + str(round(result_displacements[0], 9)) +
                                                     "\ny: " + str(round(result_displacements[1], 9)) +
                                                     "\nz: " + str(round(result_displacements[2], 9)))
                elif label == "forces":
                    result_node_ids[node.node_id] = str(node.node_id) + "\'"

            node_cloud = np.array(list(result_node_coordinates.values()))

        else:
            node_cloud = np.array(node_coordinates)

        cells = []
        for index, row in elements.iterrows():
            element: el.ElementBrickEight = row["Element"]
            cells.append([8,
                          element.connected_nodes[0].node_id - 1,
                          element.connected_nodes[1].node_id - 1,
                          element.connected_nodes[2].node_id - 1,
                          element.connected_nodes[3].node_id - 1,
                          element.connected_nodes[4].node_id - 1,
                          element.connected_nodes[5].node_id - 1,
                          element.connected_nodes[6].node_id - 1,
                          element.connected_nodes[7].node_id - 1])

        cells = np.array(cells)
        cell_type = np.full(len(elements), pv.CellType.HEXAHEDRON, dtype=np.uint8)
        grid = pv.UnstructuredGrid(cells, cell_type, node_cloud)
        mesh_actor = plotter.add_mesh(grid, color="grey", opacity=0.99)

        plotter.show_grid(n_xlabels=11, n_ylabels=11, n_zlabels=11, fmt="%.3f")
        plotter.show_grid()
        plotter.add_axes()
        plotter.reset_camera()
