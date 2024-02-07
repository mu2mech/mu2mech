# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(860, 685)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSavePlot = QAction(MainWindow)
        self.actionSavePlot.setObjectName(u"actionSavePlot")
        self.actionExportAnimation = QAction(MainWindow)
        self.actionExportAnimation.setObjectName(u"actionExportAnimation")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionSaveAllPlots = QAction(MainWindow)
        self.actionSaveAllPlots.setObjectName(u"actionSaveAllPlots")
        self.actionPlotColors = QAction(MainWindow)
        self.actionPlotColors.setObjectName(u"actionPlotColors")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.plotLabel = QLabel(self.centralwidget)
        self.plotLabel.setObjectName(u"plotLabel")
        self.plotLabel.setGeometry(QRect(20, 10, 601, 521))
        font = QFont()
        font.setPointSize(24)
        self.plotLabel.setFont(font)
        self.plotLabel.setMouseTracking(True)
        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(20, 580, 601, 20))
        self.horizontalSlider.setSingleStep(10)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.timeDisplayLabel = QLabel(self.centralwidget)
        self.timeDisplayLabel.setObjectName(u"timeDisplayLabel")
        self.timeDisplayLabel.setGeometry(QRect(140, 600, 41, 21))
        self.timeDisplayLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.timeLabel = QLabel(self.centralwidget)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setGeometry(QRect(100, 600, 41, 20))
        self.timeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.pushButtonEdit = QPushButton(self.centralwidget)
        self.pushButtonEdit.setObjectName(u"pushButtonEdit")
        self.pushButtonEdit.setGeometry(QRect(640, 80, 201, 41))
        self.layoutWidget_1 = QWidget(self.centralwidget)
        self.layoutWidget_1.setObjectName(u"layoutWidget_1")
        self.layoutWidget_1.setGeometry(QRect(640, 10, 201, 58))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget_1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget_1)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.labelCalType = QLabel(self.layoutWidget_1)
        self.labelCalType.setObjectName(u"labelCalType")

        self.verticalLayout_2.addWidget(self.labelCalType)

        self.layoutWidget_3 = QWidget(self.centralwidget)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(640, 140, 201, 58))
        self.gridLayout = QGridLayout(self.layoutWidget_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelTimeInterval = QLabel(self.layoutWidget_3)
        self.labelTimeInterval.setObjectName(u"labelTimeInterval")

        self.gridLayout.addWidget(self.labelTimeInterval, 0, 0, 1, 1)

        self.lineEditTimeInterval = QLineEdit(self.layoutWidget_3)
        self.lineEditTimeInterval.setObjectName(u"lineEditTimeInterval")

        self.gridLayout.addWidget(self.lineEditTimeInterval, 0, 1, 1, 1)

        self.labelTotalTime = QLabel(self.layoutWidget_3)
        self.labelTotalTime.setObjectName(u"labelTotalTime")

        self.gridLayout.addWidget(self.labelTotalTime, 1, 0, 1, 1)

        self.lineEditTotalTime = QLineEdit(self.layoutWidget_3)
        self.lineEditTotalTime.setObjectName(u"lineEditTotalTime")

        self.gridLayout.addWidget(self.lineEditTotalTime, 1, 1, 1, 1)

        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(640, 260, 201, 61))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.labelProgress = QLabel(self.layoutWidget)
        self.labelProgress.setObjectName(u"labelProgress")

        self.horizontalLayout_2.addWidget(self.labelProgress)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelCurrentStatusType = QLabel(self.layoutWidget)
        self.labelCurrentStatusType.setObjectName(u"labelCurrentStatusType")

        self.horizontalLayout_3.addWidget(self.labelCurrentStatusType)

        self.labelCurrentStatus = QLabel(self.layoutWidget)
        self.labelCurrentStatus.setObjectName(u"labelCurrentStatus")

        self.horizontalLayout_3.addWidget(self.labelCurrentStatus)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.pushButtonPostProcessing = QPushButton(self.centralwidget)
        self.pushButtonPostProcessing.setObjectName(u"pushButtonPostProcessing")
        self.pushButtonPostProcessing.setGeometry(QRect(640, 580, 201, 51))
        self.framePlot = QFrame(self.centralwidget)
        self.framePlot.setObjectName(u"framePlot")
        self.framePlot.setGeometry(QRect(20, -40, 600, 600))
        self.framePlot.setFrameShape(QFrame.StyledPanel)
        self.framePlot.setFrameShadow(QFrame.Raised)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(640, 340, 201, 91))
        self.checkBoxColorbar = QCheckBox(self.groupBox)
        self.checkBoxColorbar.setObjectName(u"checkBoxColorbar")
        self.checkBoxColorbar.setGeometry(QRect(10, 60, 85, 21))
        self.checkBoxColorbar.setChecked(True)
        self.checkBoxAxis = QCheckBox(self.groupBox)
        self.checkBoxAxis.setObjectName(u"checkBoxAxis")
        self.checkBoxAxis.setEnabled(True)
        self.checkBoxAxis.setGeometry(QRect(10, 30, 85, 21))
        self.checkBoxAxis.setChecked(True)
        self.pushButtonPlot = QPushButton(self.groupBox)
        self.pushButtonPlot.setObjectName(u"pushButtonPlot")
        self.pushButtonPlot.setGeometry(QRect(100, 30, 91, 51))
        self.pushButtonRight = QPushButton(self.centralwidget)
        self.pushButtonRight.setObjectName(u"pushButtonRight")
        self.pushButtonRight.setGeometry(QRect(60, 600, 31, 25))
        self.pushButtonLeft = QPushButton(self.centralwidget)
        self.pushButtonLeft.setObjectName(u"pushButtonLeft")
        self.pushButtonLeft.setGeometry(QRect(20, 600, 31, 25))
        self.labelStatus = QLabel(self.centralwidget)
        self.labelStatus.setObjectName(u"labelStatus")
        self.labelStatus.setGeometry(QRect(360, 600, 261, 20))
        font1 = QFont()
        font1.setPointSize(11)
        self.labelStatus.setFont(font1)
        self.labelStatus.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.labelMousePosition = QLabel(self.centralwidget)
        self.labelMousePosition.setObjectName(u"labelMousePosition")
        self.labelMousePosition.setGeometry(QRect(200, 600, 141, 17))
        self.pushButtonStartStopResume = QPushButton(self.centralwidget)
        self.pushButtonStartStopResume.setObjectName(u"pushButtonStartStopResume")
        self.pushButtonStartStopResume.setGeometry(QRect(640, 210, 201, 41))
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(640, 450, 201, 111))
        self.layoutWidget1 = QWidget(self.groupBox_2)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 30, 181, 71))
        self.gridLayout_2 = QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.labelLength = QLabel(self.layoutWidget1)
        self.labelLength.setObjectName(u"labelLength")

        self.gridLayout_2.addWidget(self.labelLength, 0, 0, 1, 1)

        self.labelLengthValue = QLabel(self.layoutWidget1)
        self.labelLengthValue.setObjectName(u"labelLengthValue")

        self.gridLayout_2.addWidget(self.labelLengthValue, 0, 1, 1, 1)

        self.labelTime = QLabel(self.layoutWidget1)
        self.labelTime.setObjectName(u"labelTime")

        self.gridLayout_2.addWidget(self.labelTime, 1, 0, 1, 1)

        self.labelTimeValue = QLabel(self.layoutWidget1)
        self.labelTimeValue.setObjectName(u"labelTimeValue")

        self.gridLayout_2.addWidget(self.labelTimeValue, 1, 1, 1, 1)

        self.labelEnergy = QLabel(self.layoutWidget1)
        self.labelEnergy.setObjectName(u"labelEnergy")

        self.gridLayout_2.addWidget(self.labelEnergy, 2, 0, 1, 1)

        self.labelEnergyValue = QLabel(self.layoutWidget1)
        self.labelEnergyValue.setObjectName(u"labelEnergyValue")

        self.gridLayout_2.addWidget(self.labelEnergyValue, 2, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 860, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName(u"menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSavePlot)
        self.menuFile.addAction(self.actionSaveAllPlots)
        self.menuFile.addAction(self.actionExportAnimation)
        self.menuFile.addAction(self.actionQuit)
        self.menuOptions.addAction(self.actionPlotColors)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u03bc2Mech", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
        self.actionSavePlot.setText(QCoreApplication.translate("MainWindow", u"Save Plot", None))
        self.actionExportAnimation.setText(QCoreApplication.translate("MainWindow", u"Export Animation", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionSaveAllPlots.setText(QCoreApplication.translate("MainWindow", u"Save all plots", None))
        self.actionPlotColors.setText(QCoreApplication.translate("MainWindow", u"Plot Colors", None))
        self.plotLabel.setText("")
        self.timeDisplayLabel.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"time", None))
        self.pushButtonEdit.setText(QCoreApplication.translate("MainWindow", u"Edit Parameters", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">Calculation type</span></p></body></html>", None))
        self.labelCalType.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.labelTimeInterval.setText(QCoreApplication.translate("MainWindow", u"time interval", None))
        self.labelTotalTime.setText(QCoreApplication.translate("MainWindow", u"total time", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Progress", None))
        self.labelProgress.setText(QCoreApplication.translate("MainWindow", u"0%", None))
        self.labelCurrentStatusType.setText(QCoreApplication.translate("MainWindow", u"Calculated for", None))
        self.labelCurrentStatus.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.pushButtonPostProcessing.setText(QCoreApplication.translate("MainWindow", u"Post  Processing", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Plot options", None))
        self.checkBoxColorbar.setText(QCoreApplication.translate("MainWindow", u"Colorbar", None))
        self.checkBoxAxis.setText(QCoreApplication.translate("MainWindow", u"Axis", None))
        self.pushButtonPlot.setText(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.pushButtonRight.setText("")
        self.pushButtonLeft.setText("")
        self.labelStatus.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.labelMousePosition.setText("")
        self.pushButtonStartStopResume.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Characteristics values", None))
        self.labelLength.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">Length (nm):</p></body></html>", None))
        self.labelLengthValue.setText("")
        self.labelTime.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">Time (sec.):</p></body></html>", None))
        self.labelTimeValue.setText("")
        self.labelEnergy.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">Energy (KJ/mole):</p></body></html>", None))
        self.labelEnergyValue.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

