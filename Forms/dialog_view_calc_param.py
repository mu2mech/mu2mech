# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_view_calc_param.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogViewCalcParam(object):
    def setupUi(self, DialogViewCalcParam):
        if not DialogViewCalcParam.objectName():
            DialogViewCalcParam.setObjectName(u"DialogViewCalcParam")
        DialogViewCalcParam.resize(670, 450)
        self.pushButtonSave = QPushButton(DialogViewCalcParam)
        self.pushButtonSave.setObjectName(u"pushButtonSave")
        self.pushButtonSave.setGeometry(QRect(550, 400, 111, 31))
        self.groupBox = QGroupBox(DialogViewCalcParam)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(440, 10, 221, 81))
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 30, 191, 42))
        self.gridLayout_2 = QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.labelInflextionPoint = QLabel(self.layoutWidget)
        self.labelInflextionPoint.setObjectName(u"labelInflextionPoint")

        self.gridLayout_2.addWidget(self.labelInflextionPoint, 0, 0, 1, 1)

        self.labelInflextionPointValue = QLabel(self.layoutWidget)
        self.labelInflextionPointValue.setObjectName(u"labelInflextionPointValue")

        self.gridLayout_2.addWidget(self.labelInflextionPointValue, 0, 1, 1, 1)

        self.labelBinodalPoint = QLabel(self.layoutWidget)
        self.labelBinodalPoint.setObjectName(u"labelBinodalPoint")

        self.gridLayout_2.addWidget(self.labelBinodalPoint, 1, 0, 1, 1)

        self.labelBinodalPointValue = QLabel(self.layoutWidget)
        self.labelBinodalPointValue.setObjectName(u"labelBinodalPointValue")

        self.gridLayout_2.addWidget(self.labelBinodalPointValue, 1, 1, 1, 1)

        self.groupBox_2 = QGroupBox(DialogViewCalcParam)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(440, 120, 221, 121))
        self.layoutWidget1 = QWidget(self.groupBox_2)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 30, 199, 82))
        self.gridLayout = QGridLayout(self.layoutWidget1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelInterfacialEnergy = QLabel(self.layoutWidget1)
        self.labelInterfacialEnergy.setObjectName(u"labelInterfacialEnergy")

        self.gridLayout.addWidget(self.labelInterfacialEnergy, 0, 0, 1, 1)

        self.labelInterfacialEnergyValue = QLabel(self.layoutWidget1)
        self.labelInterfacialEnergyValue.setObjectName(u"labelInterfacialEnergyValue")

        self.gridLayout.addWidget(self.labelInterfacialEnergyValue, 0, 1, 1, 1)

        self.labelDiffusivity = QLabel(self.layoutWidget1)
        self.labelDiffusivity.setObjectName(u"labelDiffusivity")

        self.gridLayout.addWidget(self.labelDiffusivity, 1, 0, 1, 1)

        self.labelDiffusivityValue = QLabel(self.layoutWidget1)
        self.labelDiffusivityValue.setObjectName(u"labelDiffusivityValue")

        self.gridLayout.addWidget(self.labelDiffusivityValue, 1, 1, 1, 1)

        self.labelBarrierHeight = QLabel(self.layoutWidget1)
        self.labelBarrierHeight.setObjectName(u"labelBarrierHeight")

        self.gridLayout.addWidget(self.labelBarrierHeight, 2, 0, 1, 1)

        self.labelBarrierHeightValue = QLabel(self.layoutWidget1)
        self.labelBarrierHeightValue.setObjectName(u"labelBarrierHeightValue")

        self.gridLayout.addWidget(self.labelBarrierHeightValue, 2, 1, 1, 1)

        self.frame = QFrame(DialogViewCalcParam)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 10, 420, 420))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.labelGXPlot = QLabel(self.frame)
        self.labelGXPlot.setObjectName(u"labelGXPlot")
        self.labelGXPlot.setGeometry(QRect(10, 10, 400, 400))

        self.retranslateUi(DialogViewCalcParam)

        QMetaObject.connectSlotsByName(DialogViewCalcParam)
    # setupUi

    def retranslateUi(self, DialogViewCalcParam):
        DialogViewCalcParam.setWindowTitle(QCoreApplication.translate("DialogViewCalcParam", u"View Calculation Parameters", None))
        self.pushButtonSave.setText(QCoreApplication.translate("DialogViewCalcParam", u"Save Data", None))
        self.groupBox.setTitle(QCoreApplication.translate("DialogViewCalcParam", u"Gibbs Plot Data", None))
        self.labelInflextionPoint.setText(QCoreApplication.translate("DialogViewCalcParam", u"<html><head/><body><p align=\"right\">Inflextion points:</p></body></html>", None))
        self.labelInflextionPointValue.setText("")
        self.labelBinodalPoint.setText(QCoreApplication.translate("DialogViewCalcParam", u"<html><head/><body><p align=\"right\">Binodal points:</p></body></html>", None))
        self.labelBinodalPointValue.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("DialogViewCalcParam", u"Other Data", None))
        self.labelInterfacialEnergy.setText(QCoreApplication.translate("DialogViewCalcParam", u"<html><head/><body><p align=\"right\">Interfacial Energy:</p></body></html>", None))
        self.labelInterfacialEnergyValue.setText("")
        self.labelDiffusivity.setText(QCoreApplication.translate("DialogViewCalcParam", u"<html><head/><body><p align=\"right\">Diffusivity:</p></body></html>", None))
        self.labelDiffusivityValue.setText("")
        self.labelBarrierHeight.setText(QCoreApplication.translate("DialogViewCalcParam", u"<html><head/><body><p align=\"right\">Barrier Height:</p></body></html>", None))
        self.labelBarrierHeightValue.setText("")
        self.labelGXPlot.setText("")
    # retranslateUi

