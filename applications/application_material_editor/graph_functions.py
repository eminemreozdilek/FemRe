import numpy as np
import os
import pyvista as pv

from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QFileDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui import ui_material_editor
from postprocessor import mesh_plotter


class FunctionsGraph(object):
    def __init__(self,
                 function_communication,
                 main_widget,
                 ui: ui_material_editor.Ui_OpenLatticeMaterialEditor):
        self.__function_communication = function_communication
        self.__main_widget = main_widget
        self.__ui = ui
        self.__grid_visibility = True

        self.__set_vtk()

    def __set_vtk(self):
        vlayout2 = QVBoxLayout()
        self.__figure = Figure()
        self.__graph_plotter = FigureCanvas(self.__figure)
        vlayout2.addWidget(self.__graph_plotter)
        self.__ui.frame_graph.setLayout(vlayout2)
        self.clear_graph_plot()

    def clear_graph_plot(self):
        self.__figure.clear()
        self.__ax = self.__figure.add_subplot(111)
        self.__ax.set_box_aspect(1)
        self.__plotting_list = []
        self.__last_plot_type = ""
        self.__graph_plotter.draw()

    def replot_curve(self):
        self.__ax.set_title("Ramberg Osgoon Curve", pad=20, fontsize=20)
        self.__ax.set_xlabel("Strain [mm/mm]", fontsize=16)
        self.__ax.set_ylabel("Stress [MPa]", fontsize=16)

        self.__ax.grid(self.__grid_visibility)

        y, x = self.__function_communication.material_editor.active_model_stress_strains
        self.__ax.plot(x, y)
        self.__graph_plotter.draw()

    def show_grid(self):
        self.__grid_visibility = True
        self.__ax.grid(self.__grid_visibility)
        self.__graph_plotter.draw()

    def hide_grid(self):
        self.__grid_visibility = False
        self.__ax.grid(self.__grid_visibility)
        self.__graph_plotter.draw()
