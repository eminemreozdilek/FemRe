from ui import ui_homogenization_interface


class UIFunctions(object):
    def __init__(self,
                 function_communication,
                 main_widget,
                 ui: ui_homogenization_interface.Ui_OpenLatticeHomogenization):
        self.__function_communication = function_communication
        self.__main_widget = main_widget
        self.__ui = ui

    def open_homogenization_menu(self):
        width = self.__ui.frame_homogenization.width()
        if width == 0:
            self.__ui.frame_homogenization.setMaximumWidth(620)
            self.__ui.frame_homogenization.setMinimumWidth(620)

            self.__ui.frame_strut_lattice_designer.setMaximumWidth(0)
            self.__ui.frame_strut_lattice_designer.setMinimumWidth(0)
        else:
            self.__ui.frame_homogenization.setMaximumWidth(0)
            self.__ui.frame_homogenization.setMinimumWidth(0)

    def open_designer_menu(self):
        width = self.__ui.frame_strut_lattice_designer.width()
        if width == 0:
            self.__ui.frame_strut_lattice_designer.setMaximumWidth(620)
            self.__ui.frame_strut_lattice_designer.setMinimumWidth(620)

            self.__ui.frame_homogenization.setMaximumWidth(0)
            self.__ui.frame_homogenization.setMinimumWidth(0)

        else:
            self.__ui.frame_strut_lattice_designer.setMaximumWidth(0)
            self.__ui.frame_strut_lattice_designer.setMinimumWidth(0)
