import os
from PySide6.QtWidgets import (QFileDialog,
                               QTableWidgetItem)

from preprocessor.homogenization_models.lattice_model import LatticeModel
from preprocessor.homogenization_models import elements as el
from preprocessor.homogenization_models import nodes as nd
import material
from file_editor.read_lif import read_input_file
from file_editor.write_lif import write_input_lif
from ui import ui_homogenization_interface
from applications.application_homogenization.table2dataframe import get_dataframe


class LatticeDesigner(object):
    def __init__(self,
                 function_communication,
                 main_widget,
                 ui: ui_homogenization_interface.Ui_OpenLatticeHomogenization):
        self.__function_communication = function_communication
        self.__main_widget = main_widget
        self.__ui = ui

        self.__lattice_model = []
        self.__active_model_index = 0

        self.__node_lookup_table = {}
        self.__strut_lookup_table = {}
        self.__material_lookup_table = {}

    def add_model(self, lattice_model: LatticeModel):
        if len(self.__lattice_model) == 0:
            self.__lattice_model.append(lattice_model)
        else:
            self.__lattice_model[self.__active_model_index] = lattice_model

    def get_model(self):
        if self.__ui.comboBox_model_types.currentText() == "From *.lif":
            file_path = QFileDialog.getOpenFileName(self.__main_widget, "Import...", os.getcwd(), f"*.lif")
            if file_path[0] != "":
                model_name = file_path[0]
                self.__node_lookup_table, self.__strut_lookup_table, self.__material_lookup_table = read_input_file(
                    model_name)
        else:
            model_name = self.__ui.comboBox_model_types.currentText()
            model_name = model_name.replace(" ", "").lower() + ".lif"
            model_name = os.path.join(os.getcwd(), os.path.join("standart_lattices", model_name))
            self.__node_lookup_table, self.__strut_lookup_table, self.__material_lookup_table = read_input_file(
                model_name)
        self.__show_values()

    def regenerate_model(self):
        self.__update_tables()
        new_lattice = LatticeModel()
        new_lattice.set_tables(self.__node_lookup_table, self.__strut_lookup_table, self.__material_lookup_table)
        self.add_model(lattice_model=new_lattice)

        resolution = int(self.__ui.spinBox_model_resolution.value())
        x_size = float(self.__ui.spinBox_model_size_x.value())
        y_size = float(self.__ui.spinBox_model_size_y.value())
        z_size = float(self.__ui.spinBox_model_size_z.value())
        self.__lattice_model[self.__active_model_index].set_geometry_size((x_size, y_size, z_size))
        self.__lattice_model[self.__active_model_index].set_resolution(resolution)
        self.__lattice_model[self.__active_model_index].generate_voxel()
        print(self.__lattice_model[self.__active_model_index].volume_fraction)
        self.__function_communication.graph_functions.show_mesh()

    def change_active_model_index(self):
        new_index = 0
        self.__active_model_index = new_index

    def __show_values(self):
        self.clear_rows()
        nodes = self.__node_lookup_table
        struts = self.__strut_lookup_table
        materials = self.__material_lookup_table
        for n in nodes:
            n = nodes[n]
            self.__add_nodes_row(n.node_id, n.x, n.y, n.z)
            self.__ui.comboBox_node_remove.addItem(str(n.node_id))

        for s in struts:
            s = struts[s]
            self.__add_struts_row(s.strut_id, s.start_node.node_id, s.end_node.node_id, s.material.material_id,
                                  s.radius)
            self.__ui.comboBox_strut_remove.addItem(str(s.strut_id))

        for m in materials:
            m = materials[m]
            self.__add_materials_row(m.material_id, m.name, m.modulus_of_elasticity,
                                     m.poissons_ratio, m.thermal_conductivity, m.yield_strength,
                                     m.yield_strain, m.tensile_strength, m.tensile_strain)
            self.__ui.comboBox_material_remove.addItem(str(m.material_id))

    def __add_nodes_row(self, name: int, x=0.0, y=0.0, z=0.0):
        node_table_row_count = self.__ui.tableWidget_node.rowCount()
        self.__ui.tableWidget_node.insertRow(node_table_row_count)

        name_item = QTableWidgetItem(str(name))
        x_item = QTableWidgetItem(str(x))
        y_item = QTableWidgetItem(str(y))
        z_item = QTableWidgetItem(str(z))

        self.__ui.tableWidget_node.setItem(node_table_row_count, 0, name_item)
        self.__ui.tableWidget_node.setItem(node_table_row_count, 1, x_item)
        self.__ui.tableWidget_node.setItem(node_table_row_count, 2, y_item)
        self.__ui.tableWidget_node.setItem(node_table_row_count, 3, z_item)

    def __add_struts_row(self, name: int, start_node=0.0, end_node=0.0, material_id=0, radius=0.0):
        strut_table_row_count = self.__ui.tableWidget_strut.rowCount()
        self.__ui.tableWidget_strut.insertRow(strut_table_row_count)

        name_item = QTableWidgetItem(str(name))
        start_node_item = QTableWidgetItem(str(start_node))
        end_node_item = QTableWidgetItem(str(end_node))
        material_id_item = QTableWidgetItem(str(material_id))
        radius_item = QTableWidgetItem(str(radius))

        self.__ui.tableWidget_strut.setItem(strut_table_row_count, 0, name_item)
        self.__ui.tableWidget_strut.setItem(strut_table_row_count, 1, start_node_item)
        self.__ui.tableWidget_strut.setItem(strut_table_row_count, 2, end_node_item)
        self.__ui.tableWidget_strut.setItem(strut_table_row_count, 3, material_id_item)
        self.__ui.tableWidget_strut.setItem(strut_table_row_count, 4, radius_item)

    def __add_materials_row(self, material_id=1, name="", modulus_of_elasticity=0.0, poissons_ratio=0.0,
                            thermal_conductivity=0.0, yield_strength=0.0, yield_strain=0.0, tensile_strength=0.0,
                            tensile_strain=0.0):
        material_table_row_count = self.__ui.tableWidget_material.rowCount()
        self.__ui.tableWidget_material.insertRow(material_table_row_count)

        material_id = QTableWidgetItem(str(material_id))
        material_name = QTableWidgetItem(name)
        modulus_of_elasticity = QTableWidgetItem(str(modulus_of_elasticity))
        poissons_ratio = QTableWidgetItem(str(poissons_ratio))
        thermal_conductivity = QTableWidgetItem(str(thermal_conductivity))
        yield_strength = QTableWidgetItem(str(yield_strength))
        yield_strain = QTableWidgetItem(str(yield_strain))
        tensile_strength = QTableWidgetItem(str(tensile_strength))
        tensile_strain = QTableWidgetItem(str(tensile_strain))

        self.__ui.tableWidget_material.setItem(material_table_row_count, 0, material_id)
        self.__ui.tableWidget_material.setItem(material_table_row_count, 1, material_name)
        self.__ui.tableWidget_material.setItem(material_table_row_count, 2, modulus_of_elasticity)
        self.__ui.tableWidget_material.setItem(material_table_row_count, 3, poissons_ratio)
        self.__ui.tableWidget_material.setItem(material_table_row_count, 4, yield_strength)
        self.__ui.tableWidget_material.setItem(material_table_row_count, 5, tensile_strength)
        self.__ui.tableWidget_material.setItem(material_table_row_count, 6, yield_strain)
        self.__ui.tableWidget_material.setItem(material_table_row_count, 7, tensile_strain)
        self.__ui.tableWidget_material.setItem(material_table_row_count, 8, thermal_conductivity)

    def clear_rows(self):
        self.__ui.tableWidget_node.setRowCount(0)
        self.__ui.tableWidget_strut.setRowCount(0)
        self.__ui.tableWidget_material.setRowCount(0)

        self.__ui.comboBox_node_remove.clear()
        self.__ui.comboBox_strut_remove.clear()
        self.__ui.comboBox_material_remove.clear()

    def add_node(self):
        node_id = int(self.__ui.spinBox_node_name.value())
        new_x = float(self.__ui.lineEdit_node_x.text())
        new_y = float(self.__ui.lineEdit_node_y.text())
        new_z = float(self.__ui.lineEdit_node_z.text())
        self.__add_nodes_row(node_id, new_x, new_y, new_z)
        self.__ui.spinBox_node_name.setValue(node_id + 1)

    def add_strut(self):
        strut_id = int(self.__ui.spinBox_strut_name.value())
        start_node_id = int(self.__ui.lineEdit_strut_start_node_id.text())
        end_node_id = int(self.__ui.lineEdit_strut_end_node_id.text())
        material_id = int(self.__ui.lineEdit_strut_material_id.text())
        radius = float(self.__ui.lineEdit_strut_radius.text())
        self.__add_struts_row(strut_id, start_node_id, end_node_id, material_id, radius)
        self.__ui.spinBox_strut_name.setValue(strut_id + 1)

    def add_material(self):
        material_id = int(self.__ui.spinBox_material_id.value())
        material_name = self.__ui.lineEdit_material_name.text()
        modulus_of_elasticity = float(self.__ui.lineEdit_modulus_of_elasticity.text())
        poissons_ratio = float(self.__ui.lineEdit_poissons_ratio.text())
        thermal_conductivity = float(self.__ui.lineEdit_thermal_conductivity.text())
        yield_stress = float(self.__ui.lineEdit_yield_stress.text())
        yield_strain = float(self.__ui.lineEdit_yield_strain.text())
        ultimate_stress = float(self.__ui.lineEdit_ultimate_stress.text())
        ultimate_strain = float(self.__ui.lineEdit_ultimate_strain.text())
        self.__add_materials_row(material_id, material_name, modulus_of_elasticity, poissons_ratio,
                                 thermal_conductivity, yield_stress, yield_strain, ultimate_stress,
                                 ultimate_strain)
        self.__ui.spinBox_material_id.setValue(material_id + 1)

    def remove_node_item(self):
        item_name = self.__ui.comboBox_node_remove.currentText()
        rows_to_remove = []
        for row in range(self.__ui.tableWidget_node.rowCount() - 1, -1, -1):  # Iterate backwards
            for col in range(self.__ui.tableWidget_node.columnCount()):
                item = self.__ui.tableWidget_node.item(row, col)
                if item and item_name in item.text():
                    rows_to_remove.append(row)
                    break  # Stop iterating columns if string found

        for row in rows_to_remove:
            self.__ui.tableWidget_node.removeRow(row)

    def remove_strut_item(self):
        item_name = self.__ui.comboBox_strut_remove.currentText()
        rows_to_remove = []
        for row in range(self.__ui.tableWidget_strut.rowCount() - 1, -1, -1):  # Iterate backwards
            for col in range(self.__ui.tableWidget_strut.columnCount()):
                item = self.__ui.tableWidget_strut.item(row, col)
                if item and item_name in item.text():
                    rows_to_remove.append(row)
                    break  # Stop iterating columns if string found

        for row in rows_to_remove:
            self.__ui.tableWidget_strut.removeRow(row)

    def remove_material_item(self):
        item_name = self.__ui.comboBox_material_remove.currentText()
        rows_to_remove = []
        for row in range(self.__ui.tableWidget_material.rowCount() - 1, -1, -1):  # Iterate backwards
            for col in range(self.__ui.tableWidget_material.columnCount()):
                item = self.__ui.tableWidget_material.item(row, col)
                if item and item_name in item.text():
                    rows_to_remove.append(row)
                    break  # Stop iterating columns if string found

        for row in rows_to_remove:
            self.__ui.tableWidget_material.removeRow(row)

    def __update_tables(self):
        self.__node_lookup_table = {}
        self.__strut_lookup_table = {}
        self.__material_lookup_table = {}

        nodes = get_dataframe(self.__ui.tableWidget_node)
        struts = get_dataframe(self.__ui.tableWidget_strut)
        materials = get_dataframe(self.__ui.tableWidget_material)

        for index, row in nodes.iterrows():
            self.__node_lookup_table[int(row["Name"])] = nd.Node(int(row["Name"]),
                                                                 float(row["X"]),
                                                                 float(row["Y"]),
                                                                 float(row["Z"]))

        for index, row in materials.iterrows():
            new_material = material.NonLinearMaterial(int(row["ID"]),
                                                      float(row["Modulus of Elasticity"]),
                                                      float(row["Poisson\'s Ratio"]),
                                                      float(row["Thermal Conductivity"]),
                                                      float(row["Yield Stress"]),
                                                      float(row["Yield Strain"]),
                                                      float(row["Ultimate Stress"]),
                                                      float(row["Ultimate Strain"]))
            self.__material_lookup_table[new_material.contains] = new_material

        for index, row in struts.iterrows():
            self.__strut_lookup_table[int(row["Name"])] = el.Strut(int(row["Name"]),
                                                                   self.__node_lookup_table[int(row["Start Node"])],
                                                                   self.__node_lookup_table[int(row["End Node"])],
                                                                   self.__material_lookup_table[
                                                                       tuple([int(row["Material"])])],
                                                                   float(row["Radius"]))

    def save_lif_file(self):
        file_type = "lif"
        file_name = QFileDialog.getSaveFileName(self.__main_widget, "Save as...", os.getcwd(), f"*.{file_type}")
        write_input_lif(file_name[0], self.__node_lookup_table, self.__strut_lookup_table, self.__material_lookup_table)

    def activate_last_model(self):
        pass

    @property
    def active_model_geometry_size(self):
        return self.__lattice_model[self.__active_model_index].geometry_size

    @property
    def active_model_voxel_array(self):
        return self.__lattice_model[self.__active_model_index].voxel_array

    @property
    def node_lookup_table(self):
        return self.__node_lookup_table

    @property
    def strut_lookup_table(self):
        return self.__strut_lookup_table

    @property
    def material_lookup_table(self):
        return self.__material_lookup_table
