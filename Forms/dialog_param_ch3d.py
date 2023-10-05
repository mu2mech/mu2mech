# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_param_ch3d.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogParamCH3D(object):
    def setupUi(self, DialogParamCH3D):
        if not DialogParamCH3D.objectName():
            DialogParamCH3D.setObjectName(u"DialogParamCH3D")
        DialogParamCH3D.resize(420, 320)
        self.buttonBoxParamCH3D = QDialogButtonBox(DialogParamCH3D)
        self.buttonBoxParamCH3D.setObjectName(u"buttonBoxParamCH3D")
        self.buttonBoxParamCH3D.setGeometry(QRect(50, 260, 341, 32))
        self.buttonBoxParamCH3D.setOrientation(Qt.Horizontal)
        self.buttonBoxParamCH3D.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.layoutWidget = QWidget(DialogParamCH3D)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(30, 40, 361, 191))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelFluctuation = QLabel(self.layoutWidget)
        self.labelFluctuation.setObjectName(u"labelFluctuation")
        self.labelFluctuation.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelFluctuation, 0, 0, 1, 1)

        self.lineEditFluctuation = QLineEdit(self.layoutWidget)
        self.lineEditFluctuation.setObjectName(u"lineEditFluctuation")

        self.gridLayout.addWidget(self.lineEditFluctuation, 0, 1, 1, 1)

        self.labelMobiliy = QLabel(self.layoutWidget)
        self.labelMobiliy.setObjectName(u"labelMobiliy")
        self.labelMobiliy.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelMobiliy, 0, 2, 1, 1)

        self.lineEditMobility = QLineEdit(self.layoutWidget)
        self.lineEditMobility.setObjectName(u"lineEditMobility")

        self.gridLayout.addWidget(self.lineEditMobility, 0, 3, 1, 1)

        self.labelCAvg = QLabel(self.layoutWidget)
        self.labelCAvg.setObjectName(u"labelCAvg")
        self.labelCAvg.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelCAvg, 1, 0, 1, 1)

        self.lineEditCAvg = QLineEdit(self.layoutWidget)
        self.lineEditCAvg.setObjectName(u"lineEditCAvg")

        self.gridLayout.addWidget(self.lineEditCAvg, 1, 1, 1, 1)

        self.labelDelT = QLabel(self.layoutWidget)
        self.labelDelT.setObjectName(u"labelDelT")
        self.labelDelT.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelDelT, 1, 2, 1, 1)

        self.lineEditDelT = QLineEdit(self.layoutWidget)
        self.lineEditDelT.setObjectName(u"lineEditDelT")

        self.gridLayout.addWidget(self.lineEditDelT, 1, 3, 1, 1)

        self.labelLx = QLabel(self.layoutWidget)
        self.labelLx.setObjectName(u"labelLx")
        self.labelLx.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelLx, 2, 0, 1, 1)

        self.lineEditLx = QLineEdit(self.layoutWidget)
        self.lineEditLx.setObjectName(u"lineEditLx")

        self.gridLayout.addWidget(self.lineEditLx, 2, 1, 1, 1)

        self.labelKappa = QLabel(self.layoutWidget)
        self.labelKappa.setObjectName(u"labelKappa")
        self.labelKappa.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelKappa, 2, 2, 1, 1)

        self.lineEditKappa = QLineEdit(self.layoutWidget)
        self.lineEditKappa.setObjectName(u"lineEditKappa")

        self.gridLayout.addWidget(self.lineEditKappa, 2, 3, 1, 1)

        self.labelLy = QLabel(self.layoutWidget)
        self.labelLy.setObjectName(u"labelLy")
        self.labelLy.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelLy, 3, 0, 1, 1)

        self.lineEditLy = QLineEdit(self.layoutWidget)
        self.lineEditLy.setObjectName(u"lineEditLy")

        self.gridLayout.addWidget(self.lineEditLy, 3, 1, 1, 1)

        self.labelDelX = QLabel(self.layoutWidget)
        self.labelDelX.setObjectName(u"labelDelX")
        self.labelDelX.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelDelX, 3, 2, 1, 1)

        self.lineEditDelX = QLineEdit(self.layoutWidget)
        self.lineEditDelX.setObjectName(u"lineEditDelX")

        self.gridLayout.addWidget(self.lineEditDelX, 3, 3, 1, 1)

        self.labelLz = QLabel(self.layoutWidget)
        self.labelLz.setObjectName(u"labelLz")
        self.labelLz.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelLz, 4, 0, 1, 1)

        self.lineEditLz = QLineEdit(self.layoutWidget)
        self.lineEditLz.setObjectName(u"lineEditLz")

        self.gridLayout.addWidget(self.lineEditLz, 4, 1, 1, 1)

        self.labelDelY = QLabel(self.layoutWidget)
        self.labelDelY.setObjectName(u"labelDelY")
        self.labelDelY.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelDelY, 4, 2, 1, 1)

        self.lineEditDelY = QLineEdit(self.layoutWidget)
        self.lineEditDelY.setObjectName(u"lineEditDelY")

        self.gridLayout.addWidget(self.lineEditDelY, 4, 3, 1, 1)

        self.labelDelZ = QLabel(self.layoutWidget)
        self.labelDelZ.setObjectName(u"labelDelZ")
        self.labelDelZ.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelDelZ, 5, 2, 1, 1)

        self.lineEditDelZ = QLineEdit(self.layoutWidget)
        self.lineEditDelZ.setObjectName(u"lineEditDelZ")

        self.gridLayout.addWidget(self.lineEditDelZ, 5, 3, 1, 1)


        self.retranslateUi(DialogParamCH3D)
        self.buttonBoxParamCH3D.accepted.connect(DialogParamCH3D.accept)
        self.buttonBoxParamCH3D.rejected.connect(DialogParamCH3D.reject)

        QMetaObject.connectSlotsByName(DialogParamCH3D)
    # setupUi

    def retranslateUi(self, DialogParamCH3D):
        DialogParamCH3D.setWindowTitle(QCoreApplication.translate("DialogParamCH3D", u"Edit Parameters ", None))
        self.labelFluctuation.setText(QCoreApplication.translate("DialogParamCH3D", u"fluctuation", None))
        self.labelMobiliy.setText(QCoreApplication.translate("DialogParamCH3D", u"Mobility", None))
        self.labelCAvg.setText(QCoreApplication.translate("DialogParamCH3D", u"Average\n"
"composition", None))
        self.labelDelT.setText(QCoreApplication.translate("DialogParamCH3D", u"delta t", None))
        self.labelLx.setText(QCoreApplication.translate("DialogParamCH3D", u"lx", None))
        self.labelKappa.setText(QCoreApplication.translate("DialogParamCH3D", u"Kappa", None))
        self.labelLy.setText(QCoreApplication.translate("DialogParamCH3D", u"ly", None))
        self.labelDelX.setText(QCoreApplication.translate("DialogParamCH3D", u"delta x", None))
        self.labelLz.setText(QCoreApplication.translate("DialogParamCH3D", u"lz", None))
        self.labelDelY.setText(QCoreApplication.translate("DialogParamCH3D", u"delta y", None))
        self.labelDelZ.setText(QCoreApplication.translate("DialogParamCH3D", u"delta z", None))
    # retranslateUi

