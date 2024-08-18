from ui import ui_homogenization_interface, ui_material_editor
from applications.controller_material_editor import graph_functions
from applications.controller_material_editor import material_editor
import PySide6.QtWidgets as QtWidgets


class UIMaterialEditorFunctionsCommunication(object):
    def __init__(self, main_widget, ui: ui_material_editor.Ui_OpenLatticeMaterialEditor):
        self.__main_widget = main_widget
        self.__ui = ui
        self.__item_data = {}

        self.__graph_functions = graph_functions.FunctionsGraph(self, self.__main_widget, self.__ui)
        self.__material_editor = material_editor.MaterialEditor(self, self.__main_widget, self.__ui)

    @property
    def graph_functions(self):
        return self.__graph_functions

    @property
    def material_editor(self):
        return self.__material_editor
