import os
from PySide6.QtWidgets import (QFileDialog,
                               QTableWidgetItem)

from preprocessor.properties import material
from input_output.write_h5 import write_material_h5
from ui import ui_material_editor
from ui.table2dataframe import get_dataframe


class MaterialEditor(object):
    def __init__(self,
                 function_communication,
                 main_widget,
                 ui: ui_material_editor.Ui_OpenLatticeMaterialEditor):
        self.__function_communication = function_communication
        self.__main_widget = main_widget
        self.__ui = ui

        self.__active_model_index = 0

        self.__material_table = {}

    def import_material(self):
        pass

    def export_material(self):
        file_type = "h5"
        file_name = QFileDialog.getSaveFileName(self.__main_widget, "Save as...", os.getcwd(), f"*.{file_type}")
        write_material_h5(file_name[0], self.__material_table)

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
        self.__ui.comboBox_material_curve.addItem(str(material_id))
        self.__ui.comboBox_material_remove.addItem(str(material_id))

        if ("No Model" == self.__ui.comboBox_material_remove.itemText(0)):
            self.__ui.comboBox_material_remove.removeItem(0)
            self.__ui.comboBox_material_curve.removeItem(0)

    def __add_materials_row(self, material_id=1, name="", modulus_of_elasticity=0.0, poissons_ratio=0.0,
                            thermal_conductivity=0.0, yield_strength=0.0, yield_strain=0.0, tensile_strength=0.0,
                            tensile_strain=0.0):
        material_table_row_count = self.__ui.tableWidget_material.rowCount()
        self.__ui.tableWidget_material.insertRow(material_table_row_count)

        self.__material_table[material_id] = material.NonLinearMaterial(material_id,
                                                                        modulus_of_elasticity,
                                                                        poissons_ratio,
                                                                        yield_strength,
                                                                        tensile_strength,
                                                                        yield_strain,
                                                                        tensile_strain,
                                                                        thermal_conductivity,
                                                                        name, )

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

    def remove_material_item(self):
        item_name = self.__ui.comboBox_material_remove.currentText()
        rows_to_remove = []
        for row in range(self.__ui.tableWidget_material.rowCount() - 1, -1, -1):
            item = self.__ui.tableWidget_material.item(row, 0)
            if item_name in item.text():
                rows_to_remove.append(row)

        self.__material_table.pop(int(item_name))

        for row in rows_to_remove:
            self.__ui.tableWidget_material.removeRow(row)
            self.__ui.comboBox_material_curve.removeItem(item_name)
            self.__ui.comboBox_material_remove.removeRow(item_name)

        if self.__ui.comboBox_material_remove.count() == 0:
            self.__ui.comboBox_material_remove.addItem("No Material")
            self.__ui.comboBox_material_curve.addItem("No Material")

    def update_tables(self):
        self.__material_table = {}
        materials = get_dataframe(self.__ui.tableWidget_material)

        for index, row in materials.iterrows():
            new_material = material.NonLinearMaterial(int(row["ID"]),
                                                      float(row["Modulus of Elasticity"]),
                                                      float(row["Poisson\'s Ratio"]),
                                                      float(row["Thermal Conductivity"]),
                                                      float(row["Yield Stress"]),
                                                      float(row["Yield Strain"]),
                                                      float(row["Ultimate Stress"]),
                                                      float(row["Ultimate Strain"]),
                                                      name=row["Name"])
            self.__material_table[new_material.contains] = new_material

    @property
    def active_model_stress_strains(self):
        material_id = int(self.__ui.comboBox_material_curve.currentIndex())
        data = self.__material_table[material_id].ramberg_osgoon_values
        stresses = data["Stresses"].values
        strains = data["Strains [%]"].values / 100
        return stresses, strains
