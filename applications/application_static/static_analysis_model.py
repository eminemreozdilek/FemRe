import os
import sys
import numpy as np
import pandas as pd
from PySide6.QtWidgets import QFileDialog, QWidget, QApplication

from file_editor import read_sif, read_msh
from ui import ui_static_interface
from applications.application_static.model_storage import Storage
from solver import solve


class StaticAnalysisModel(object):

    def __init__(self,
                 function_communication,
                 main_widget,
                 ui: ui_static_interface.Ui_CellulozStatic):

        self.__function_communication = function_communication
        self.__main_widget = main_widget
        self.__ui = ui

        self.__model_storage: Storage = None

        self.__us = None
        self.__ps = None

        self.__status = {"GeometricModelGenerated": False,
                         "MathematicModelGenerated": False,
                         "Results": False, }

    def import_static_model(self):

        file_path = QFileDialog.getOpenFileName(
            self.__main_widget,
            "Import...",
            os.environ["FEMRE_LOCATION"],
            "Static Input Files (*.sif);;HDF5 Files (*.h5);;MESH Files (*.msh);;CSV Files (*.csv);;")

        if file_path[0] != "":
            model_name = file_path[0]
            if model_name.endswith(".h5"):
                pass
            elif model_name.endswith(".sif"):
                # data = read_sif.read_input_file(model_name)
                pass
            elif model_name.endswith(".msh"):
                data = read_msh.read_msh(model_name)
                self.update_model_storage(data)
            self.__function_communication.graph_functions.show_mesh()

    def get_mathematical_model(self):
        self.__model_storage.generate_mathematical_model()
        us, ps = solve(self.__model_storage)
        self.__model_storage.save_mechanical_results(us, ps)
        self.__function_communication.graph_functions.show_mesh()

    def update_model_storage(self, data: Storage):
        self.__model_storage = data

    def set_boundary_conditions(self):
        data = self.__model_storage.node_storage.data
        node_ids = self.__get_volume()
        mask = data["NodeID"].isin(node_ids)
        bc_type = self.__ui.comboBox_bc_type.currentText()

        if "Rest" == bc_type:
            if self.__ui.checkBox_bc_add_x.isChecked():
                data.loc[mask, "RestX"] = 1
            if self.__ui.checkBox_bc_add_y.isChecked():
                data.loc[mask, "RestY"] = 1
            if self.__ui.checkBox_bc_add_z.isChecked():
                data.loc[mask, "RestZ"] = 1

        elif "Displacement" == bc_type:
            if self.__ui.checkBox_bc_add_x.isChecked():
                data.loc[mask, "RestX"] = 1
                data.loc[mask, "DisplacementX"] = float(self.__ui.lineEdit_value_x.text())
            if self.__ui.checkBox_bc_add_y.isChecked():
                data.loc[mask, "RestY"] = 1
                data.loc[mask, "DisplacementY"] = float(self.__ui.lineEdit_value_y.text())
            if self.__ui.checkBox_bc_add_z.isChecked():
                data.loc[mask, "RestZ"] = 1
                data.loc[mask, "DisplacementZ"] = float(self.__ui.lineEdit_value_z.text())

        elif "Force" == bc_type:
            if self.__ui.checkBox_bc_add_x.isChecked():
                data.loc[mask, "ForceX"] = float(self.__ui.lineEdit_value_x.text())
            if self.__ui.checkBox_bc_add_y.isChecked():
                data.loc[mask, "ForceY"] = float(self.__ui.lineEdit_value_y.text())
            if self.__ui.checkBox_bc_add_z.isChecked():
                data.loc[mask, "ForceZ"] = float(self.__ui.lineEdit_value_z.text())

        else:
            pass

        self.__model_storage.set_new_nodal_data(data)
        self.__function_communication.graph_functions.show_mesh()

    def clear_boundary_conditions(self):
        data = self.__model_storage.node_storage.data
        node_ids = self.__get_volume()
        mask = data.isin(node_ids)
        bc_type = self.__ui.comboBox_bc_type.currentText()

        if "Rest" == bc_type:
            if self.__ui.checkBox_bc_add_x.isChecked():
                data.loc[mask, "RestX"] = 0
            if self.__ui.checkBox_bc_add_y.isChecked():
                data.loc[mask, "RestY"] = 0
            if self.__ui.checkBox_bc_add_z.isChecked():
                data.loc[mask, "RestZ"] = 0

        elif "Displacement" == bc_type:
            if self.__ui.checkBox_bc_add_x.isChecked():
                data.loc[mask, "DisplacementX"] = 0
            if self.__ui.checkBox_bc_add_y.isChecked():
                data.loc[mask, "DisplacementY"] = 0
            if self.__ui.checkBox_bc_add_z.isChecked():
                data.loc[mask, "DisplacementZ"] = 0

        elif "Force" == bc_type:
            if self.__ui.checkBox_bc_add_x.isChecked():
                data.loc[mask, "ForceX"] = 0
            if self.__ui.checkBox_bc_add_y.isChecked():
                data.loc[mask, "ForceY"] = 0
            if self.__ui.checkBox_bc_add_z.isChecked():
                data.loc[mask, "ForceZ"] = 0

        else:
            pass

        self.__model_storage.set_new_nodal_data(data)
        self.__function_communication.graph_functions.show_mesh()

    def update_choosen_nodes(self):
        node_ids = self.__get_volume()
        self.__function_communication.graph_functions.show_choosed_nodes(node_ids)

    def __get_volume(self):
        center_coordinate = [self.__ui.doubleSpinBox_x_coordinate.value(),
                             self.__ui.doubleSpinBox_y_coordinate.value(),
                             self.__ui.doubleSpinBox_z_coordinate.value()]
        addition_x = self.__ui.doubleSpinBox_x_coordinate_volume.value() / 2
        addition_y = self.__ui.doubleSpinBox_y_coordinate_volume.value() / 2
        addition_z = self.__ui.doubleSpinBox_z_coordinate_volume.value() / 2

        max_coordinates = (
            center_coordinate[0] + addition_x, center_coordinate[1] + addition_y, center_coordinate[2] + addition_z)
        min_coordinates = (
            center_coordinate[0] - addition_x, center_coordinate[1] - addition_y, center_coordinate[2] - addition_z)
        return self.__model_storage.node_storage.get_node_id_from_volume(min_coordinates, max_coordinates)

    @property
    def model_storage(self):
        return self.__model_storage
