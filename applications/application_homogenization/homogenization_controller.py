import numpy as np

from ui import ui_homogenization_interface


class HomogenizationController(object):
    def __init__(self,
                 function_communication,
                 main_widget,
                 ui: ui_homogenization_interface.Ui_OpenLatticeHomogenization):
        self.__function_communication = function_communication
        self.__main_widget = main_widget
        self.__ui = ui

        self.__case_flag_thickness = True
        self.__unit_strain_array = np.array([])
        self.__thickness_array = np.array([])
        self.__volume_fraction_array = np.array([])

    def homogenize_lattices(self):
        pass
