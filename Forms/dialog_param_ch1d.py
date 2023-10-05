# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_param_ch1d.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_DialogParamCH1D(object):
    def setupUi(self, DialogParamCH1D):
        if not DialogParamCH1D.objectName():
            DialogParamCH1D.setObjectName(u"DialogParamCH1D")
        DialogParamCH1D.resize(250, 300)
        self.buttonBoxPramCH1D = QDialogButtonBox(DialogParamCH1D)
        self.buttonBoxPramCH1D.setObjectName(u"buttonBoxPramCH1D")
        self.buttonBoxPramCH1D.setGeometry(QRect(70, 250, 161, 32))
        self.buttonBoxPramCH1D.setOrientation(Qt.Horizontal)
        self.buttonBoxPramCH1D.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.layoutWidget = QWidget(DialogParamCH1D)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 30, 211, 211))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelLx = QLabel(self.layoutWidget)
        self.labelLx.setObjectName(u"labelLx")

        self.gridLayout.addWidget(self.labelLx, 0, 1, 1, 1)

        self.lineEditKappa = QLineEdit(self.layoutWidget)
        self.lineEditKappa.setObjectName(u"lineEditKappa")

        self.gridLayout.addWidget(self.lineEditKappa, 2, 0, 1, 1)

        self.lineEditDelX = QLineEdit(self.layoutWidget)
        self.lineEditDelX.setObjectName(u"lineEditDelX")

        self.gridLayout.addWidget(self.lineEditDelX, 3, 0, 1, 1)

        self.labelDelX = QLabel(self.layoutWidget)
        self.labelDelX.setObjectName(u"labelDelX")

        self.gridLayout.addWidget(self.labelDelX, 3, 1, 1, 1)

        self.labelKappa = QLabel(self.layoutWidget)
        self.labelKappa.setObjectName(u"labelKappa")

        self.gridLayout.addWidget(self.labelKappa, 2, 1, 1, 1)

        self.lineEditDelT = QLineEdit(self.layoutWidget)
        self.lineEditDelT.setObjectName(u"lineEditDelT")

        self.gridLayout.addWidget(self.lineEditDelT, 1, 0, 1, 1)

        self.labelDelT = QLabel(self.layoutWidget)
        self.labelDelT.setObjectName(u"labelDelT")

        self.gridLayout.addWidget(self.labelDelT, 1, 1, 1, 1)

        self.lineEditDTilda = QLineEdit(self.layoutWidget)
        self.lineEditDTilda.setObjectName(u"lineEditDTilda")

        self.gridLayout.addWidget(self.lineEditDTilda, 4, 0, 1, 1)

        self.lineEditLx = QLineEdit(self.layoutWidget)
        self.lineEditLx.setObjectName(u"lineEditLx")

        self.gridLayout.addWidget(self.lineEditLx, 0, 0, 1, 1)

        self.labelDTilda = QLabel(self.layoutWidget)
        self.labelDTilda.setObjectName(u"labelDTilda")

        self.gridLayout.addWidget(self.labelDTilda, 4, 1, 1, 1)


        self.retranslateUi(DialogParamCH1D)

        QMetaObject.connectSlotsByName(DialogParamCH1D)
    # setupUi

    def retranslateUi(self, DialogParamCH1D):
        DialogParamCH1D.setWindowTitle(QCoreApplication.translate("DialogParamCH1D", u"Dialog", None))
        self.labelLx.setText(QCoreApplication.translate("DialogParamCH1D", u"length", None))
        self.labelDelX.setText(QCoreApplication.translate("DialogParamCH1D", u"delta x", None))
        self.labelKappa.setText(QCoreApplication.translate("DialogParamCH1D", u"Kappa", None))
        self.labelDelT.setText(QCoreApplication.translate("DialogParamCH1D", u"delta t", None))
        self.labelDTilda.setText(QCoreApplication.translate("DialogParamCH1D", u"d tilda", None))
    # retranslateUi

