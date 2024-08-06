# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'open_interfaceEVgIHT.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_OpenLattice_Lite(object):
    def setupUi(self, OpenLattice_Lite):
        if not OpenLattice_Lite.objectName():
            OpenLattice_Lite.setObjectName(u"OpenLattice_Lite")
        OpenLattice_Lite.resize(800, 600)
        OpenLattice_Lite.setMaximumSize(QSize(800, 600))
        self.actionImport = QAction(OpenLattice_Lite)
        self.actionImport.setObjectName(u"actionImport")
        self.actionExport = QAction(OpenLattice_Lite)
        self.actionExport.setObjectName(u"actionExport")
        self.actionAnalysis_Based = QAction(OpenLattice_Lite)
        self.actionAnalysis_Based.setObjectName(u"actionAnalysis_Based")
        self.actionProject_Based = QAction(OpenLattice_Lite)
        self.actionProject_Based.setObjectName(u"actionProject_Based")
        self.actionProject_Based.setEnabled(False)
        self.centralwidget = QWidget(OpenLattice_Lite)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_applications = QFrame(self.centralwidget)
        self.frame_applications.setObjectName(u"frame_applications")
        self.frame_applications.setMinimumSize(QSize(300, 0))
        self.frame_applications.setMaximumSize(QSize(300, 16777215))
        self.frame_applications.setFrameShape(QFrame.StyledPanel)
        self.frame_applications.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_applications)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.label_new_data = QLabel(self.frame_applications)
        self.label_new_data.setObjectName(u"label_new_data")

        self.verticalLayout_2.addWidget(self.label_new_data)

        self.pushButton_material_data = QPushButton(self.frame_applications)
        self.pushButton_material_data.setObjectName(u"pushButton_material_data")
        self.pushButton_material_data.setMinimumSize(QSize(100, 25))
        self.pushButton_material_data.setMaximumSize(QSize(100, 25))

        self.verticalLayout_2.addWidget(self.pushButton_material_data, 0, Qt.AlignHCenter)

        self.label_new_analyses = QLabel(self.frame_applications)
        self.label_new_analyses.setObjectName(u"label_new_analyses")

        self.verticalLayout_2.addWidget(self.label_new_analyses)

        self.pushButton_static = QPushButton(self.frame_applications)
        self.pushButton_static.setObjectName(u"pushButton_static")
        self.pushButton_static.setMinimumSize(QSize(100, 25))
        self.pushButton_static.setMaximumSize(QSize(100, 25))

        self.verticalLayout_2.addWidget(self.pushButton_static, 0, Qt.AlignHCenter)

        self.pushButton_homogenization = QPushButton(self.frame_applications)
        self.pushButton_homogenization.setObjectName(u"pushButton_homogenization")
        self.pushButton_homogenization.setMinimumSize(QSize(100, 25))
        self.pushButton_homogenization.setMaximumSize(QSize(100, 25))

        self.verticalLayout_2.addWidget(self.pushButton_homogenization, 0, Qt.AlignHCenter)

        self.pushButton_optimization = QPushButton(self.frame_applications)
        self.pushButton_optimization.setObjectName(u"pushButton_optimization")
        self.pushButton_optimization.setMinimumSize(QSize(100, 25))
        self.pushButton_optimization.setMaximumSize(QSize(100, 25))

        self.verticalLayout_2.addWidget(self.pushButton_optimization, 0, Qt.AlignHCenter)

        self.pushButton_reconstruction = QPushButton(self.frame_applications)
        self.pushButton_reconstruction.setObjectName(u"pushButton_reconstruction")
        self.pushButton_reconstruction.setMinimumSize(QSize(100, 25))
        self.pushButton_reconstruction.setMaximumSize(QSize(100, 25))

        self.verticalLayout_2.addWidget(self.pushButton_reconstruction, 0, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.frame_applications)

        self.frame_models = QFrame(self.centralwidget)
        self.frame_models.setObjectName(u"frame_models")
        self.frame_models.setFrameShape(QFrame.StyledPanel)
        self.frame_models.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_models)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.treeWidget = QTreeWidget(self.frame_models)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout.addWidget(self.treeWidget)


        self.horizontalLayout.addWidget(self.frame_models)

        OpenLattice_Lite.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(OpenLattice_Lite)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuview = QMenu(self.menubar)
        self.menuview.setObjectName(u"menuview")
        OpenLattice_Lite.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuview.menuAction())
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionExport)
        self.menuview.addAction(self.actionAnalysis_Based)
        self.menuview.addAction(self.actionProject_Based)

        self.retranslateUi(OpenLattice_Lite)

        QMetaObject.connectSlotsByName(OpenLattice_Lite)
    # setupUi

    def retranslateUi(self, OpenLattice_Lite):
        OpenLattice_Lite.setWindowTitle(QCoreApplication.translate("OpenLattice_Lite", u"OpenLattice Lite", None))
        self.actionImport.setText(QCoreApplication.translate("OpenLattice_Lite", u"Import", None))
        self.actionExport.setText(QCoreApplication.translate("OpenLattice_Lite", u"Export", None))
        self.actionAnalysis_Based.setText(QCoreApplication.translate("OpenLattice_Lite", u"Analysis Based", None))
        self.actionProject_Based.setText(QCoreApplication.translate("OpenLattice_Lite", u"Project Based", None))
        self.label_new_data.setText(QCoreApplication.translate("OpenLattice_Lite", u"New Data", None))
        self.pushButton_material_data.setText(QCoreApplication.translate("OpenLattice_Lite", u"Material Data", None))
        self.label_new_analyses.setText(QCoreApplication.translate("OpenLattice_Lite", u"New Analyses", None))
        self.pushButton_static.setText(QCoreApplication.translate("OpenLattice_Lite", u"Static", None))
        self.pushButton_homogenization.setText(QCoreApplication.translate("OpenLattice_Lite", u"Homogenization", None))
        self.pushButton_optimization.setText(QCoreApplication.translate("OpenLattice_Lite", u"Optimization", None))
        self.pushButton_reconstruction.setText(QCoreApplication.translate("OpenLattice_Lite", u"Reconstruction", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("OpenLattice_Lite", u"Analyses", None));
        self.menuFile.setTitle(QCoreApplication.translate("OpenLattice_Lite", u"File", None))
        self.menuview.setTitle(QCoreApplication.translate("OpenLattice_Lite", u"view", None))
    # retranslateUi

