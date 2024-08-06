import numpy as np
import os
import pyvista as pv

from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QFileDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui import ui_homogenization_interface
from postprocessor import mesh_plotter


class FunctionsGraph(object):
    def __init__(self,
                 function_communication,
                 main_widget,
                 ui: ui_homogenization_interface.Ui_OpenLatticeHomogenization):
        self.__function_communication = function_communication
        self.__main_widget = main_widget
        self.__ui = ui

        self.__flag_showed_mesh_type = "StrutMesh"
        self.__flag_show_nodes = True
        self.__flag_show_edges_labels = True

        self.__set_vtk()

    def __set_vtk(self):
        vlayout1 = QVBoxLayout()
        self.plotter = QtInteractor(self.__ui.frame_vista)
        light = pv.Light(light_type='camera light')
        self.plotter.add_light(light)
        self.plotter.set_background('#BCD2E8', top='#03002E')
        vlayout1.addWidget(self.plotter.interactor)
        self.__ui.frame_vista.setLayout(vlayout1)

    def show_mesh(self):
        if self.__flag_showed_mesh_type == "StrutMesh":
            self.show_strut_mesh()
        elif self.__flag_showed_mesh_type == "VoxelMesh":
            self.show_voxel_mesh()

    def show_voxel_mesh(self):
        self.clear_showed_models()
        voxel_array = self.__function_communication.lattice_designer.active_model_voxel_array
        model_geometry_size = self.__function_communication.lattice_designer.active_model_geometry_size
        grid_mesh = mesh_plotter.plot_voxel_with_pyvista(voxel_array, model_geometry_size)
        self.plotter.add_mesh(grid_mesh, show_edges=True, color="cyan")
        self.plotter.add_axes()
        self.plotter.show_grid()
        self.plotter.reset_camera()

    def show_strut_mesh(self):
        self.clear_showed_models()
        nodes = self.__function_communication.lattice_designer.node_lookup_table
        struts = self.__function_communication.lattice_designer.strut_lookup_table
        model_geometry_size = self.__function_communication.lattice_designer.active_model_geometry_size
        strut_lines = mesh_plotter.create_strut_lines_with_pyvista(nodes, struts, model_size=model_geometry_size)
        self.plotter.add_mesh(strut_lines, line_width=10)

        if self.__flag_show_nodes:
            mesh_plotter.plot_nodal_points(self.plotter, nodes, "ID", model_size=model_geometry_size)
        if self.__flag_show_edges_labels:
            mesh_plotter.plot_strut_labels(self.plotter, struts, model_size=model_geometry_size)

        self.plotter.add_axes()
        self.plotter.show_grid()
        self.plotter.reset_camera()

    def set_plot_type_as_voxel_mesh(self):
        self.__flag_showed_mesh_type = "VoxelMesh"
        try:
            self.show_mesh()
        except:
            pass

    def set_plot_type_as_strut_mesh(self):
        self.__flag_showed_mesh_type = "StrutMesh"
        try:
            self.show_mesh()
        except:
            pass

    def clear_showed_models(self):
        self.plotter.clear()
        self.plotter.add_light(pv.Light(light_type='camera light'))

    def set_isometric_view(self):
        self.plotter.view_isometric()

    def set_front_view(self):
        self.plotter.view_xz(False)

    def set_back_view(self):
        self.plotter.view_xz(True)

    def set_right_view(self):
        self.plotter.view_yz(True)

    def set_left_view(self):
        self.plotter.view_yz(False)

    def set_top_view(self):
        self.plotter.view_xy(True)

    def set_bottom_view(self):
        self.plotter.view_xy(False)
