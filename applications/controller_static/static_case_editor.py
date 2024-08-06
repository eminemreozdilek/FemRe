import os
from PySide6.QtWidgets import (QFileDialog,
                               QTableWidgetItem)

import pandas as pd
import preprocessor.models.nodes as nd
import preprocessor.models.elements as elmnt
import preprocessor.properties.section as sct
import preprocessor.properties.material as mtrl
from input_output import read_sif
from applications.controller_static.model_storage import Storage
from applications.controller_static.function_communication import UIStaticFunctionsCommunication


class StaticFiniteElementMethod:
    def __init__(self, function_communication: UIStaticFunctionsCommunication, main_widget, ui):
        self.__function_communication = function_communication
        self.__main_widget = main_widget
        self.__ui = ui

        self.__model_storage = None

    def import_static_model(self):
        file_path = QFileDialog.getOpenFileName(self.__main_widget,
                                                "Import...",
                                                os.getcwd(),
                                                "Static Input Files (*.sif);;HDF5 Files (*.h5);;CSV Files (*.csv);;")
        if file_path[0] != "":
            model_name = file_path[0]
            data = read_sif.read_input_file(model_name)
            self.update_model_storage(data)
            self.__function_communication.graph_functions.show_mesh()

    def update_model_storage(self, data: Storage):
        self.__model_storage = data

    @property
    def model_storage(self):
        return self.__model_storage
