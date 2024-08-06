# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'homogenization_interfaceNOsjnR.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_OpenLatticeHomogenization(object):
    def setupUi(self, OpenLatticeHomogenization):
        if not OpenLatticeHomogenization.objectName():
            OpenLatticeHomogenization.setObjectName(u"OpenLatticeHomogenization")
        OpenLatticeHomogenization.resize(1920, 1039)
        self.actionDesignerData = QAction(OpenLatticeHomogenization)
        self.actionDesignerData.setObjectName(u"actionDesignerData")
        self.actionHomogenizer = QAction(OpenLatticeHomogenization)
        self.actionHomogenizer.setObjectName(u"actionHomogenizer")
        self.actionDesignerMaterialProperties = QAction(OpenLatticeHomogenization)
        self.actionDesignerMaterialProperties.setObjectName(u"actionDesignerMaterialProperties")
        self.actionIsometric = QAction(OpenLatticeHomogenization)
        self.actionIsometric.setObjectName(u"actionIsometric")
        self.actionFront = QAction(OpenLatticeHomogenization)
        self.actionFront.setObjectName(u"actionFront")
        self.actionRight = QAction(OpenLatticeHomogenization)
        self.actionRight.setObjectName(u"actionRight")
        self.actionTop = QAction(OpenLatticeHomogenization)
        self.actionTop.setObjectName(u"actionTop")
        self.actionBack = QAction(OpenLatticeHomogenization)
        self.actionBack.setObjectName(u"actionBack")
        self.actionLeft = QAction(OpenLatticeHomogenization)
        self.actionLeft.setObjectName(u"actionLeft")
        self.actionBottom = QAction(OpenLatticeHomogenization)
        self.actionBottom.setObjectName(u"actionBottom")
        self.actionProject = QAction(OpenLatticeHomogenization)
        self.actionProject.setObjectName(u"actionProject")
        self.actionGeometry = QAction(OpenLatticeHomogenization)
        self.actionGeometry.setObjectName(u"actionGeometry")
        self.actionHomogenization_Results = QAction(OpenLatticeHomogenization)
        self.actionHomogenization_Results.setObjectName(u"actionHomogenization_Results")
        self.actionPicture = QAction(OpenLatticeHomogenization)
        self.actionPicture.setObjectName(u"actionPicture")
        self.actionProject_2 = QAction(OpenLatticeHomogenization)
        self.actionProject_2.setObjectName(u"actionProject_2")
        self.actionLattice = QAction(OpenLatticeHomogenization)
        self.actionLattice.setObjectName(u"actionLattice")
        self.actionHomogenizer_Data = QAction(OpenLatticeHomogenization)
        self.actionHomogenizer_Data.setObjectName(u"actionHomogenizer_Data")
        self.actionHomogenizer_Menu = QAction(OpenLatticeHomogenization)
        self.actionHomogenizer_Menu.setObjectName(u"actionHomogenizer_Menu")
        self.centralwidget = QWidget(OpenLatticeHomogenization)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.centralwidget)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 30))
        self.frame_top.setMaximumSize(QSize(16777215, 30))
        self.frame_top.setFrameShape(QFrame.StyledPanel)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_top_show_voxel = QPushButton(self.frame_top)
        self.pushButton_top_show_voxel.setObjectName(u"pushButton_top_show_voxel")

        self.horizontalLayout_2.addWidget(self.pushButton_top_show_voxel)

        self.pushButton_top_show_strut = QPushButton(self.frame_top)
        self.pushButton_top_show_strut.setObjectName(u"pushButton_top_show_strut")

        self.horizontalLayout_2.addWidget(self.pushButton_top_show_strut)

        self.comboBox_volumefraction_2 = QComboBox(self.frame_top)
        self.comboBox_volumefraction_2.addItem("")
        self.comboBox_volumefraction_2.setObjectName(u"comboBox_volumefraction_2")
        self.comboBox_volumefraction_2.setMinimumSize(QSize(70, 20))
        self.comboBox_volumefraction_2.setMaximumSize(QSize(70, 20))

        self.horizontalLayout_2.addWidget(self.comboBox_volumefraction_2)

        self.horizontalSpacer = QSpacerItem(1735, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.frame_top)

        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.StyledPanel)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_main)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.frame_homogenization = QFrame(self.frame_main)
        self.frame_homogenization.setObjectName(u"frame_homogenization")
        self.frame_homogenization.setMinimumSize(QSize(0, 0))
        self.frame_homogenization.setMaximumSize(QSize(0, 16777215))
        self.frame_homogenization.setFrameShape(QFrame.StyledPanel)
        self.frame_homogenization.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_homogenization)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.frame_homogenization_case_lists = QFrame(self.frame_homogenization)
        self.frame_homogenization_case_lists.setObjectName(u"frame_homogenization_case_lists")
        self.frame_homogenization_case_lists.setMinimumSize(QSize(300, 0))
        self.frame_homogenization_case_lists.setMaximumSize(QSize(300, 16777215))
        self.frame_homogenization_case_lists.setFrameShape(QFrame.StyledPanel)
        self.frame_homogenization_case_lists.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_homogenization_case_lists)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.tableWidget_homogenization_cases = QTableWidget(self.frame_homogenization_case_lists)
        if (self.tableWidget_homogenization_cases.columnCount() < 6):
            self.tableWidget_homogenization_cases.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_homogenization_cases.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_homogenization_cases.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_homogenization_cases.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_homogenization_cases.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_homogenization_cases.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_homogenization_cases.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tableWidget_homogenization_cases.setObjectName(u"tableWidget_homogenization_cases")
        self.tableWidget_homogenization_cases.setMinimumSize(QSize(0, 700))
        self.tableWidget_homogenization_cases.setMaximumSize(QSize(16777215, 700))
        self.tableWidget_homogenization_cases.horizontalHeader().setDefaultSectionSize(80)

        self.verticalLayout_5.addWidget(self.tableWidget_homogenization_cases)

        self.verticalSpacer_6 = QSpacerItem(20, 465, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_6)


        self.horizontalLayout_4.addWidget(self.frame_homogenization_case_lists)

        self.frame_homogenization_case_setup = QFrame(self.frame_homogenization)
        self.frame_homogenization_case_setup.setObjectName(u"frame_homogenization_case_setup")
        self.frame_homogenization_case_setup.setFrameShape(QFrame.StyledPanel)
        self.frame_homogenization_case_setup.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_homogenization_case_setup)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.pushButton_import_last_model = QPushButton(self.frame_homogenization_case_setup)
        self.pushButton_import_last_model.setObjectName(u"pushButton_import_last_model")

        self.verticalLayout_6.addWidget(self.pushButton_import_last_model)

        self.label_2 = QLabel(self.frame_homogenization_case_setup)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_6.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame_homogenization_case_setup)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_6.addWidget(self.label_3)

        self.lineEdit_thickness_from = QLineEdit(self.frame_homogenization_case_setup)
        self.lineEdit_thickness_from.setObjectName(u"lineEdit_thickness_from")

        self.verticalLayout_6.addWidget(self.lineEdit_thickness_from)

        self.lineEdit_thickness_to = QLineEdit(self.frame_homogenization_case_setup)
        self.lineEdit_thickness_to.setObjectName(u"lineEdit_thickness_to")

        self.verticalLayout_6.addWidget(self.lineEdit_thickness_to)

        self.lineEdit_thickness_number = QLineEdit(self.frame_homogenization_case_setup)
        self.lineEdit_thickness_number.setObjectName(u"lineEdit_thickness_number")

        self.verticalLayout_6.addWidget(self.lineEdit_thickness_number)

        self.pushButton_use_thickness_to_models = QPushButton(self.frame_homogenization_case_setup)
        self.pushButton_use_thickness_to_models.setObjectName(u"pushButton_use_thickness_to_models")

        self.verticalLayout_6.addWidget(self.pushButton_use_thickness_to_models)

        self.label_30 = QLabel(self.frame_homogenization_case_setup)
        self.label_30.setObjectName(u"label_30")

        self.verticalLayout_6.addWidget(self.label_30)

        self.lineEdit_vf_from = QLineEdit(self.frame_homogenization_case_setup)
        self.lineEdit_vf_from.setObjectName(u"lineEdit_vf_from")

        self.verticalLayout_6.addWidget(self.lineEdit_vf_from)

        self.lineEdit_vf_to = QLineEdit(self.frame_homogenization_case_setup)
        self.lineEdit_vf_to.setObjectName(u"lineEdit_vf_to")

        self.verticalLayout_6.addWidget(self.lineEdit_vf_to)

        self.lineEdit_vf_number = QLineEdit(self.frame_homogenization_case_setup)
        self.lineEdit_vf_number.setObjectName(u"lineEdit_vf_number")

        self.verticalLayout_6.addWidget(self.lineEdit_vf_number)

        self.pushButton_use_vf_to_models = QPushButton(self.frame_homogenization_case_setup)
        self.pushButton_use_vf_to_models.setObjectName(u"pushButton_use_vf_to_models")

        self.verticalLayout_6.addWidget(self.pushButton_use_vf_to_models)

        self.verticalSpacer_8 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_8)

        self.label_31 = QLabel(self.frame_homogenization_case_setup)
        self.label_31.setObjectName(u"label_31")

        self.verticalLayout_6.addWidget(self.label_31)

        self.lineEdit_unit_strain_from = QLineEdit(self.frame_homogenization_case_setup)
        self.lineEdit_unit_strain_from.setObjectName(u"lineEdit_unit_strain_from")

        self.verticalLayout_6.addWidget(self.lineEdit_unit_strain_from)

        self.lineEdit_unit_strain_to = QLineEdit(self.frame_homogenization_case_setup)
        self.lineEdit_unit_strain_to.setObjectName(u"lineEdit_unit_strain_to")

        self.verticalLayout_6.addWidget(self.lineEdit_unit_strain_to)

        self.lineEdit_unit_strain_number = QLineEdit(self.frame_homogenization_case_setup)
        self.lineEdit_unit_strain_number.setObjectName(u"lineEdit_unit_strain_number")

        self.verticalLayout_6.addWidget(self.lineEdit_unit_strain_number)

        self.verticalSpacer_9 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_9)

        self.pushButton_add_cases = QPushButton(self.frame_homogenization_case_setup)
        self.pushButton_add_cases.setObjectName(u"pushButton_add_cases")

        self.verticalLayout_6.addWidget(self.pushButton_add_cases)

        self.verticalSpacer_10 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_10)

        self.label_32 = QLabel(self.frame_homogenization_case_setup)
        self.label_32.setObjectName(u"label_32")

        self.verticalLayout_6.addWidget(self.label_32)

        self.lineEdit_remove_from = QLineEdit(self.frame_homogenization_case_setup)
        self.lineEdit_remove_from.setObjectName(u"lineEdit_remove_from")

        self.verticalLayout_6.addWidget(self.lineEdit_remove_from)

        self.lineEdit_remove_to = QLineEdit(self.frame_homogenization_case_setup)
        self.lineEdit_remove_to.setObjectName(u"lineEdit_remove_to")

        self.verticalLayout_6.addWidget(self.lineEdit_remove_to)

        self.pushButton_remove_cases = QPushButton(self.frame_homogenization_case_setup)
        self.pushButton_remove_cases.setObjectName(u"pushButton_remove_cases")

        self.verticalLayout_6.addWidget(self.pushButton_remove_cases)

        self.verticalSpacer_11 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_11)

        self.pushButton_start_homogenize = QPushButton(self.frame_homogenization_case_setup)
        self.pushButton_start_homogenize.setObjectName(u"pushButton_start_homogenize")

        self.verticalLayout_6.addWidget(self.pushButton_start_homogenize)

        self.verticalSpacer_7 = QSpacerItem(20, 268, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_7)


        self.horizontalLayout_4.addWidget(self.frame_homogenization_case_setup)


        self.horizontalLayout.addWidget(self.frame_homogenization)

        self.frame_strut_lattice_designer = QFrame(self.frame_main)
        self.frame_strut_lattice_designer.setObjectName(u"frame_strut_lattice_designer")
        self.frame_strut_lattice_designer.setMinimumSize(QSize(0, 0))
        self.frame_strut_lattice_designer.setMaximumSize(QSize(0, 16777215))
        self.frame_strut_lattice_designer.setFrameShape(QFrame.StyledPanel)
        self.frame_strut_lattice_designer.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_strut_lattice_designer)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.frame_strut_lister = QFrame(self.frame_strut_lattice_designer)
        self.frame_strut_lister.setObjectName(u"frame_strut_lister")
        self.frame_strut_lister.setMinimumSize(QSize(300, 0))
        self.frame_strut_lister.setMaximumSize(QSize(300, 16777215))
        self.frame_strut_lister.setFrameShape(QFrame.StyledPanel)
        self.frame_strut_lister.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_strut_lister)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.tableWidget_node = QTableWidget(self.frame_strut_lister)
        if (self.tableWidget_node.columnCount() < 4):
            self.tableWidget_node.setColumnCount(4)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(3, __qtablewidgetitem9)
        self.tableWidget_node.setObjectName(u"tableWidget_node")
        self.tableWidget_node.setMinimumSize(QSize(0, 350))
        self.tableWidget_node.setMaximumSize(QSize(16777215, 350))
        self.tableWidget_node.horizontalHeader().setDefaultSectionSize(80)

        self.verticalLayout_2.addWidget(self.tableWidget_node)

        self.tableWidget_strut = QTableWidget(self.frame_strut_lister)
        if (self.tableWidget_strut.columnCount() < 5):
            self.tableWidget_strut.setColumnCount(5)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(4, __qtablewidgetitem14)
        self.tableWidget_strut.setObjectName(u"tableWidget_strut")
        self.tableWidget_strut.setMinimumSize(QSize(0, 350))
        self.tableWidget_strut.setMaximumSize(QSize(16777215, 350))
        self.tableWidget_strut.horizontalHeader().setDefaultSectionSize(50)

        self.verticalLayout_2.addWidget(self.tableWidget_strut)

        self.tableWidget_material = QTableWidget(self.frame_strut_lister)
        if (self.tableWidget_material.columnCount() < 9):
            self.tableWidget_material.setColumnCount(9)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(2, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(3, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(4, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(5, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(6, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(7, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(8, __qtablewidgetitem23)
        self.tableWidget_material.setObjectName(u"tableWidget_material")
        self.tableWidget_material.setMinimumSize(QSize(0, 100))
        self.tableWidget_material.setMaximumSize(QSize(16777215, 100))
        self.tableWidget_material.horizontalHeader().setDefaultSectionSize(50)

        self.verticalLayout_2.addWidget(self.tableWidget_material)

        self.label_25 = QLabel(self.frame_strut_lister)
        self.label_25.setObjectName(u"label_25")

        self.verticalLayout_2.addWidget(self.label_25)

        self.spinBox_model_resolution = QSpinBox(self.frame_strut_lister)
        self.spinBox_model_resolution.setObjectName(u"spinBox_model_resolution")
        self.spinBox_model_resolution.setMinimum(10)
        self.spinBox_model_resolution.setMaximum(200)
        self.spinBox_model_resolution.setValue(50)

        self.verticalLayout_2.addWidget(self.spinBox_model_resolution)

        self.pushButton_regenerate_model = QPushButton(self.frame_strut_lister)
        self.pushButton_regenerate_model.setObjectName(u"pushButton_regenerate_model")

        self.verticalLayout_2.addWidget(self.pushButton_regenerate_model)

        self.pushButton_save_model = QPushButton(self.frame_strut_lister)
        self.pushButton_save_model.setObjectName(u"pushButton_save_model")

        self.verticalLayout_2.addWidget(self.pushButton_save_model)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_12)


        self.horizontalLayout_3.addWidget(self.frame_strut_lister)

        self.frame_strut_designer = QFrame(self.frame_strut_lattice_designer)
        self.frame_strut_designer.setObjectName(u"frame_strut_designer")
        self.frame_strut_designer.setMaximumSize(QSize(150, 16777215))
        self.frame_strut_designer.setFrameShape(QFrame.StyledPanel)
        self.frame_strut_designer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_strut_designer)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.label = QLabel(self.frame_strut_designer)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.comboBox_model_types = QComboBox(self.frame_strut_designer)
        self.comboBox_model_types.addItem("")
        self.comboBox_model_types.addItem("")
        self.comboBox_model_types.addItem("")
        self.comboBox_model_types.addItem("")
        self.comboBox_model_types.addItem("")
        self.comboBox_model_types.addItem("")
        self.comboBox_model_types.addItem("")
        self.comboBox_model_types.setObjectName(u"comboBox_model_types")

        self.verticalLayout_3.addWidget(self.comboBox_model_types)

        self.pushButton_model_get = QPushButton(self.frame_strut_designer)
        self.pushButton_model_get.setObjectName(u"pushButton_model_get")

        self.verticalLayout_3.addWidget(self.pushButton_model_get)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.label_4 = QLabel(self.frame_strut_designer)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.label_5 = QLabel(self.frame_strut_designer)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_3.addWidget(self.label_5)

        self.spinBox_node_name = QSpinBox(self.frame_strut_designer)
        self.spinBox_node_name.setObjectName(u"spinBox_node_name")
        self.spinBox_node_name.setMinimum(1)
        self.spinBox_node_name.setMaximum(1000)

        self.verticalLayout_3.addWidget(self.spinBox_node_name)

        self.label_6 = QLabel(self.frame_strut_designer)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_3.addWidget(self.label_6)

        self.lineEdit_node_x = QLineEdit(self.frame_strut_designer)
        self.lineEdit_node_x.setObjectName(u"lineEdit_node_x")

        self.verticalLayout_3.addWidget(self.lineEdit_node_x)

        self.label_7 = QLabel(self.frame_strut_designer)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_3.addWidget(self.label_7)

        self.lineEdit_node_y = QLineEdit(self.frame_strut_designer)
        self.lineEdit_node_y.setObjectName(u"lineEdit_node_y")

        self.verticalLayout_3.addWidget(self.lineEdit_node_y)

        self.label_8 = QLabel(self.frame_strut_designer)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_3.addWidget(self.label_8)

        self.lineEdit_node_z = QLineEdit(self.frame_strut_designer)
        self.lineEdit_node_z.setObjectName(u"lineEdit_node_z")

        self.verticalLayout_3.addWidget(self.lineEdit_node_z)

        self.pushButton_add_node = QPushButton(self.frame_strut_designer)
        self.pushButton_add_node.setObjectName(u"pushButton_add_node")

        self.verticalLayout_3.addWidget(self.pushButton_add_node)

        self.comboBox_node_remove = QComboBox(self.frame_strut_designer)
        self.comboBox_node_remove.setObjectName(u"comboBox_node_remove")

        self.verticalLayout_3.addWidget(self.comboBox_node_remove)

        self.pushButton_node_remove = QPushButton(self.frame_strut_designer)
        self.pushButton_node_remove.setObjectName(u"pushButton_node_remove")

        self.verticalLayout_3.addWidget(self.pushButton_node_remove)

        self.verticalSpacer_3 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.label_9 = QLabel(self.frame_strut_designer)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_3.addWidget(self.label_9)

        self.label_10 = QLabel(self.frame_strut_designer)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_3.addWidget(self.label_10)

        self.spinBox_strut_name = QSpinBox(self.frame_strut_designer)
        self.spinBox_strut_name.setObjectName(u"spinBox_strut_name")
        self.spinBox_strut_name.setMinimum(1)
        self.spinBox_strut_name.setMaximum(1000)

        self.verticalLayout_3.addWidget(self.spinBox_strut_name)

        self.label_11 = QLabel(self.frame_strut_designer)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_3.addWidget(self.label_11)

        self.lineEdit_strut_start_node_id = QLineEdit(self.frame_strut_designer)
        self.lineEdit_strut_start_node_id.setObjectName(u"lineEdit_strut_start_node_id")

        self.verticalLayout_3.addWidget(self.lineEdit_strut_start_node_id)

        self.label_12 = QLabel(self.frame_strut_designer)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_3.addWidget(self.label_12)

        self.lineEdit_strut_end_node_id = QLineEdit(self.frame_strut_designer)
        self.lineEdit_strut_end_node_id.setObjectName(u"lineEdit_strut_end_node_id")

        self.verticalLayout_3.addWidget(self.lineEdit_strut_end_node_id)

        self.label_13 = QLabel(self.frame_strut_designer)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_3.addWidget(self.label_13)

        self.lineEdit_strut_material_id = QLineEdit(self.frame_strut_designer)
        self.lineEdit_strut_material_id.setObjectName(u"lineEdit_strut_material_id")

        self.verticalLayout_3.addWidget(self.lineEdit_strut_material_id)

        self.label_14 = QLabel(self.frame_strut_designer)
        self.label_14.setObjectName(u"label_14")

        self.verticalLayout_3.addWidget(self.label_14)

        self.lineEdit_strut_radius = QLineEdit(self.frame_strut_designer)
        self.lineEdit_strut_radius.setObjectName(u"lineEdit_strut_radius")

        self.verticalLayout_3.addWidget(self.lineEdit_strut_radius)

        self.pushButton_strut_add = QPushButton(self.frame_strut_designer)
        self.pushButton_strut_add.setObjectName(u"pushButton_strut_add")

        self.verticalLayout_3.addWidget(self.pushButton_strut_add)

        self.comboBox_strut_remove = QComboBox(self.frame_strut_designer)
        self.comboBox_strut_remove.setObjectName(u"comboBox_strut_remove")

        self.verticalLayout_3.addWidget(self.comboBox_strut_remove)

        self.pushButton_strut_remove = QPushButton(self.frame_strut_designer)
        self.pushButton_strut_remove.setObjectName(u"pushButton_strut_remove")

        self.verticalLayout_3.addWidget(self.pushButton_strut_remove)

        self.verticalSpacer_5 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_5)

        self.label_26 = QLabel(self.frame_strut_designer)
        self.label_26.setObjectName(u"label_26")

        self.verticalLayout_3.addWidget(self.label_26)

        self.label_27 = QLabel(self.frame_strut_designer)
        self.label_27.setObjectName(u"label_27")

        self.verticalLayout_3.addWidget(self.label_27)

        self.spinBox_model_size_x = QSpinBox(self.frame_strut_designer)
        self.spinBox_model_size_x.setObjectName(u"spinBox_model_size_x")
        self.spinBox_model_size_x.setValue(10)

        self.verticalLayout_3.addWidget(self.spinBox_model_size_x)

        self.label_28 = QLabel(self.frame_strut_designer)
        self.label_28.setObjectName(u"label_28")

        self.verticalLayout_3.addWidget(self.label_28)

        self.spinBox_model_size_y = QSpinBox(self.frame_strut_designer)
        self.spinBox_model_size_y.setObjectName(u"spinBox_model_size_y")
        self.spinBox_model_size_y.setValue(10)

        self.verticalLayout_3.addWidget(self.spinBox_model_size_y)

        self.label_29 = QLabel(self.frame_strut_designer)
        self.label_29.setObjectName(u"label_29")

        self.verticalLayout_3.addWidget(self.label_29)

        self.spinBox_model_size_z = QSpinBox(self.frame_strut_designer)
        self.spinBox_model_size_z.setObjectName(u"spinBox_model_size_z")
        self.spinBox_model_size_z.setValue(10)

        self.verticalLayout_3.addWidget(self.spinBox_model_size_z)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.horizontalLayout_3.addWidget(self.frame_strut_designer)

        self.frame_material = QFrame(self.frame_strut_lattice_designer)
        self.frame_material.setObjectName(u"frame_material")
        self.frame_material.setMaximumSize(QSize(150, 16777215))
        self.frame_material.setFrameShape(QFrame.StyledPanel)
        self.frame_material.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_material)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.label_15 = QLabel(self.frame_material)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout_4.addWidget(self.label_15)

        self.label_16 = QLabel(self.frame_material)
        self.label_16.setObjectName(u"label_16")

        self.verticalLayout_4.addWidget(self.label_16)

        self.spinBox_material_id = QSpinBox(self.frame_material)
        self.spinBox_material_id.setObjectName(u"spinBox_material_id")
        self.spinBox_material_id.setMinimum(1)
        self.spinBox_material_id.setMaximum(1000)

        self.verticalLayout_4.addWidget(self.spinBox_material_id)

        self.label_17 = QLabel(self.frame_material)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_4.addWidget(self.label_17)

        self.lineEdit_material_name = QLineEdit(self.frame_material)
        self.lineEdit_material_name.setObjectName(u"lineEdit_material_name")

        self.verticalLayout_4.addWidget(self.lineEdit_material_name)

        self.label_18 = QLabel(self.frame_material)
        self.label_18.setObjectName(u"label_18")

        self.verticalLayout_4.addWidget(self.label_18)

        self.lineEdit_modulus_of_elasticity = QLineEdit(self.frame_material)
        self.lineEdit_modulus_of_elasticity.setObjectName(u"lineEdit_modulus_of_elasticity")

        self.verticalLayout_4.addWidget(self.lineEdit_modulus_of_elasticity)

        self.label_19 = QLabel(self.frame_material)
        self.label_19.setObjectName(u"label_19")

        self.verticalLayout_4.addWidget(self.label_19)

        self.lineEdit_poissons_ratio = QLineEdit(self.frame_material)
        self.lineEdit_poissons_ratio.setObjectName(u"lineEdit_poissons_ratio")

        self.verticalLayout_4.addWidget(self.lineEdit_poissons_ratio)

        self.label_20 = QLabel(self.frame_material)
        self.label_20.setObjectName(u"label_20")

        self.verticalLayout_4.addWidget(self.label_20)

        self.lineEdit_thermal_conductivity = QLineEdit(self.frame_material)
        self.lineEdit_thermal_conductivity.setObjectName(u"lineEdit_thermal_conductivity")

        self.verticalLayout_4.addWidget(self.lineEdit_thermal_conductivity)

        self.label_21 = QLabel(self.frame_material)
        self.label_21.setObjectName(u"label_21")

        self.verticalLayout_4.addWidget(self.label_21)

        self.lineEdit_yield_stress = QLineEdit(self.frame_material)
        self.lineEdit_yield_stress.setObjectName(u"lineEdit_yield_stress")

        self.verticalLayout_4.addWidget(self.lineEdit_yield_stress)

        self.label_22 = QLabel(self.frame_material)
        self.label_22.setObjectName(u"label_22")

        self.verticalLayout_4.addWidget(self.label_22)

        self.lineEdit_yield_strain = QLineEdit(self.frame_material)
        self.lineEdit_yield_strain.setObjectName(u"lineEdit_yield_strain")

        self.verticalLayout_4.addWidget(self.lineEdit_yield_strain)

        self.label_23 = QLabel(self.frame_material)
        self.label_23.setObjectName(u"label_23")

        self.verticalLayout_4.addWidget(self.label_23)

        self.lineEdit_ultimate_stress = QLineEdit(self.frame_material)
        self.lineEdit_ultimate_stress.setObjectName(u"lineEdit_ultimate_stress")

        self.verticalLayout_4.addWidget(self.lineEdit_ultimate_stress)

        self.label_24 = QLabel(self.frame_material)
        self.label_24.setObjectName(u"label_24")

        self.verticalLayout_4.addWidget(self.label_24)

        self.lineEdit_ultimate_strain = QLineEdit(self.frame_material)
        self.lineEdit_ultimate_strain.setObjectName(u"lineEdit_ultimate_strain")

        self.verticalLayout_4.addWidget(self.lineEdit_ultimate_strain)

        self.pushButton_material_add = QPushButton(self.frame_material)
        self.pushButton_material_add.setObjectName(u"pushButton_material_add")

        self.verticalLayout_4.addWidget(self.pushButton_material_add)

        self.comboBox_material_remove = QComboBox(self.frame_material)
        self.comboBox_material_remove.setObjectName(u"comboBox_material_remove")

        self.verticalLayout_4.addWidget(self.comboBox_material_remove)

        self.pushButton_material_remove = QPushButton(self.frame_material)
        self.pushButton_material_remove.setObjectName(u"pushButton_material_remove")

        self.verticalLayout_4.addWidget(self.pushButton_material_remove)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)


        self.horizontalLayout_3.addWidget(self.frame_material)


        self.horizontalLayout.addWidget(self.frame_strut_lattice_designer)

        self.frame_fem_preprocessor = QFrame(self.frame_main)
        self.frame_fem_preprocessor.setObjectName(u"frame_fem_preprocessor")
        self.frame_fem_preprocessor.setMaximumSize(QSize(0, 16777215))
        self.frame_fem_preprocessor.setFrameShape(QFrame.StyledPanel)
        self.frame_fem_preprocessor.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.frame_fem_preprocessor)

        self.frame_vista = QFrame(self.frame_main)
        self.frame_vista.setObjectName(u"frame_vista")
        self.frame_vista.setFrameShape(QFrame.StyledPanel)
        self.frame_vista.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.frame_vista)

        self.frame_graph = QFrame(self.frame_main)
        self.frame_graph.setObjectName(u"frame_graph")
        self.frame_graph.setMaximumSize(QSize(0, 16777215))
        self.frame_graph.setFrameShape(QFrame.StyledPanel)
        self.frame_graph.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.frame_graph)


        self.verticalLayout.addWidget(self.frame_main)

        OpenLatticeHomogenization.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(OpenLatticeHomogenization)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1920, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSave = QMenu(self.menuFile)
        self.menuSave.setObjectName(u"menuSave")
        self.menuLattice_Model = QMenu(self.menuSave)
        self.menuLattice_Model.setObjectName(u"menuLattice_Model")
        self.menuImport = QMenu(self.menuFile)
        self.menuImport.setObjectName(u"menuImport")
        self.menuModules = QMenu(self.menubar)
        self.menuModules.setObjectName(u"menuModules")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuView_Angle = QMenu(self.menuView)
        self.menuView_Angle.setObjectName(u"menuView_Angle")
        OpenLatticeHomogenization.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuModules.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.menuSave.menuAction())
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addAction(self.actionPicture)
        self.menuSave.addAction(self.actionProject)
        self.menuSave.addAction(self.menuLattice_Model.menuAction())
        self.menuLattice_Model.addAction(self.actionGeometry)
        self.menuLattice_Model.addAction(self.actionHomogenization_Results)
        self.menuImport.addAction(self.actionProject_2)
        self.menuImport.addAction(self.actionLattice)
        self.menuModules.addAction(self.actionDesignerData)
        self.menuModules.addAction(self.actionHomogenizer)
        self.menuView.addAction(self.menuView_Angle.menuAction())
        self.menuView_Angle.addAction(self.actionIsometric)
        self.menuView_Angle.addAction(self.actionFront)
        self.menuView_Angle.addAction(self.actionRight)
        self.menuView_Angle.addAction(self.actionTop)
        self.menuView_Angle.addAction(self.actionBack)
        self.menuView_Angle.addAction(self.actionLeft)
        self.menuView_Angle.addAction(self.actionBottom)

        self.retranslateUi(OpenLatticeHomogenization)

        QMetaObject.connectSlotsByName(OpenLatticeHomogenization)
    # setupUi

    def retranslateUi(self, OpenLatticeHomogenization):
        OpenLatticeHomogenization.setWindowTitle(QCoreApplication.translate("OpenLatticeHomogenization", u"OpenLattice Homogenization", None))
        self.actionDesignerData.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Strut Designer", None))
        self.actionHomogenizer.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Homogenizer", None))
        self.actionDesignerMaterialProperties.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Designer Material Properties", None))
        self.actionIsometric.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Isometric", None))
        self.actionFront.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Front", None))
        self.actionRight.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Right", None))
        self.actionTop.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Top", None))
        self.actionBack.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Back", None))
        self.actionLeft.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Left", None))
        self.actionBottom.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Bottom", None))
        self.actionProject.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Project", None))
        self.actionGeometry.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Geometry", None))
        self.actionHomogenization_Results.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Homogenization Results", None))
        self.actionPicture.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Picture", None))
        self.actionProject_2.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Project", None))
        self.actionLattice.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Lattice", None))
        self.actionHomogenizer_Data.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Homogenizer Data", None))
        self.actionHomogenizer_Menu.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Homogenizer Menu", None))
        self.pushButton_top_show_voxel.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Show Voxel", None))
        self.pushButton_top_show_strut.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Show Strut", None))
        self.comboBox_volumefraction_2.setItemText(0, QCoreApplication.translate("OpenLatticeHomogenization", u"No VF", None))

        ___qtablewidgetitem = self.tableWidget_homogenization_cases.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Case Number", None));
        ___qtablewidgetitem1 = self.tableWidget_homogenization_cases.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Topology Name", None));
        ___qtablewidgetitem2 = self.tableWidget_homogenization_cases.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Strut thickness", None));
        ___qtablewidgetitem3 = self.tableWidget_homogenization_cases.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Volume Fraction", None));
        ___qtablewidgetitem4 = self.tableWidget_homogenization_cases.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Displacement", None));
        ___qtablewidgetitem5 = self.tableWidget_homogenization_cases.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Status", None));
        self.pushButton_import_last_model.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Import Last Model", None))
        self.label_2.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Volume Fraction", None))
        self.label_3.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Thickness to Models", None))
        self.lineEdit_thickness_from.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0.1", None))
        self.lineEdit_thickness_from.setPlaceholderText(QCoreApplication.translate("OpenLatticeHomogenization", u"From", None))
        self.lineEdit_thickness_to.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0.1", None))
        self.lineEdit_thickness_to.setPlaceholderText(QCoreApplication.translate("OpenLatticeHomogenization", u"To", None))
        self.lineEdit_thickness_number.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"1", None))
        self.lineEdit_thickness_number.setPlaceholderText(QCoreApplication.translate("OpenLatticeHomogenization", u"Number", None))
        self.pushButton_use_thickness_to_models.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Use Thickness to Models", None))
        self.label_30.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Volume Fraction to Models", None))
        self.lineEdit_vf_from.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0.1", None))
        self.lineEdit_vf_from.setPlaceholderText(QCoreApplication.translate("OpenLatticeHomogenization", u"From", None))
        self.lineEdit_vf_to.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0.1", None))
        self.lineEdit_vf_to.setPlaceholderText(QCoreApplication.translate("OpenLatticeHomogenization", u"To", None))
        self.lineEdit_vf_number.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"1", None))
        self.lineEdit_vf_number.setPlaceholderText(QCoreApplication.translate("OpenLatticeHomogenization", u"Number", None))
        self.pushButton_use_vf_to_models.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Use Volume Fraction to Models", None))
        self.label_31.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Unit Strain Displacement", None))
        self.lineEdit_unit_strain_from.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0.001", None))
        self.lineEdit_unit_strain_from.setPlaceholderText(QCoreApplication.translate("OpenLatticeHomogenization", u"From", None))
        self.lineEdit_unit_strain_to.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0.001", None))
        self.lineEdit_unit_strain_to.setPlaceholderText(QCoreApplication.translate("OpenLatticeHomogenization", u"To", None))
        self.lineEdit_unit_strain_number.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"1", None))
        self.lineEdit_unit_strain_number.setPlaceholderText(QCoreApplication.translate("OpenLatticeHomogenization", u"Number", None))
        self.pushButton_add_cases.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Add Cases", None))
        self.label_32.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Remove Cases", None))
        self.lineEdit_remove_from.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"1", None))
        self.lineEdit_remove_to.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"1", None))
        self.pushButton_remove_cases.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Remove Cases", None))
        self.pushButton_start_homogenize.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Start Homogenize", None))
        ___qtablewidgetitem6 = self.tableWidget_node.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Name", None));
        ___qtablewidgetitem7 = self.tableWidget_node.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"X", None));
        ___qtablewidgetitem8 = self.tableWidget_node.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Y", None));
        ___qtablewidgetitem9 = self.tableWidget_node.horizontalHeaderItem(3)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Z", None));
        ___qtablewidgetitem10 = self.tableWidget_strut.horizontalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Name", None));
        ___qtablewidgetitem11 = self.tableWidget_strut.horizontalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Start Node", None));
        ___qtablewidgetitem12 = self.tableWidget_strut.horizontalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"End Node", None));
        ___qtablewidgetitem13 = self.tableWidget_strut.horizontalHeaderItem(3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Material", None));
        ___qtablewidgetitem14 = self.tableWidget_strut.horizontalHeaderItem(4)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Radius", None));
        ___qtablewidgetitem15 = self.tableWidget_material.horizontalHeaderItem(0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"ID", None));
        ___qtablewidgetitem16 = self.tableWidget_material.horizontalHeaderItem(1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Name", None));
        ___qtablewidgetitem17 = self.tableWidget_material.horizontalHeaderItem(2)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Modulus of Elasticity", None));
        ___qtablewidgetitem18 = self.tableWidget_material.horizontalHeaderItem(3)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Poisson's Ratio", None));
        ___qtablewidgetitem19 = self.tableWidget_material.horizontalHeaderItem(4)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Yield Stress", None));
        ___qtablewidgetitem20 = self.tableWidget_material.horizontalHeaderItem(5)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Ultimate Stress", None));
        ___qtablewidgetitem21 = self.tableWidget_material.horizontalHeaderItem(6)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Yield Strain", None));
        ___qtablewidgetitem22 = self.tableWidget_material.horizontalHeaderItem(7)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Ultimate Strain", None));
        ___qtablewidgetitem23 = self.tableWidget_material.horizontalHeaderItem(8)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Thermal Conductivity", None));
        self.label_25.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Resolution", None))
        self.pushButton_regenerate_model.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"ReGenerate", None))
        self.pushButton_save_model.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Save", None))
        self.label.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Standart Models", None))
        self.comboBox_model_types.setItemText(0, QCoreApplication.translate("OpenLatticeHomogenization", u"Grid", None))
        self.comboBox_model_types.setItemText(1, QCoreApplication.translate("OpenLatticeHomogenization", u"Octet", None))
        self.comboBox_model_types.setItemText(2, QCoreApplication.translate("OpenLatticeHomogenization", u"X", None))
        self.comboBox_model_types.setItemText(3, QCoreApplication.translate("OpenLatticeHomogenization", u"Face Center", None))
        self.comboBox_model_types.setItemText(4, QCoreApplication.translate("OpenLatticeHomogenization", u"Cubic Center", None))
        self.comboBox_model_types.setItemText(5, QCoreApplication.translate("OpenLatticeHomogenization", u"Butterfly", None))
        self.comboBox_model_types.setItemText(6, QCoreApplication.translate("OpenLatticeHomogenization", u"From *.lif", None))

        self.pushButton_model_get.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Get", None))
        self.label_4.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Nodes", None))
        self.label_5.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Name", None))
        self.label_6.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"X", None))
        self.lineEdit_node_x.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0", None))
        self.label_7.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Y", None))
        self.lineEdit_node_y.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0", None))
        self.label_8.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Z", None))
        self.lineEdit_node_z.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0", None))
        self.pushButton_add_node.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Add", None))
        self.pushButton_node_remove.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Remove", None))
        self.label_9.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Strut", None))
        self.label_10.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Name", None))
        self.label_11.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Start Node", None))
        self.lineEdit_strut_start_node_id.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"1", None))
        self.label_12.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"End Node", None))
        self.lineEdit_strut_end_node_id.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"2", None))
        self.label_13.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Material ID", None))
        self.lineEdit_strut_material_id.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"1", None))
        self.label_14.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Radius", None))
        self.lineEdit_strut_radius.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0.1", None))
        self.pushButton_strut_add.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Add", None))
        self.pushButton_strut_remove.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Remove", None))
        self.label_26.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Size", None))
        self.label_27.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"X", None))
        self.label_28.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Y", None))
        self.label_29.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Z", None))
        self.label_15.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Material", None))
        self.label_16.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"ID", None))
        self.label_17.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Name", None))
        self.lineEdit_material_name.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Steel", None))
        self.label_18.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Modulus of Elasticity", None))
        self.lineEdit_modulus_of_elasticity.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"210000", None))
        self.label_19.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Poisson's Ratio", None))
        self.lineEdit_poissons_ratio.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0.3", None))
        self.label_20.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Thermal Conductivity", None))
        self.lineEdit_thermal_conductivity.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"65.3", None))
        self.label_21.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Yield Stress", None))
        self.lineEdit_yield_stress.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"370", None))
        self.label_22.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Yield Strain", None))
        self.lineEdit_yield_strain.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0.002", None))
        self.label_23.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Ultimate Stress", None))
        self.lineEdit_ultimate_stress.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"420", None))
        self.label_24.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Ultimate Strain", None))
        self.lineEdit_ultimate_strain.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"0.3", None))
        self.pushButton_material_add.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Add", None))
        self.pushButton_material_remove.setText(QCoreApplication.translate("OpenLatticeHomogenization", u"Remove", None))
        self.menuFile.setTitle(QCoreApplication.translate("OpenLatticeHomogenization", u"File", None))
        self.menuSave.setTitle(QCoreApplication.translate("OpenLatticeHomogenization", u"Save", None))
        self.menuLattice_Model.setTitle(QCoreApplication.translate("OpenLatticeHomogenization", u"Lattice Model", None))
        self.menuImport.setTitle(QCoreApplication.translate("OpenLatticeHomogenization", u"Import", None))
        self.menuModules.setTitle(QCoreApplication.translate("OpenLatticeHomogenization", u"Modules", None))
        self.menuView.setTitle(QCoreApplication.translate("OpenLatticeHomogenization", u"View", None))
        self.menuView_Angle.setTitle(QCoreApplication.translate("OpenLatticeHomogenization", u"View Angle", None))
    # retranslateUi

