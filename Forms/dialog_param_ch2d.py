# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_param_ch2d.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogParamCH2D(object):
    def setupUi(self, DialogParamCH2D):
        if not DialogParamCH2D.objectName():
            DialogParamCH2D.setObjectName(u"DialogParamCH2D")
        DialogParamCH2D.resize(250, 433)
        self.layoutWidget = QWidget(DialogParamCH2D)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 30, 211, 341))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEditFluctuation = QLineEdit(self.layoutWidget)
        self.lineEditFluctuation.setObjectName(u"lineEditFluctuation")

        self.gridLayout.addWidget(self.lineEditFluctuation, 0, 0, 1, 1)

        self.labelFluctuation = QLabel(self.layoutWidget)
        self.labelFluctuation.setObjectName(u"labelFluctuation")

        self.gridLayout.addWidget(self.labelFluctuation, 0, 1, 1, 1)

        self.lineEditCAvg = QLineEdit(self.layoutWidget)
        self.lineEditCAvg.setObjectName(u"lineEditCAvg")

        self.gridLayout.addWidget(self.lineEditCAvg, 1, 0, 1, 1)

        self.labelCAvg = QLabel(self.layoutWidget)
        self.labelCAvg.setObjectName(u"labelCAvg")

        self.gridLayout.addWidget(self.labelCAvg, 1, 1, 1, 1)

        self.lineEditLx = QLineEdit(self.layoutWidget)
        self.lineEditLx.setObjectName(u"lineEditLx")

        self.gridLayout.addWidget(self.lineEditLx, 2, 0, 1, 1)

        self.labelLx = QLabel(self.layoutWidget)
        self.labelLx.setObjectName(u"labelLx")

        self.gridLayout.addWidget(self.labelLx, 2, 1, 1, 1)

        self.lineEditLy = QLineEdit(self.layoutWidget)
        self.lineEditLy.setObjectName(u"lineEditLy")

        self.gridLayout.addWidget(self.lineEditLy, 3, 0, 1, 1)

        self.labelLy = QLabel(self.layoutWidget)
        self.labelLy.setObjectName(u"labelLy")

        self.gridLayout.addWidget(self.labelLy, 3, 1, 1, 1)

        self.lineEditMobility = QLineEdit(self.layoutWidget)
        self.lineEditMobility.setObjectName(u"lineEditMobility")

        self.gridLayout.addWidget(self.lineEditMobility, 4, 0, 1, 1)

        self.labelMobiliy = QLabel(self.layoutWidget)
        self.labelMobiliy.setObjectName(u"labelMobiliy")

        self.gridLayout.addWidget(self.labelMobiliy, 4, 1, 1, 1)

        self.lineEditDelT = QLineEdit(self.layoutWidget)
        self.lineEditDelT.setObjectName(u"lineEditDelT")

        self.gridLayout.addWidget(self.lineEditDelT, 5, 0, 1, 1)

        self.labelDelT = QLabel(self.layoutWidget)
        self.labelDelT.setObjectName(u"labelDelT")

        self.gridLayout.addWidget(self.labelDelT, 5, 1, 1, 1)

        self.lineEditKappa = QLineEdit(self.layoutWidget)
        self.lineEditKappa.setObjectName(u"lineEditKappa")

        self.gridLayout.addWidget(self.lineEditKappa, 6, 0, 1, 1)

        self.labelKappa = QLabel(self.layoutWidget)
        self.labelKappa.setObjectName(u"labelKappa")

        self.gridLayout.addWidget(self.labelKappa, 6, 1, 1, 1)

        self.lineEditDelX = QLineEdit(self.layoutWidget)
        self.lineEditDelX.setObjectName(u"lineEditDelX")

        self.gridLayout.addWidget(self.lineEditDelX, 7, 0, 1, 1)

        self.labelDelX = QLabel(self.layoutWidget)
        self.labelDelX.setObjectName(u"labelDelX")

        self.gridLayout.addWidget(self.labelDelX, 7, 1, 1, 1)

        self.lineEditDelY = QLineEdit(self.layoutWidget)
        self.lineEditDelY.setObjectName(u"lineEditDelY")

        self.gridLayout.addWidget(self.lineEditDelY, 8, 0, 1, 1)

        self.labelDelY = QLabel(self.layoutWidget)
        self.labelDelY.setObjectName(u"labelDelY")

        self.gridLayout.addWidget(self.labelDelY, 8, 1, 1, 1)

        self.buttonBoxPramCH2D = QPushButton(DialogParamCH2D)
        self.buttonBoxPramCH2D.setObjectName(u"buttonBoxPramCH2D")
        self.buttonBoxPramCH2D.setGeometry(QRect(140, 390, 89, 25))

        self.retranslateUi(DialogParamCH2D)

        QMetaObject.connectSlotsByName(DialogParamCH2D)
    # setupUi

    def retranslateUi(self, DialogParamCH2D):
        DialogParamCH2D.setWindowTitle(QCoreApplication.translate("DialogParamCH2D", u"Edit Parameters", None))
        self.labelFluctuation.setText(QCoreApplication.translate("DialogParamCH2D", u"fluctuation", None))
        self.labelCAvg.setText(QCoreApplication.translate("DialogParamCH2D", u"Average\n"
"Composition", None))
        self.labelLx.setText(QCoreApplication.translate("DialogParamCH2D", u"lx", None))
        self.labelLy.setText(QCoreApplication.translate("DialogParamCH2D", u"ly", None))
        self.labelMobiliy.setText(QCoreApplication.translate("DialogParamCH2D", u"Mobility", None))
        self.labelDelT.setText(QCoreApplication.translate("DialogParamCH2D", u"delta t", None))
        self.labelKappa.setText(QCoreApplication.translate("DialogParamCH2D", u"Kappa", None))
        self.labelDelX.setText(QCoreApplication.translate("DialogParamCH2D", u"delta x", None))
        self.labelDelY.setText(QCoreApplication.translate("DialogParamCH2D", u"delta y", None))
        self.buttonBoxPramCH2D.setText(QCoreApplication.translate("DialogParamCH2D", u"OK", None))
    # retranslateUi

