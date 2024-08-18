import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QVBoxLayout

from ui import ui_static_interface
import preprocessor.models.elements as el
import preprocessor.models.nodes as nd
import postprocessor.mesh_plotter as mp
from applications.application_static.model_storage import Storage

pv.global_theme.allow_empty_mesh = True


class FunctionsGraph(object):
    def __init__(self,
                 function_communication,
                 main_widget,
                 ui: ui_static_interface.Ui_CellulozStatic):
        self.__function_communication = function_communication
        self.__main_widget = main_widget
        self.__ui = ui

        self.__opacity = 1

        self.__showed_choosen_node_actor = None
        self.__showed_tetrahedron_mesh = None
        self.__showed_hexahedron_mesh = None
        self.__showed_tetrahedron_mesh_lines = None
        self.__showed_hexahedron_mesh_lines = None

        self.__flag_show_nodes = False
        self.__flag_show_edges = True
        self.__visual_parameter_mesh_opacity = 1.0

        self.__set_vtk()

    def __set_vtk(self):
        vlayout1 = QVBoxLayout()
        self.__plotter = QtInteractor(self.__ui.frame_vista)
        light = pv.Light(light_type='camera light')
        self.__plotter.add_light(light)
        self.__plotter.set_background('#353535', top='#000000')
        vlayout1.addWidget(self.__plotter.interactor)
        self.__ui.frame_vista.setLayout(vlayout1)

    def show_mesh(self):
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

    def set_full_opacity(self):
        self.__opacity = 1.0
        self.plot_solid_system()

    def self_half_opacity(self):
        self.__opacity = 0.1
        self.plot_solid_system()

    def plot_solid_system(self, scale: float = 1.0, label=""):
        self.clear_showed_models()

        data: Storage = self.__function_communication.static_case_editor.model_storage

        visual_meshes, edge_meshes = mp.plot_mesh_static_case_mesh(data, scale)

        self.__showed_tetrahedron_mesh = self.__plotter.add_mesh(visual_meshes[0],
                                                                 show_edges=False,
                                                                 color="cyan",
                                                                 opacity=self.__opacity)
        self.__showed_tetrahedron_mesh = self.__plotter.add_mesh(visual_meshes[1],
                                                                 show_edges=False,
                                                                 color="cyan",
                                                                 opacity=self.__opacity)

        self.__showed_tetrahedron_mesh_lines = self.__plotter.add_mesh(edge_meshes[0],
                                                                       color="white",
                                                                       edge_color="white")

        self.__showed_hexahedron_mesh_lines = self.__plotter.add_mesh(edge_meshes[1],
                                                                      color="white",
                                                                      edge_color="white")

        self.__plotter.add_axes()
        self.__plotter.show_grid()
        self.__plotter.reset_camera()

    def show_choosed_nodes(self, node_ids: np.array):
        if self.__showed_choosen_node_actor is not None:
            self.__plotter.remove_actor(self.__showed_choosen_node_actor)

        data: Storage = self.__function_communication.static_case_editor.model_storage

        points = mp.plot_points(data, node_ids)
        self.__showed_choosen_node_actor = self.__plotter.add_mesh(points, color="red")
        self.__plotter.reset_camera()

    def show_nodal_results(self, plot_code="", scale: float = 1.0):
        self.clear_showed_models()

        data: Storage = self.__function_communication.static_case_editor.model_storage

        visual_meshes, edge_meshes = mp.plot_mesh_static_case_mesh(data, scale)

        if plot_code == "ResultDisplacementTotal":
            scalar = np.sqrt(np.square(np.array(data.node_storage.data["ResultDisplacementX"].values)) + np.square(
                np.array(data.node_storage.data["ResultDisplacementY"].values)) + np.square(
                np.array(data.node_storage.data["ResultDisplacementZ"].values)))

        elif plot_code == "ResultForceTotal":
            scalar = np.sqrt(np.square(np.array(data.node_storage.data["ResultForceX"].values)) + np.square(
                np.array(data.node_storage.data["ResultForceY"].values)) + np.square(
                np.array(data.node_storage.data["ResultForceZ"].values)))

        else:
            scalar = data.node_storage.data[plot_code].values

        self.__showed_tetrahedron_mesh = self.__plotter.add_mesh(visual_meshes[0],
                                                                 show_edges=False,
                                                                 cmap="turbo",
                                                                 scalars=scalar, )
        self.__showed_hexahedron_mesh = self.__plotter.add_mesh(visual_meshes[1],
                                                                show_edges=False,
                                                                cmap="turbo",
                                                                scalars=scalar, )

        self.__showed_tetrahedron_mesh_lines = None

        self.__showed_hexahedron_mesh_lines = None

        self.__plotter.add_axes()
        self.__plotter.show_grid()
        self.__plotter.reset_camera()

    def show_element_results(self, plot_code="", scale: float = 1.0):
        self.clear_showed_models()

        data: Storage = self.__function_communication.static_case_editor.model_storage

        visual_meshes, edge_meshes = mp.plot_mesh_static_case_mesh(data, scale)

        if len(data.element_tetra_four_storage.data[plot_code].values) != 0:
            visual_meshes[0].cell_data[plot_code] = data.element_tetra_four_storage.data[plot_code].values
            min_tetra_values = min(data.element_tetra_four_storage.data[plot_code].values)
            max_tetra_values = max(data.element_tetra_four_storage.data[plot_code].values)
            self.__showed_tetrahedron_mesh = self.__plotter.add_mesh(visual_meshes[0],
                                                                     show_edges=False,
                                                                     cmap="turbo",
                                                                     scalars=plot_code,
                                                                     clim=(min_tetra_values, max_tetra_values))
        else:
            self.__showed_tetrahedron_mesh = None

        if len(data.element_brick_eight_storage.data[plot_code].values) != 0:
            visual_meshes[1].cell_data[plot_code] = data.element_brick_eight_storage.data[plot_code].values
            min_hexa_values = min(data.element_brick_eight_storage.data[plot_code].values)
            max_hexa_values = max(data.element_brick_eight_storage.data[plot_code].values)
            self.__showed_hexahedron_mesh = self.__plotter.add_mesh(visual_meshes[1],
                                                                    show_edges=False,
                                                                    cmap="turbo",
                                                                    scalars=plot_code,
                                                                    clim=(min_hexa_values, max_hexa_values))
        else:
            self.__showed_hexahedron_mesh = None

        self.__showed_tetrahedron_mesh_lines = None

        self.__showed_hexahedron_mesh_lines = None

        self.__plotter.add_axes()
        self.__plotter.show_grid()
        self.__plotter.reset_camera()

    def __set_args(self, title: str):
        return {"title": title + "\n", "fmt": "%10.3f", "n_labels": 10, "label_font_size": 17,
                "title_font_size": 22, "height": 0.6, "width": 0.04, "vertical": True, "position_y": 0.18}

    def plot_x_displacement(self):
        plot_code = "ResultDisplacementX"
        self.show_nodal_results(plot_code)

    def plot_y_displacement(self):
        plot_code = "ResultDisplacementY"
        self.show_nodal_results(plot_code)

    def plot_z_displacement(self):
        plot_code = "ResultDisplacementZ"
        self.show_nodal_results(plot_code)

    def plot_total_displacement(self):
        plot_code = "ResultDisplacementTotal"
        self.show_nodal_results(plot_code)

    def plot_x_force(self):
        plot_code = "ResultForceX"
        self.show_nodal_results(plot_code)

    def plot_y_force(self):
        plot_code = "ResultForceY"
        self.show_nodal_results(plot_code)

    def plot_z_force(self):
        plot_code = "ResultForceZ"
        self.show_nodal_results(plot_code)

    def plot_total_force(self):
        plot_code = "ResultForceTotal"
        self.show_nodal_results(plot_code)

    def plot_von_misses_stress(self):
        plot_code = "VonMissesStress"
        self.show_element_results(plot_code)

    def plot_von_misses_strain(self):
        plot_code = "VonMissesStrain"
        self.show_element_results(plot_code)

    def plot_von_misses_energy(self):
        plot_code = "VonMissesEnergy"
        self.show_element_results(plot_code)
