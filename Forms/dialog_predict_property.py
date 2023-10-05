# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_predict_property.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogPredictProperty(object):
    def setupUi(self, DialogPredictProperty):
        if not DialogPredictProperty.objectName():
            DialogPredictProperty.setObjectName(u"DialogPredictProperty")
        DialogPredictProperty.resize(790, 602)
        self.pushButtonPredict = QPushButton(DialogPredictProperty)
        self.pushButtonPredict.setObjectName(u"pushButtonPredict")
        self.pushButtonPredict.setGeometry(QRect(660, 310, 101, 41))
        self.labelPlot = QLabel(DialogPredictProperty)
        self.labelPlot.setObjectName(u"labelPlot")
        self.labelPlot.setGeometry(QRect(30, 30, 512, 512))
        self.pushButtonParameters = QPushButton(DialogPredictProperty)
        self.pushButtonParameters.setObjectName(u"pushButtonParameters")
        self.pushButtonParameters.setGeometry(QRect(660, 110, 121, 41))
        self.groupBoxSelectPhase = QGroupBox(DialogPredictProperty)
        self.groupBoxSelectPhase.setObjectName(u"groupBoxSelectPhase")
        self.groupBoxSelectPhase.setGeometry(QRect(550, 20, 231, 71))
        self.labelX = QLabel(self.groupBoxSelectPhase)
        self.labelX.setObjectName(u"labelX")
        self.labelX.setGeometry(QRect(10, 40, 31, 17))
        self.labelY = QLabel(self.groupBoxSelectPhase)
        self.labelY.setObjectName(u"labelY")
        self.labelY.setGeometry(QRect(130, 40, 21, 16))
        self.lineEditX = QLineEdit(self.groupBoxSelectPhase)
        self.lineEditX.setObjectName(u"lineEditX")
        self.lineEditX.setGeometry(QRect(30, 30, 71, 31))
        self.lineEditY = QLineEdit(self.groupBoxSelectPhase)
        self.lineEditY.setObjectName(u"lineEditY")
        self.lineEditY.setGeometry(QRect(150, 30, 71, 31))
        self.groupBoxOutput = QGroupBox(DialogPredictProperty)
        self.groupBoxOutput.setObjectName(u"groupBoxOutput")
        self.groupBoxOutput.setGeometry(QRect(550, 170, 231, 80))
        self.pushButtonBrowseOutDir = QPushButton(self.groupBoxOutput)
        self.pushButtonBrowseOutDir.setObjectName(u"pushButtonBrowseOutDir")
        self.pushButtonBrowseOutDir.setGeometry(QRect(10, 30, 31, 31))
        self.lineEditOutDir = QLineEdit(self.groupBoxOutput)
        self.lineEditOutDir.setObjectName(u"lineEditOutDir")
        self.lineEditOutDir.setGeometry(QRect(40, 30, 181, 31))
        self.groupBox = QGroupBox(DialogPredictProperty)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(550, 370, 221, 111))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelOutput = QLabel(self.groupBox)
        self.labelOutput.setObjectName(u"labelOutput")
        self.labelOutput.setMinimumSize(QSize(0, 0))

        self.verticalLayout.addWidget(self.labelOutput)


        self.retranslateUi(DialogPredictProperty)

        QMetaObject.connectSlotsByName(DialogPredictProperty)
    # setupUi

    def retranslateUi(self, DialogPredictProperty):
        DialogPredictProperty.setWindowTitle(QCoreApplication.translate("DialogPredictProperty", u"Predict Property", None))
        self.pushButtonPredict.setText(QCoreApplication.translate("DialogPredictProperty", u"Predict", None))
        self.labelPlot.setText("")
        self.pushButtonParameters.setText(QCoreApplication.translate("DialogPredictProperty", u"Parameters", None))
        self.groupBoxSelectPhase.setTitle(QCoreApplication.translate("DialogPredictProperty", u"Select Phase 1", None))
        self.labelX.setText(QCoreApplication.translate("DialogPredictProperty", u"X", None))
        self.labelY.setText(QCoreApplication.translate("DialogPredictProperty", u"Y", None))
        self.groupBoxOutput.setTitle(QCoreApplication.translate("DialogPredictProperty", u"Output Path", None))
        self.pushButtonBrowseOutDir.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("DialogPredictProperty", u"Output", None))
        self.labelOutput.setText("")
    # retranslateUi

