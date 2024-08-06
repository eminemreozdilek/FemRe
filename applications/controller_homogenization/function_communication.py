from ui import ui_homogenization_interface, ui_material_editor
from applications.controller_homogenization import lattice_designer, homogenization_controller, ui_functions, graph_functions


class UIHomogenizationFunctionsCommunication(object):
    def __init__(self, main_widget, ui: ui_homogenization_interface.Ui_OpenLatticeHomogenization):
        self.__main_widget = main_widget
        self.__ui = ui

        self.__graph_functions = graph_functions.FunctionsGraph(self, self.__main_widget, self.__ui)
        self.__lattice_designer = lattice_designer.LatticeDesigner(self, self.__main_widget, self.__ui)
        self.__homogenization_functions = homogenization_controller.HomogenizationController(self, self.__main_widget,
                                                                                             self.__ui)
        self.__ui_functions = ui_functions.UIFunctions(self, self.__main_widget, self.__ui)

    @property
    def graph_functions(self):
        return self.__graph_functions

    @property
    def lattice_designer(self):
        return self.__lattice_designer

    @property
    def ui_functions(self):
        return self.__ui_functions
