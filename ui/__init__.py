import os

import applications.application_homogenization.function_communication as ach
# import applications.controller_material_editor.function_communication as acm
import applications.application_static.function_communication as acs

from pyvistaqt import MainWindow
from PySide6.QtWidgets import QMainWindow
from ui.ui_homogenization_interface import Ui_OpenLatticeHomogenization
from ui.ui_open_interface import Ui_OpenLattice_Lite
# from ui.ui_material_editor import Ui_OpenLatticeMaterialEditor
from ui.ui_static_interface import Ui_CellulozStatic


class HomogenizationWindow(MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.__ui = Ui_OpenLatticeHomogenization()
        self.__ui.setupUi(self)

        self.__ui_functions = ach.UIHomogenizationFunctionsCommunication(self, self.__ui)
        self.__set_communication()

    def __set_communication(self):
        self.__ui.actionDesignerData.triggered.connect(self.__ui_functions.ui_functions.open_designer_menu)
        self.__ui.actionHomogenizer_Data.triggered.connect(self.__ui_functions.ui_functions.open_homogenization_menu)

        self.__ui.actionIsometric.triggered.connect(self.__ui_functions.graph_functions.set_isometric_view)
        self.__ui.actionTop.triggered.connect(self.__ui_functions.graph_functions.set_top_view)
        self.__ui.actionBottom.triggered.connect(self.__ui_functions.graph_functions.set_bottom_view)
        self.__ui.actionFront.triggered.connect(self.__ui_functions.graph_functions.set_front_view)
        self.__ui.actionBack.triggered.connect(self.__ui_functions.graph_functions.set_back_view)
        self.__ui.actionLeft.triggered.connect(self.__ui_functions.graph_functions.set_left_view)
        self.__ui.actionRight.triggered.connect(self.__ui_functions.graph_functions.set_right_view)

        self.__ui.pushButton_top_show_voxel.clicked.connect(
            self.__ui_functions.graph_functions.set_plot_type_as_voxel_mesh)
        self.__ui.pushButton_top_show_strut.clicked.connect(
            self.__ui_functions.graph_functions.set_plot_type_as_strut_mesh)

        self.__ui.pushButton_model_get.clicked.connect(self.__ui_functions.lattice_designer.get_model)
        self.__ui.pushButton_regenerate_model.clicked.connect(self.__ui_functions.lattice_designer.regenerate_model)
        self.__ui.pushButton_save_model.clicked.connect(self.__ui_functions.lattice_designer.save_lif_file)
        self.__ui.pushButton_add_node.clicked.connect(self.__ui_functions.lattice_designer.add_node)
        self.__ui.pushButton_strut_add.clicked.connect(self.__ui_functions.lattice_designer.add_strut)
        self.__ui.pushButton_material_add.clicked.connect(self.__ui_functions.lattice_designer.add_material)
        self.__ui.pushButton_node_remove.clicked.connect(self.__ui_functions.lattice_designer.remove_node_item)
        self.__ui.pushButton_strut_remove.clicked.connect(self.__ui_functions.lattice_designer.remove_strut_item)
        self.__ui.pushButton_material_remove.clicked.connect(self.__ui_functions.lattice_designer.remove_material_item)


# class MaterialEditorWindow(MainWindow):
#     def __init__(self, parent=None):
#         QMainWindow.__init__(self, parent)
#
#         self.__ui = Ui_OpenLatticeMaterialEditor()
#         self.__ui.setupUi(self)
#
#         self.__ui_functions = acm.UIMaterialEditorFunctionsCommunication(self, self.__ui)
#         self.__set_communication()
#
#     def __set_communication(self):
#         self.__ui.actionImport.triggered.connect(self.__ui_functions.material_editor.import_material)
#         self.__ui.actionExport.triggered.connect(self.__ui_functions.material_editor.export_material)
#
#         self.__ui.actionShow_Grid.triggered.connect(self.__ui_functions.graph_functions.show_grid)
#         self.__ui.actionHide_Grid.triggered.connect(self.__ui_functions.graph_functions.hide_grid)
#
#         # self.__ui.tableWidget_material.cellChanged.connect(self.__ui_functions.material_editor.read_table)
#
#         self.__ui.pushButton_material_add.clicked.connect(self.__ui_functions.material_editor.add_material)
#         self.__ui.pushButton_material_remove.clicked.connect(self.__ui_functions.material_editor.remove_material_item)
#         self.__ui.comboBox_material_curve.currentIndexChanged.connect(self.__ui_functions.graph_functions.replot_curve)


class StaticWindow(MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.__ui = Ui_CellulozStatic()
        self.__ui.setupUi(self)

        self.__ui_functions = acs.UIStaticFunctionsCommunication(self, self.__ui)
        self.__set_communication()

    def __set_communication(self):
        self.__ui.actionImportStaticModel.triggered.connect(
            self.__ui_functions.static_case_editor.import_static_model)

        self.__ui.actionIsometric.triggered.connect(
            self.__ui_functions.graph_functions.set_isometric_view)
        self.__ui.actionTop.triggered.connect(
            self.__ui_functions.graph_functions.set_top_view)
        self.__ui.actionBottom.triggered.connect(
            self.__ui_functions.graph_functions.set_bottom_view)
        self.__ui.actionFront.triggered.connect(
            self.__ui_functions.graph_functions.set_front_view)
        self.__ui.actionBack.triggered.connect(
            self.__ui_functions.graph_functions.set_back_view)
        self.__ui.actionLeft.triggered.connect(
            self.__ui_functions.graph_functions.set_left_view)
        self.__ui.actionRight.triggered.connect(
            self.__ui_functions.graph_functions.set_right_view)

        self.__ui.actionFull_Solid.triggered.connect(
            self.__ui_functions.graph_functions.set_full_opacity)
        self.__ui.actionHalf_Transparent.triggered.connect(
            self.__ui_functions.graph_functions.self_half_opacity)

        self.__ui.actionTotal_Forces.triggered.connect(
            self.__ui_functions.graph_functions.plot_total_force)
        self.__ui.actionX_Forces.triggered.connect(
            self.__ui_functions.graph_functions.plot_x_force)
        self.__ui.actionY_Forces.triggered.connect(
            self.__ui_functions.graph_functions.plot_y_force)
        self.__ui.actionZ_Forces.triggered.connect(
            self.__ui_functions.graph_functions.plot_z_force)

        self.__ui.actionTotal_Displacement.triggered.connect(
            self.__ui_functions.graph_functions.plot_total_displacement)
        self.__ui.actionX_Displacement.triggered.connect(
            self.__ui_functions.graph_functions.plot_x_displacement)
        self.__ui.actionY_Displacement.triggered.connect(
            self.__ui_functions.graph_functions.plot_y_displacement)
        self.__ui.actionZ_Displacement.triggered.connect(
            self.__ui_functions.graph_functions.plot_z_displacement)

        self.__ui.actionVon_Misses_Stress.triggered.connect(
            self.__ui_functions.graph_functions.plot_von_misses_stress)
        self.__ui.actionVon_Misses_Strain.triggered.connect(
            self.__ui_functions.graph_functions.plot_von_misses_strain)
        self.__ui.actionVon_Misses_Energy.triggered.connect(
            self.__ui_functions.graph_functions.plot_von_misses_energy)

        self.__ui.actionSolve_Mathematical_Model.triggered.connect(
            self.__ui_functions.static_case_editor.get_mathematical_model)

        self.__ui.pushButton_bc_check.clicked.connect(
            self.__ui_functions.static_case_editor.update_choosen_nodes)
        self.__ui.pushButton_bc_clear.clicked.connect(
            self.__ui_functions.static_case_editor.clear_boundary_conditions)
        self.__ui.pushButton_bc_add.clicked.connect(
            self.__ui_functions.static_case_editor.set_boundary_conditions)


class OpenWindow(MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.__ui = Ui_OpenLattice_Lite()
        self.__ui.setupUi(self)

        self.__set_applications()
        self.__set_communication()
        self.show()

    def __set_applications(self):
        # self.__material_editor_application = MaterialEditorWindow()
        self.__static_application = StaticWindow()
        self.__homogenization_application = HomogenizationWindow()
        self.__optimization_application = None
        self.__reconstruct_application = None

    def __set_communication(self):
        # self.__ui.pushButton_material_data.clicked.connect(self.__run_material_editor_application)

        self.__ui.pushButton_static.clicked.connect(self.__run_static_application)
        self.__ui.pushButton_optimization.clicked.connect(self.__run_optimization_application)
        self.__ui.pushButton_homogenization.clicked.connect(self.__run_homogenization_application)
        # self.__ui.pushButton_reconstruction.clicked.connect(self.__run_homogenization_application)

    # def __run_material_editor_application(self):
    #     self.__material_editor_application.show()

    def __run_static_application(self):
        self.__static_application.show()

    def __run_optimization_application(self):
        pass

    def __run_homogenization_application(self):
        self.__homogenization_application.show()

    def __run_homogenization(self):
        pass
