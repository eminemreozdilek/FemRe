# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'material_editorsDxYJN.ui'
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

class Ui_OpenLatticeMaterialEditor(object):
    def setupUi(self, OpenLatticeMaterialEditor):
        if not OpenLatticeMaterialEditor.objectName():
            OpenLatticeMaterialEditor.setObjectName(u"OpenLatticeMaterialEditor")
        OpenLatticeMaterialEditor.resize(1920, 1000)
        OpenLatticeMaterialEditor.setMinimumSize(QSize(800, 600))
        OpenLatticeMaterialEditor.setMaximumSize(QSize(1920, 1000))
        self.actionImport = QAction(OpenLatticeMaterialEditor)
        self.actionImport.setObjectName(u"actionImport")
        self.actionExport = QAction(OpenLatticeMaterialEditor)
        self.actionExport.setObjectName(u"actionExport")
        self.actionTable = QAction(OpenLatticeMaterialEditor)
        self.actionTable.setObjectName(u"actionTable")
        self.actionGraph = QAction(OpenLatticeMaterialEditor)
        self.actionGraph.setObjectName(u"actionGraph")
        self.actionNew = QAction(OpenLatticeMaterialEditor)
        self.actionNew.setObjectName(u"actionNew")
        self.actionClear = QAction(OpenLatticeMaterialEditor)
        self.actionClear.setObjectName(u"actionClear")
        self.actionShow_Grid = QAction(OpenLatticeMaterialEditor)
        self.actionShow_Grid.setObjectName(u"actionShow_Grid")
        self.actionHide_Grid = QAction(OpenLatticeMaterialEditor)
        self.actionHide_Grid.setObjectName(u"actionHide_Grid")
        self.centralwidget = QWidget(OpenLatticeMaterialEditor)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_material_settings = QFrame(self.centralwidget)
        self.frame_material_settings.setObjectName(u"frame_material_settings")
        self.frame_material_settings.setMaximumSize(QSize(150, 16777215))
        self.frame_material_settings.setFrameShape(QFrame.StyledPanel)
        self.frame_material_settings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_material_settings)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.label_15 = QLabel(self.frame_material_settings)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout_3.addWidget(self.label_15)

        self.label_16 = QLabel(self.frame_material_settings)
        self.label_16.setObjectName(u"label_16")

        self.verticalLayout_3.addWidget(self.label_16)

        self.spinBox_material_id = QSpinBox(self.frame_material_settings)
        self.spinBox_material_id.setObjectName(u"spinBox_material_id")
        self.spinBox_material_id.setMinimum(1)
        self.spinBox_material_id.setMaximum(1000)

        self.verticalLayout_3.addWidget(self.spinBox_material_id)

        self.label_17 = QLabel(self.frame_material_settings)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_3.addWidget(self.label_17)

        self.lineEdit_material_name = QLineEdit(self.frame_material_settings)
        self.lineEdit_material_name.setObjectName(u"lineEdit_material_name")

        self.verticalLayout_3.addWidget(self.lineEdit_material_name)

        self.label_18 = QLabel(self.frame_material_settings)
        self.label_18.setObjectName(u"label_18")

        self.verticalLayout_3.addWidget(self.label_18)

        self.lineEdit_modulus_of_elasticity = QLineEdit(self.frame_material_settings)
        self.lineEdit_modulus_of_elasticity.setObjectName(u"lineEdit_modulus_of_elasticity")

        self.verticalLayout_3.addWidget(self.lineEdit_modulus_of_elasticity)

        self.label_19 = QLabel(self.frame_material_settings)
        self.label_19.setObjectName(u"label_19")

        self.verticalLayout_3.addWidget(self.label_19)

        self.lineEdit_poissons_ratio = QLineEdit(self.frame_material_settings)
        self.lineEdit_poissons_ratio.setObjectName(u"lineEdit_poissons_ratio")

        self.verticalLayout_3.addWidget(self.lineEdit_poissons_ratio)

        self.label_21 = QLabel(self.frame_material_settings)
        self.label_21.setObjectName(u"label_21")

        self.verticalLayout_3.addWidget(self.label_21)

        self.lineEdit_yield_stress = QLineEdit(self.frame_material_settings)
        self.lineEdit_yield_stress.setObjectName(u"lineEdit_yield_stress")

        self.verticalLayout_3.addWidget(self.lineEdit_yield_stress)

        self.label_23 = QLabel(self.frame_material_settings)
        self.label_23.setObjectName(u"label_23")

        self.verticalLayout_3.addWidget(self.label_23)

        self.lineEdit_ultimate_stress = QLineEdit(self.frame_material_settings)
        self.lineEdit_ultimate_stress.setObjectName(u"lineEdit_ultimate_stress")

        self.verticalLayout_3.addWidget(self.lineEdit_ultimate_stress)

        self.label_22 = QLabel(self.frame_material_settings)
        self.label_22.setObjectName(u"label_22")

        self.verticalLayout_3.addWidget(self.label_22)

        self.lineEdit_yield_strain = QLineEdit(self.frame_material_settings)
        self.lineEdit_yield_strain.setObjectName(u"lineEdit_yield_strain")

        self.verticalLayout_3.addWidget(self.lineEdit_yield_strain)

        self.label_24 = QLabel(self.frame_material_settings)
        self.label_24.setObjectName(u"label_24")

        self.verticalLayout_3.addWidget(self.label_24)

        self.lineEdit_ultimate_strain = QLineEdit(self.frame_material_settings)
        self.lineEdit_ultimate_strain.setObjectName(u"lineEdit_ultimate_strain")

        self.verticalLayout_3.addWidget(self.lineEdit_ultimate_strain)

        self.label_20 = QLabel(self.frame_material_settings)
        self.label_20.setObjectName(u"label_20")

        self.verticalLayout_3.addWidget(self.label_20)

        self.lineEdit_thermal_conductivity = QLineEdit(self.frame_material_settings)
        self.lineEdit_thermal_conductivity.setObjectName(u"lineEdit_thermal_conductivity")

        self.verticalLayout_3.addWidget(self.lineEdit_thermal_conductivity)

        self.pushButton_material_add = QPushButton(self.frame_material_settings)
        self.pushButton_material_add.setObjectName(u"pushButton_material_add")

        self.verticalLayout_3.addWidget(self.pushButton_material_add)

        self.comboBox_material_remove = QComboBox(self.frame_material_settings)
        self.comboBox_material_remove.addItem("")
        self.comboBox_material_remove.setObjectName(u"comboBox_material_remove")

        self.verticalLayout_3.addWidget(self.comboBox_material_remove)

        self.pushButton_material_remove = QPushButton(self.frame_material_settings)
        self.pushButton_material_remove.setObjectName(u"pushButton_material_remove")

        self.verticalLayout_3.addWidget(self.pushButton_material_remove)

        self.verticalSpacer_4 = QSpacerItem(20, 425, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)


        self.horizontalLayout.addWidget(self.frame_material_settings)

        self.frame_material_tree = QFrame(self.centralwidget)
        self.frame_material_tree.setObjectName(u"frame_material_tree")
        self.frame_material_tree.setMinimumSize(QSize(500, 0))
        self.frame_material_tree.setMaximumSize(QSize(300, 16777215))
        self.frame_material_tree.setFrameShape(QFrame.StyledPanel)
        self.frame_material_tree.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_material_tree)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.tableWidget_material = QTableWidget(self.frame_material_tree)
        if (self.tableWidget_material.columnCount() < 9):
            self.tableWidget_material.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        self.tableWidget_material.setObjectName(u"tableWidget_material")
        self.tableWidget_material.setMinimumSize(QSize(0, 0))
        self.tableWidget_material.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget_material.horizontalHeader().setDefaultSectionSize(50)

        self.verticalLayout.addWidget(self.tableWidget_material)


        self.horizontalLayout.addWidget(self.frame_material_tree)

        self.frame_info = QFrame(self.centralwidget)
        self.frame_info.setObjectName(u"frame_info")
        self.frame_info.setFrameShape(QFrame.StyledPanel)
        self.frame_info.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_info)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_plot_settings = QFrame(self.frame_info)
        self.frame_plot_settings.setObjectName(u"frame_plot_settings")
        self.frame_plot_settings.setMinimumSize(QSize(0, 32))
        self.frame_plot_settings.setMaximumSize(QSize(16777215, 32))
        self.frame_plot_settings.setFrameShape(QFrame.StyledPanel)
        self.frame_plot_settings.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_plot_settings)
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(1120, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.comboBox_material_curve = QComboBox(self.frame_plot_settings)
        self.comboBox_material_curve.addItem("")
        self.comboBox_material_curve.setObjectName(u"comboBox_material_curve")
        self.comboBox_material_curve.setMinimumSize(QSize(100, 25))
        self.comboBox_material_curve.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_2.addWidget(self.comboBox_material_curve)


        self.verticalLayout_2.addWidget(self.frame_plot_settings)

        self.frame_graph = QFrame(self.frame_info)
        self.frame_graph.setObjectName(u"frame_graph")
        self.frame_graph.setFrameShape(QFrame.StyledPanel)
        self.frame_graph.setFrameShadow(QFrame.Raised)

        self.verticalLayout_2.addWidget(self.frame_graph)


        self.horizontalLayout.addWidget(self.frame_info)

        OpenLatticeMaterialEditor.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(OpenLatticeMaterialEditor)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1920, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuGraph = QMenu(self.menubar)
        self.menuGraph.setObjectName(u"menuGraph")
        self.menuGrid = QMenu(self.menuGraph)
        self.menuGrid.setObjectName(u"menuGrid")
        OpenLatticeMaterialEditor.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuGraph.menuAction())
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionExport)
        self.menuGraph.addAction(self.actionClear)
        self.menuGraph.addAction(self.menuGrid.menuAction())
        self.menuGrid.addAction(self.actionShow_Grid)
        self.menuGrid.addAction(self.actionHide_Grid)

        self.retranslateUi(OpenLatticeMaterialEditor)

        QMetaObject.connectSlotsByName(OpenLatticeMaterialEditor)
    # setupUi

    def retranslateUi(self, OpenLatticeMaterialEditor):
        OpenLatticeMaterialEditor.setWindowTitle(QCoreApplication.translate("OpenLatticeMaterialEditor", u"OpenLattice Material Editor", None))
        self.actionImport.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Import", None))
        self.actionExport.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Export", None))
        self.actionTable.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Table", None))
        self.actionGraph.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Graph", None))
        self.actionNew.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"New", None))
        self.actionClear.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Clear", None))
        self.actionShow_Grid.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Show Grid", None))
        self.actionHide_Grid.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Hide Grid", None))
        self.label_15.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Material", None))
        self.label_16.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"ID", None))
        self.label_17.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Name", None))
        self.lineEdit_material_name.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Steel", None))
        self.label_18.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Modulus of Elasticity", None))
        self.lineEdit_modulus_of_elasticity.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"210000", None))
        self.label_19.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Poisson's Ratio", None))
        self.lineEdit_poissons_ratio.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"0.3", None))
        self.label_21.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Yield Stress", None))
        self.lineEdit_yield_stress.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"370", None))
        self.label_23.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Ultimate Stress", None))
        self.lineEdit_ultimate_stress.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"420", None))
        self.label_22.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Yield Strain", None))
        self.lineEdit_yield_strain.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"0.002", None))
        self.label_24.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Ultimate Strain", None))
        self.lineEdit_ultimate_strain.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"0.3", None))
        self.label_20.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Thermal Conductivity", None))
        self.lineEdit_thermal_conductivity.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"65.3", None))
        self.pushButton_material_add.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Add", None))
        self.comboBox_material_remove.setItemText(0, QCoreApplication.translate("OpenLatticeMaterialEditor", u"No Material", None))

        self.pushButton_material_remove.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Remove", None))
        ___qtablewidgetitem = self.tableWidget_material.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"ID", None));
        ___qtablewidgetitem1 = self.tableWidget_material.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Name", None));
        ___qtablewidgetitem2 = self.tableWidget_material.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Modulus of Elasticity", None));
        ___qtablewidgetitem3 = self.tableWidget_material.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Poisson's Ratio", None));
        ___qtablewidgetitem4 = self.tableWidget_material.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Yield Stress", None));
        ___qtablewidgetitem5 = self.tableWidget_material.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Ultimate Stress", None));
        ___qtablewidgetitem6 = self.tableWidget_material.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Yield Strain", None));
        ___qtablewidgetitem7 = self.tableWidget_material.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Ultimate Strain", None));
        ___qtablewidgetitem8 = self.tableWidget_material.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Thermal Conductivity", None));
        self.comboBox_material_curve.setItemText(0, QCoreApplication.translate("OpenLatticeMaterialEditor", u"No Material", None))

        self.menuFile.setTitle(QCoreApplication.translate("OpenLatticeMaterialEditor", u"File", None))
        self.menuGraph.setTitle(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Graph", None))
        self.menuGrid.setTitle(QCoreApplication.translate("OpenLatticeMaterialEditor", u"Grid", None))
    # retranslateUi

