# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_oof2_calculation.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogOOF2Calculation(object):
    def setupUi(self, DialogOOF2Calculation):
        if not DialogOOF2Calculation.objectName():
            DialogOOF2Calculation.setObjectName(u"DialogOOF2Calculation")
        DialogOOF2Calculation.resize(600, 580)
        self.groupBoxBoundaryCondition = QGroupBox(DialogOOF2Calculation)
        self.groupBoxBoundaryCondition.setObjectName(u"groupBoxBoundaryCondition")
        self.groupBoxBoundaryCondition.setGeometry(QRect(290, 210, 301, 111))
        self.layoutWidget = QWidget(self.groupBoxBoundaryCondition)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 40, 261, 58))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelLeftValue = QLabel(self.layoutWidget)
        self.labelLeftValue.setObjectName(u"labelLeftValue")
        self.labelLeftValue.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelLeftValue, 0, 0, 1, 1)

        self.lineEditBC1Value = QLineEdit(self.layoutWidget)
        self.lineEditBC1Value.setObjectName(u"lineEditBC1Value")

        self.gridLayout.addWidget(self.lineEditBC1Value, 0, 1, 1, 1)

        self.labelRightValue = QLabel(self.layoutWidget)
        self.labelRightValue.setObjectName(u"labelRightValue")
        self.labelRightValue.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelRightValue, 1, 0, 1, 1)

        self.lineEditBC2Value = QLineEdit(self.layoutWidget)
        self.lineEditBC2Value.setObjectName(u"lineEditBC2Value")

        self.gridLayout.addWidget(self.lineEditBC2Value, 1, 1, 1, 1)

        self.pushButtonBrowseOutDir = QPushButton(DialogOOF2Calculation)
        self.pushButtonBrowseOutDir.setObjectName(u"pushButtonBrowseOutDir")
        self.pushButtonBrowseOutDir.setGeometry(QRect(110, 350, 31, 31))
        self.labelStatus = QLabel(DialogOOF2Calculation)
        self.labelStatus.setObjectName(u"labelStatus")
        self.labelStatus.setGeometry(QRect(20, 520, 281, 17))
        self.lineEditOutDir = QLineEdit(DialogOOF2Calculation)
        self.lineEditOutDir.setObjectName(u"lineEditOutDir")
        self.lineEditOutDir.setGeometry(QRect(140, 350, 451, 31))
        self.groupBoxElasticConstant = QGroupBox(DialogOOF2Calculation)
        self.groupBoxElasticConstant.setObjectName(u"groupBoxElasticConstant")
        self.groupBoxElasticConstant.setGeometry(QRect(290, 10, 301, 181))
        self.groupBox = QGroupBox(self.groupBoxElasticConstant)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 30, 141, 131))
        self.layoutWidget2 = QWidget(self.groupBox)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 30, 111, 89))
        self.gridLayout_2 = QGridLayout(self.layoutWidget2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.labelCijValue = QLabel(self.layoutWidget2)
        self.labelCijValue.setObjectName(u"labelCijValue")

        self.gridLayout_2.addWidget(self.labelCijValue, 0, 0, 1, 1)

        self.lineEditPhase1C11 = QLineEdit(self.layoutWidget2)
        self.lineEditPhase1C11.setObjectName(u"lineEditPhase1C11")

        self.gridLayout_2.addWidget(self.lineEditPhase1C11, 0, 1, 1, 1)

        self.labelCijValue_2 = QLabel(self.layoutWidget2)
        self.labelCijValue_2.setObjectName(u"labelCijValue_2")

        self.gridLayout_2.addWidget(self.labelCijValue_2, 1, 0, 1, 1)

        self.lineEditPhase1C12 = QLineEdit(self.layoutWidget2)
        self.lineEditPhase1C12.setObjectName(u"lineEditPhase1C12")

        self.gridLayout_2.addWidget(self.lineEditPhase1C12, 1, 1, 1, 1)

        self.labelCijValue_3 = QLabel(self.layoutWidget2)
        self.labelCijValue_3.setObjectName(u"labelCijValue_3")

        self.gridLayout_2.addWidget(self.labelCijValue_3, 2, 0, 1, 1)

        self.lineEditPhase1C44 = QLineEdit(self.layoutWidget2)
        self.lineEditPhase1C44.setObjectName(u"lineEditPhase1C44")

        self.gridLayout_2.addWidget(self.lineEditPhase1C44, 2, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.groupBoxElasticConstant)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(160, 30, 131, 131))
        self.layoutWidget3 = QWidget(self.groupBox_2)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(10, 30, 111, 89))
        self.gridLayout_4 = QGridLayout(self.layoutWidget3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.labelCijValue_7 = QLabel(self.layoutWidget3)
        self.labelCijValue_7.setObjectName(u"labelCijValue_7")

        self.gridLayout_4.addWidget(self.labelCijValue_7, 0, 0, 1, 1)

        self.lineEditPhase2C11 = QLineEdit(self.layoutWidget3)
        self.lineEditPhase2C11.setObjectName(u"lineEditPhase2C11")

        self.gridLayout_4.addWidget(self.lineEditPhase2C11, 0, 1, 1, 1)

        self.labelCijValue_8 = QLabel(self.layoutWidget3)
        self.labelCijValue_8.setObjectName(u"labelCijValue_8")

        self.gridLayout_4.addWidget(self.labelCijValue_8, 1, 0, 1, 1)

        self.lineEditPhase2C12 = QLineEdit(self.layoutWidget3)
        self.lineEditPhase2C12.setObjectName(u"lineEditPhase2C12")

        self.gridLayout_4.addWidget(self.lineEditPhase2C12, 1, 1, 1, 1)

        self.labelCijValue_9 = QLabel(self.layoutWidget3)
        self.labelCijValue_9.setObjectName(u"labelCijValue_9")

        self.gridLayout_4.addWidget(self.labelCijValue_9, 2, 0, 1, 1)

        self.lineEditPhase2C44 = QLineEdit(self.layoutWidget3)
        self.lineEditPhase2C44.setObjectName(u"lineEditPhase2C44")

        self.gridLayout_4.addWidget(self.lineEditPhase2C44, 2, 1, 1, 1)

        self.groupBoxMesh = QGroupBox(DialogOOF2Calculation)
        self.groupBoxMesh.setObjectName(u"groupBoxMesh")
        self.groupBoxMesh.setGeometry(QRect(10, 190, 261, 131))
        self.layoutWidget4 = QWidget(self.groupBoxMesh)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(10, 31, 231, 89))
        self.gridLayout_3 = QGridLayout(self.layoutWidget4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.labelXElements = QLabel(self.layoutWidget4)
        self.labelXElements.setObjectName(u"labelXElements")

        self.gridLayout_3.addWidget(self.labelXElements, 0, 0, 1, 1)

        self.lineEditXElements = QLineEdit(self.layoutWidget4)
        self.lineEditXElements.setObjectName(u"lineEditXElements")

        self.gridLayout_3.addWidget(self.lineEditXElements, 0, 1, 1, 1)

        self.labelYElements = QLabel(self.layoutWidget4)
        self.labelYElements.setObjectName(u"labelYElements")

        self.gridLayout_3.addWidget(self.labelYElements, 1, 0, 1, 1)

        self.lineEditYElements = QLineEdit(self.layoutWidget4)
        self.lineEditYElements.setObjectName(u"lineEditYElements")

        self.gridLayout_3.addWidget(self.lineEditYElements, 1, 1, 1, 1)

        self.label = QLabel(self.layoutWidget4)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 2, 0, 1, 1)

        self.comboBoxElementType = QComboBox(self.layoutWidget4)
        self.comboBoxElementType.addItem("")
        self.comboBoxElementType.addItem("")
        self.comboBoxElementType.setObjectName(u"comboBoxElementType")

        self.gridLayout_3.addWidget(self.comboBoxElementType, 2, 1, 1, 1)

        self.labelOutputPath = QLabel(DialogOOF2Calculation)
        self.labelOutputPath.setObjectName(u"labelOutputPath")
        self.labelOutputPath.setGeometry(QRect(20, 360, 91, 17))
        self.pushButtonPredict = QPushButton(DialogOOF2Calculation)
        self.pushButtonPredict.setObjectName(u"pushButtonPredict")
        self.pushButtonPredict.setGeometry(QRect(500, 510, 91, 41))
        self.groupBoxSelectPhase = QGroupBox(DialogOOF2Calculation)
        self.groupBoxSelectPhase.setObjectName(u"groupBoxSelectPhase")
        self.groupBoxSelectPhase.setGeometry(QRect(10, 10, 261, 141))
        self.pushButtonGetMousePosition = QPushButton(self.groupBoxSelectPhase)
        self.pushButtonGetMousePosition.setObjectName(u"pushButtonGetMousePosition")
        self.pushButtonGetMousePosition.setGeometry(QRect(10, 60, 51, 41))
        self.layoutWidget_3 = QWidget(self.groupBoxSelectPhase)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(80, 50, 161, 58))
        self.gridLayout_6 = QGridLayout(self.layoutWidget_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.labelX = QLabel(self.layoutWidget_3)
        self.labelX.setObjectName(u"labelX")

        self.gridLayout_6.addWidget(self.labelX, 0, 0, 1, 1)

        self.lineEditX = QLineEdit(self.layoutWidget_3)
        self.lineEditX.setObjectName(u"lineEditX")

        self.gridLayout_6.addWidget(self.lineEditX, 0, 1, 1, 1)

        self.labelY = QLabel(self.layoutWidget_3)
        self.labelY.setObjectName(u"labelY")

        self.gridLayout_6.addWidget(self.labelY, 1, 0, 1, 1)

        self.lineEditY = QLineEdit(self.layoutWidget_3)
        self.lineEditY.setObjectName(u"lineEditY")

        self.gridLayout_6.addWidget(self.lineEditY, 1, 1, 1, 1)

        self.groupBoxOutput = QGroupBox(DialogOOF2Calculation)
        self.groupBoxOutput.setObjectName(u"groupBoxOutput")
        self.groupBoxOutput.setGeometry(QRect(20, 400, 571, 91))
        self.labelOutput = QLabel(self.groupBoxOutput)
        self.labelOutput.setObjectName(u"labelOutput")
        self.labelOutput.setGeometry(QRect(10, 30, 451, 51))
        self.labelOutput.setMinimumSize(QSize(0, 0))
        self.labelOutput.setAutoFillBackground(False)

        self.retranslateUi(DialogOOF2Calculation)

        QMetaObject.connectSlotsByName(DialogOOF2Calculation)
    # setupUi

    def retranslateUi(self, DialogOOF2Calculation):
        DialogOOF2Calculation.setWindowTitle(QCoreApplication.translate("DialogOOF2Calculation", u"OOF2 Calculation", None))
        self.groupBoxBoundaryCondition.setTitle(QCoreApplication.translate("DialogOOF2Calculation", u"Boundary Conditions  (In Pixel)", None))
        self.labelLeftValue.setText(QCoreApplication.translate("DialogOOF2Calculation", u"Left ", None))
        self.labelRightValue.setText(QCoreApplication.translate("DialogOOF2Calculation", u"Right ", None))
        self.pushButtonBrowseOutDir.setText("")
        self.labelStatus.setText("")
        self.groupBoxElasticConstant.setTitle(QCoreApplication.translate("DialogOOF2Calculation", u"Elastic Constants (in GPa)", None))
        self.groupBox.setTitle(QCoreApplication.translate("DialogOOF2Calculation", u"Phase 1(Continuous)", None))
        self.labelCijValue.setText(QCoreApplication.translate("DialogOOF2Calculation", u"<html><head/><body><p><span style=\" font-size:14pt;\">C</span><span style=\" font-size:14pt; vertical-align:sub;\">11</span></p></body></html>", None))
        self.labelCijValue_2.setText(QCoreApplication.translate("DialogOOF2Calculation", u"<html><head/><body><p><span style=\" font-size:14pt;\">C</span><span style=\" font-size:14pt; vertical-align:sub;\">12</span></p></body></html>", None))
        self.labelCijValue_3.setText(QCoreApplication.translate("DialogOOF2Calculation", u"<html><head/><body><p><span style=\" font-size:14pt;\">C</span><span style=\" font-size:14pt; vertical-align:sub;\">44</span></p></body></html>", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("DialogOOF2Calculation", u"Phase 2", None))
        self.labelCijValue_7.setText(QCoreApplication.translate("DialogOOF2Calculation", u"<html><head/><body><p><span style=\" font-size:14pt;\">C</span><span style=\" font-size:14pt; vertical-align:sub;\">11</span></p></body></html>", None))
        self.labelCijValue_8.setText(QCoreApplication.translate("DialogOOF2Calculation", u"<html><head/><body><p><span style=\" font-size:14pt;\">C</span><span style=\" font-size:14pt; vertical-align:sub;\">12</span></p></body></html>", None))
        self.labelCijValue_9.setText(QCoreApplication.translate("DialogOOF2Calculation", u"<html><head/><body><p><span style=\" font-size:14pt;\">C</span><span style=\" font-size:14pt; vertical-align:sub;\">44</span></p></body></html>", None))
        self.groupBoxMesh.setTitle(QCoreApplication.translate("DialogOOF2Calculation", u"Mesh", None))
        self.labelXElements.setText(QCoreApplication.translate("DialogOOF2Calculation", u"X elements", None))
        self.labelYElements.setText(QCoreApplication.translate("DialogOOF2Calculation", u"Y elements", None))
        self.label.setText(QCoreApplication.translate("DialogOOF2Calculation", u"Element type", None))
        self.comboBoxElementType.setItemText(0, QCoreApplication.translate("DialogOOF2Calculation", u"TriSkeleton", None))
        self.comboBoxElementType.setItemText(1, QCoreApplication.translate("DialogOOF2Calculation", u"QuadSkeleton", None))

        self.labelOutputPath.setText(QCoreApplication.translate("DialogOOF2Calculation", u"Output Path", None))
        self.pushButtonPredict.setText(QCoreApplication.translate("DialogOOF2Calculation", u"Predict", None))
        self.groupBoxSelectPhase.setTitle(QCoreApplication.translate("DialogOOF2Calculation", u"Select Phase 1 (Continuous)", None))
        self.pushButtonGetMousePosition.setText("")
        self.labelX.setText(QCoreApplication.translate("DialogOOF2Calculation", u"X", None))
        self.labelY.setText(QCoreApplication.translate("DialogOOF2Calculation", u"Y", None))
        self.groupBoxOutput.setTitle(QCoreApplication.translate("DialogOOF2Calculation", u"Output", None))
        self.labelOutput.setText("")
    # retranslateUi

