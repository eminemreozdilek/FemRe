# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'static_interfacemLleiX.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_CellulozStatic(object):
    def setupUi(self, CellulozStatic):
        if not CellulozStatic.objectName():
            CellulozStatic.setObjectName(u"CellulozStatic")
        CellulozStatic.resize(1920, 1039)
        self.actionIsometric = QAction(CellulozStatic)
        self.actionIsometric.setObjectName(u"actionIsometric")
        self.actionFront = QAction(CellulozStatic)
        self.actionFront.setObjectName(u"actionFront")
        self.actionRight = QAction(CellulozStatic)
        self.actionRight.setObjectName(u"actionRight")
        self.actionTop = QAction(CellulozStatic)
        self.actionTop.setObjectName(u"actionTop")
        self.actionBack = QAction(CellulozStatic)
        self.actionBack.setObjectName(u"actionBack")
        self.actionLeft = QAction(CellulozStatic)
        self.actionLeft.setObjectName(u"actionLeft")
        self.actionBottom = QAction(CellulozStatic)
        self.actionBottom.setObjectName(u"actionBottom")
        self.actionProject = QAction(CellulozStatic)
        self.actionProject.setObjectName(u"actionProject")
        self.actionGeometry = QAction(CellulozStatic)
        self.actionGeometry.setObjectName(u"actionGeometry")
        self.actionHomogenization_Results = QAction(CellulozStatic)
        self.actionHomogenization_Results.setObjectName(u"actionHomogenization_Results")
        self.actionPicture = QAction(CellulozStatic)
        self.actionPicture.setObjectName(u"actionPicture")
        self.actionImportProject = QAction(CellulozStatic)
        self.actionImportProject.setObjectName(u"actionImportProject")
        self.actionImportStaticModel = QAction(CellulozStatic)
        self.actionImportStaticModel.setObjectName(u"actionImportStaticModel")
        self.actionHomogenizer_Data = QAction(CellulozStatic)
        self.actionHomogenizer_Data.setObjectName(u"actionHomogenizer_Data")
        self.actionHomogenizer_Menu = QAction(CellulozStatic)
        self.actionHomogenizer_Menu.setObjectName(u"actionHomogenizer_Menu")
        self.actionAdd_Body = QAction(CellulozStatic)
        self.actionAdd_Body.setObjectName(u"actionAdd_Body")
        self.actionAdd_Strut = QAction(CellulozStatic)
        self.actionAdd_Strut.setObjectName(u"actionAdd_Strut")
        self.actionAdd_Brick = QAction(CellulozStatic)
        self.actionAdd_Brick.setObjectName(u"actionAdd_Brick")
        self.actionAdd_Boundary_Conditions = QAction(CellulozStatic)
        self.actionAdd_Boundary_Conditions.setObjectName(u"actionAdd_Boundary_Conditions")
        self.actionSolver = QAction(CellulozStatic)
        self.actionSolver.setObjectName(u"actionSolver")
        self.actionResults = QAction(CellulozStatic)
        self.actionResults.setObjectName(u"actionResults")
        self.actionProperties = QAction(CellulozStatic)
        self.actionProperties.setObjectName(u"actionProperties")
        self.centralwidget = QWidget(CellulozStatic)
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
        self.frame_model_properties = QFrame(self.frame_main)
        self.frame_model_properties.setObjectName(u"frame_model_properties")
        self.frame_model_properties.setMinimumSize(QSize(0, 0))
        self.frame_model_properties.setMaximumSize(QSize(700, 16777215))
        self.frame_model_properties.setFrameShape(QFrame.StyledPanel)
        self.frame_model_properties.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_model_properties)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.frame_strut_lister = QFrame(self.frame_model_properties)
        self.frame_strut_lister.setObjectName(u"frame_strut_lister")
        self.frame_strut_lister.setMaximumSize(QSize(700, 16777215))
        self.frame_strut_lister.setFrameShape(QFrame.StyledPanel)
        self.frame_strut_lister.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_strut_lister)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.tableWidget_node = QTableWidget(self.frame_strut_lister)
        if (self.tableWidget_node.columnCount() < 13):
            self.tableWidget_node.setColumnCount(13)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_node.setHorizontalHeaderItem(12, __qtablewidgetitem12)
        self.tableWidget_node.setObjectName(u"tableWidget_node")
        self.tableWidget_node.setMinimumSize(QSize(0, 350))
        self.tableWidget_node.setMaximumSize(QSize(16777215, 350))
        self.tableWidget_node.horizontalHeader().setDefaultSectionSize(50)

        self.verticalLayout_2.addWidget(self.tableWidget_node)

        self.tableWidget_strut = QTableWidget(self.frame_strut_lister)
        if (self.tableWidget_strut.columnCount() < 9):
            self.tableWidget_strut.setColumnCount(9)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(1, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(2, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(3, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(4, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(5, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(6, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(7, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget_strut.setHorizontalHeaderItem(8, __qtablewidgetitem21)
        self.tableWidget_strut.setObjectName(u"tableWidget_strut")
        self.tableWidget_strut.setMinimumSize(QSize(0, 350))
        self.tableWidget_strut.setMaximumSize(QSize(16777215, 350))
        self.tableWidget_strut.horizontalHeader().setDefaultSectionSize(70)

        self.verticalLayout_2.addWidget(self.tableWidget_strut)

        self.tableWidget_material = QTableWidget(self.frame_strut_lister)
        if (self.tableWidget_material.columnCount() < 10):
            self.tableWidget_material.setColumnCount(10)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(0, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(1, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(2, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(3, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(4, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(5, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(6, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(7, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(8, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tableWidget_material.setHorizontalHeaderItem(9, __qtablewidgetitem31)
        self.tableWidget_material.setObjectName(u"tableWidget_material")
        self.tableWidget_material.setMinimumSize(QSize(0, 100))
        self.tableWidget_material.setMaximumSize(QSize(16777215, 100))
        self.tableWidget_material.horizontalHeader().setDefaultSectionSize(70)

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


        self.horizontalLayout_3.addWidget(self.frame_strut_lister)


        self.horizontalLayout.addWidget(self.frame_model_properties)

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

        CellulozStatic.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(CellulozStatic)
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
        self.menuAdd_Structure = QMenu(self.menuModules)
        self.menuAdd_Structure.setObjectName(u"menuAdd_Structure")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuView_Angle = QMenu(self.menuView)
        self.menuView_Angle.setObjectName(u"menuView_Angle")
        CellulozStatic.setMenuBar(self.menubar)

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
        self.menuImport.addAction(self.actionImportProject)
        self.menuImport.addAction(self.actionImportStaticModel)
        self.menuModules.addAction(self.menuAdd_Structure.menuAction())
        self.menuModules.addAction(self.actionAdd_Boundary_Conditions)
        self.menuModules.addAction(self.actionSolver)
        self.menuModules.addAction(self.actionResults)
        self.menuAdd_Structure.addAction(self.actionAdd_Body)
        self.menuAdd_Structure.addAction(self.actionAdd_Strut)
        self.menuAdd_Structure.addAction(self.actionAdd_Brick)
        self.menuView.addAction(self.menuView_Angle.menuAction())
        self.menuView.addAction(self.actionProperties)
        self.menuView_Angle.addAction(self.actionIsometric)
        self.menuView_Angle.addAction(self.actionFront)
        self.menuView_Angle.addAction(self.actionRight)
        self.menuView_Angle.addAction(self.actionTop)
        self.menuView_Angle.addAction(self.actionBack)
        self.menuView_Angle.addAction(self.actionLeft)
        self.menuView_Angle.addAction(self.actionBottom)

        self.retranslateUi(CellulozStatic)

        QMetaObject.connectSlotsByName(CellulozStatic)
    # setupUi

    def retranslateUi(self, CellulozStatic):
        CellulozStatic.setWindowTitle(QCoreApplication.translate("CellulozStatic", u"Celluloz Static", None))
        self.actionIsometric.setText(QCoreApplication.translate("CellulozStatic", u"Isometric", None))
        self.actionFront.setText(QCoreApplication.translate("CellulozStatic", u"Front", None))
        self.actionRight.setText(QCoreApplication.translate("CellulozStatic", u"Right", None))
        self.actionTop.setText(QCoreApplication.translate("CellulozStatic", u"Top", None))
        self.actionBack.setText(QCoreApplication.translate("CellulozStatic", u"Back", None))
        self.actionLeft.setText(QCoreApplication.translate("CellulozStatic", u"Left", None))
        self.actionBottom.setText(QCoreApplication.translate("CellulozStatic", u"Bottom", None))
        self.actionProject.setText(QCoreApplication.translate("CellulozStatic", u"Project", None))
        self.actionGeometry.setText(QCoreApplication.translate("CellulozStatic", u"Geometry", None))
        self.actionHomogenization_Results.setText(QCoreApplication.translate("CellulozStatic", u"Properties", None))
        self.actionPicture.setText(QCoreApplication.translate("CellulozStatic", u"Picture", None))
        self.actionImportProject.setText(QCoreApplication.translate("CellulozStatic", u"Project", None))
        self.actionImportStaticModel.setText(QCoreApplication.translate("CellulozStatic", u"Static Model", None))
        self.actionHomogenizer_Data.setText(QCoreApplication.translate("CellulozStatic", u"Homogenizer Data", None))
        self.actionHomogenizer_Menu.setText(QCoreApplication.translate("CellulozStatic", u"Homogenizer Menu", None))
        self.actionAdd_Body.setText(QCoreApplication.translate("CellulozStatic", u"Add Body", None))
        self.actionAdd_Strut.setText(QCoreApplication.translate("CellulozStatic", u"Add Strut", None))
        self.actionAdd_Brick.setText(QCoreApplication.translate("CellulozStatic", u"Add Brick", None))
        self.actionAdd_Boundary_Conditions.setText(QCoreApplication.translate("CellulozStatic", u"Add Boundary Conditions", None))
        self.actionSolver.setText(QCoreApplication.translate("CellulozStatic", u"Solver", None))
        self.actionResults.setText(QCoreApplication.translate("CellulozStatic", u"Results", None))
        self.actionProperties.setText(QCoreApplication.translate("CellulozStatic", u"Properties", None))
        ___qtablewidgetitem = self.tableWidget_node.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("CellulozStatic", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget_node.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("CellulozStatic", u"X", None));
        ___qtablewidgetitem2 = self.tableWidget_node.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("CellulozStatic", u"Y", None));
        ___qtablewidgetitem3 = self.tableWidget_node.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("CellulozStatic", u"Z", None));
        ___qtablewidgetitem4 = self.tableWidget_node.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("CellulozStatic", u"Force X", None));
        ___qtablewidgetitem5 = self.tableWidget_node.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("CellulozStatic", u"Force Y", None));
        ___qtablewidgetitem6 = self.tableWidget_node.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("CellulozStatic", u"Force Z", None));
        ___qtablewidgetitem7 = self.tableWidget_node.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("CellulozStatic", u"Rest X", None));
        ___qtablewidgetitem8 = self.tableWidget_node.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("CellulozStatic", u"Rest Y", None));
        ___qtablewidgetitem9 = self.tableWidget_node.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("CellulozStatic", u"Rest Z", None));
        ___qtablewidgetitem10 = self.tableWidget_node.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("CellulozStatic", u"Displacement X", None));
        ___qtablewidgetitem11 = self.tableWidget_node.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("CellulozStatic", u"Displacement Y", None));
        ___qtablewidgetitem12 = self.tableWidget_node.horizontalHeaderItem(12)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("CellulozStatic", u"Displacement Z", None));
        ___qtablewidgetitem13 = self.tableWidget_strut.horizontalHeaderItem(0)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("CellulozStatic", u"Name", None));
        ___qtablewidgetitem14 = self.tableWidget_strut.horizontalHeaderItem(1)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("CellulozStatic", u"Nodes", None));
        ___qtablewidgetitem15 = self.tableWidget_strut.horizontalHeaderItem(2)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("CellulozStatic", u"Material", None));
        ___qtablewidgetitem16 = self.tableWidget_strut.horizontalHeaderItem(3)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("CellulozStatic", u"Section", None));
        ___qtablewidgetitem17 = self.tableWidget_strut.horizontalHeaderItem(4)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("CellulozStatic", u"Boundary Force X", None));
        ___qtablewidgetitem18 = self.tableWidget_strut.horizontalHeaderItem(5)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("CellulozStatic", u"Boundary Force Y", None));
        ___qtablewidgetitem19 = self.tableWidget_strut.horizontalHeaderItem(6)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("CellulozStatic", u"Boundary Force Z", None));
        ___qtablewidgetitem20 = self.tableWidget_strut.horizontalHeaderItem(7)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("CellulozStatic", u"Volume Force", None));
        ___qtablewidgetitem21 = self.tableWidget_strut.horizontalHeaderItem(8)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("CellulozStatic", u"Tempreture Change", None));
        ___qtablewidgetitem22 = self.tableWidget_material.horizontalHeaderItem(0)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("CellulozStatic", u"ID", None));
        ___qtablewidgetitem23 = self.tableWidget_material.horizontalHeaderItem(1)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("CellulozStatic", u"Name", None));
        ___qtablewidgetitem24 = self.tableWidget_material.horizontalHeaderItem(2)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("CellulozStatic", u"Modulus of Elasticity", None));
        ___qtablewidgetitem25 = self.tableWidget_material.horizontalHeaderItem(3)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("CellulozStatic", u"Poisson's Ratio", None));
        ___qtablewidgetitem26 = self.tableWidget_material.horizontalHeaderItem(4)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("CellulozStatic", u"Yield Stress", None));
        ___qtablewidgetitem27 = self.tableWidget_material.horizontalHeaderItem(5)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("CellulozStatic", u"Ultimate Stress", None));
        ___qtablewidgetitem28 = self.tableWidget_material.horizontalHeaderItem(6)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("CellulozStatic", u"Yield Strain", None));
        ___qtablewidgetitem29 = self.tableWidget_material.horizontalHeaderItem(7)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("CellulozStatic", u"Ultimate Strain", None));
        ___qtablewidgetitem30 = self.tableWidget_material.horizontalHeaderItem(8)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("CellulozStatic", u"Thermal Conductivity", None));
        ___qtablewidgetitem31 = self.tableWidget_material.horizontalHeaderItem(9)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("CellulozStatic", u"Spesific Weight", None));
        self.label_25.setText(QCoreApplication.translate("CellulozStatic", u"Resolution", None))
        self.pushButton_regenerate_model.setText(QCoreApplication.translate("CellulozStatic", u"ReGenerate", None))
        self.pushButton_save_model.setText(QCoreApplication.translate("CellulozStatic", u"Save", None))
        self.menuFile.setTitle(QCoreApplication.translate("CellulozStatic", u"File", None))
        self.menuSave.setTitle(QCoreApplication.translate("CellulozStatic", u"Save", None))
        self.menuLattice_Model.setTitle(QCoreApplication.translate("CellulozStatic", u"Static Model", None))
        self.menuImport.setTitle(QCoreApplication.translate("CellulozStatic", u"Import", None))
        self.menuModules.setTitle(QCoreApplication.translate("CellulozStatic", u"Modules", None))
        self.menuAdd_Structure.setTitle(QCoreApplication.translate("CellulozStatic", u"Add Structure", None))
        self.menuView.setTitle(QCoreApplication.translate("CellulozStatic", u"View", None))
        self.menuView_Angle.setTitle(QCoreApplication.translate("CellulozStatic", u"View Angle", None))
    # retranslateUi

