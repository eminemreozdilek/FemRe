from ui import ui_static_interface, ui_material_editor
from applications.controller_static import graph_functions
from applications.controller_static import static_case_editor
import PySide6.QtWidgets as QtWidgets


class UIStaticFunctionsCommunication(object):
    def __init__(self, main_widget, ui: ui_static_interface.Ui_CellulozStatic):
        self.__main_widget = main_widget
        self.__ui = ui
        self.__item_data = {}

        self.__graph_functions = graph_functions.FunctionsGraph(self, self.__main_widget, self.__ui)
        self.__static_case_editor = static_case_editor.StaticFiniteElementMethod(self, self.__main_widget, self.__ui)

    @property
    def graph_functions(self):
        return self.__graph_functions

    @property
    def static_case_editor(self):
        return self.__static_case_editor
