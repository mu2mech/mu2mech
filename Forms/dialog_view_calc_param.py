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
        DialogViewCalcParam.resize(700, 440)
        self.frame = QFrame(DialogViewCalcParam)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 10, 420, 420))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.labelGXPlot = QLabel(self.frame)
        self.labelGXPlot.setObjectName(u"labelGXPlot")
        self.labelGXPlot.setGeometry(QRect(10, 10, 400, 400))
        self.layoutWidget = QWidget(DialogViewCalcParam)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(440, 11, 241, 161))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelInflextionPoint = QLabel(self.layoutWidget)
        self.labelInflextionPoint.setObjectName(u"labelInflextionPoint")

        self.gridLayout.addWidget(self.labelInflextionPoint, 0, 0, 1, 1)

        self.labelInflextionPointValue = QLabel(self.layoutWidget)
        self.labelInflextionPointValue.setObjectName(u"labelInflextionPointValue")

        self.gridLayout.addWidget(self.labelInflextionPointValue, 0, 1, 1, 1)

        self.labelBinodalPoint = QLabel(self.layoutWidget)
        self.labelBinodalPoint.setObjectName(u"labelBinodalPoint")

        self.gridLayout.addWidget(self.labelBinodalPoint, 1, 0, 1, 1)

        self.labelBinodalPointValue = QLabel(self.layoutWidget)
        self.labelBinodalPointValue.setObjectName(u"labelBinodalPointValue")

        self.gridLayout.addWidget(self.labelBinodalPointValue, 1, 1, 1, 1)

        self.labelBarrierHeight = QLabel(self.layoutWidget)
        self.labelBarrierHeight.setObjectName(u"labelBarrierHeight")

        self.gridLayout.addWidget(self.labelBarrierHeight, 2, 0, 1, 1)

        self.labelBarrierHeightValue = QLabel(self.layoutWidget)
        self.labelBarrierHeightValue.setObjectName(u"labelBarrierHeightValue")

        self.gridLayout.addWidget(self.labelBarrierHeightValue, 2, 1, 1, 1)

        self.labelDiffusivity = QLabel(self.layoutWidget)
        self.labelDiffusivity.setObjectName(u"labelDiffusivity")

        self.gridLayout.addWidget(self.labelDiffusivity, 3, 0, 1, 1)

        self.labelDiffusivityValue = QLabel(self.layoutWidget)
        self.labelDiffusivityValue.setObjectName(u"labelDiffusivityValue")

        self.gridLayout.addWidget(self.labelDiffusivityValue, 3, 1, 1, 1)

        self.labelGBEnergy = QLabel(self.layoutWidget)
        self.labelGBEnergy.setObjectName(u"labelGBEnergy")

        self.gridLayout.addWidget(self.labelGBEnergy, 4, 0, 1, 1)

        self.labelGBEnergyValue = QLabel(self.layoutWidget)
        self.labelGBEnergyValue.setObjectName(u"labelGBEnergyValue")

        self.gridLayout.addWidget(self.labelGBEnergyValue, 4, 1, 1, 1)


        self.retranslateUi(DialogViewCalcParam)

        QMetaObject.connectSlotsByName(DialogViewCalcParam)
    # setupUi

    def retranslateUi(self, DialogViewCalcParam):
        DialogViewCalcParam.setWindowTitle(QCoreApplication.translate("DialogViewCalcParam", u"View Calculation Parameters", None))
        self.labelGXPlot.setText("")
        self.labelInflextionPoint.setText(QCoreApplication.translate("DialogViewCalcParam", u"<html><head/><body><p align=\"right\">Inflextion points:</p></body></html>", None))
        self.labelInflextionPointValue.setText("")
        self.labelBinodalPoint.setText(QCoreApplication.translate("DialogViewCalcParam", u"<html><head/><body><p align=\"right\">Binodal points:</p></body></html>", None))
        self.labelBinodalPointValue.setText("")
        self.labelBarrierHeight.setText(QCoreApplication.translate("DialogViewCalcParam", u"<html><head/><body><p align=\"right\">H (KJ/mole):</p></body></html>", None))
        self.labelBarrierHeightValue.setText("")
        self.labelDiffusivity.setText(QCoreApplication.translate("DialogViewCalcParam", u"<html><head/><body><p align=\"right\">D (m<span style=\" vertical-align:super;\">2</span>/sec):</p></body></html>", None))
        self.labelDiffusivityValue.setText("")
        self.labelGBEnergy.setText(QCoreApplication.translate("DialogViewCalcParam", u"<html><head/><body><p align=\"right\"><span style=\" font-family:'Google Sans,arial,sans-serif'; color:#202124; background-color:#ffffff;\">\u03c3 </span>(J/m<span style=\" vertical-align:super;\">2</span>):</p></body></html>", None))
        self.labelGBEnergyValue.setText("")
    # retranslateUi

