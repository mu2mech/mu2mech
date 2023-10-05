# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_new_calc.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogNewCalc(object):
    def setupUi(self, DialogNewCalc):
        if not DialogNewCalc.objectName():
            DialogNewCalc.setObjectName(u"DialogNewCalc")
        DialogNewCalc.resize(320, 150)
        self.label = QLabel(DialogNewCalc)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 120, 81, 21))
        self.layoutWidget = QWidget(DialogNewCalc)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 297, 101))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelCalType = QLabel(self.layoutWidget)
        self.labelCalType.setObjectName(u"labelCalType")

        self.horizontalLayout.addWidget(self.labelCalType)

        self.comboBoxCalType = QComboBox(self.layoutWidget)
        self.comboBoxCalType.addItem("")
        self.comboBoxCalType.addItem("")
        self.comboBoxCalType.addItem("")
        self.comboBoxCalType.addItem("")
        self.comboBoxCalType.setObjectName(u"comboBoxCalType")

        self.horizontalLayout.addWidget(self.comboBoxCalType)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBoxNew = QDialogButtonBox(self.layoutWidget)
        self.buttonBoxNew.setObjectName(u"buttonBoxNew")
        self.buttonBoxNew.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBoxNew)


        self.retranslateUi(DialogNewCalc)

        QMetaObject.connectSlotsByName(DialogNewCalc)
    # setupUi

    def retranslateUi(self, DialogNewCalc):
        DialogNewCalc.setWindowTitle(QCoreApplication.translate("DialogNewCalc", u"New", None))
        self.label.setText("")
        self.labelCalType.setText(QCoreApplication.translate("DialogNewCalc", u"Calculation type", None))
        self.comboBoxCalType.setItemText(0, "")
        self.comboBoxCalType.setItemText(1, QCoreApplication.translate("DialogNewCalc", u"Cahn Hilliard 2D", None))
        self.comboBoxCalType.setItemText(2, QCoreApplication.translate("DialogNewCalc", u"Cahn Hilliard 2D alloy", None))
        self.comboBoxCalType.setItemText(3, QCoreApplication.translate("DialogNewCalc", u"Cahn Hilliard 3D alloy", None))

    # retranslateUi

