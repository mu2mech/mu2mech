# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_plot_colors.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogPlotColors(object):
    def setupUi(self, DialogPlotColors):
        if not DialogPlotColors.objectName():
            DialogPlotColors.setObjectName(u"DialogPlotColors")
        DialogPlotColors.resize(331, 482)
        self.buttonBox = QDialogButtonBox(DialogPlotColors)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(80, 410, 221, 41))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.groupBox_3 = QGroupBox(DialogPlotColors)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(30, 20, 271, 101))
        self.layoutWidget_3 = QWidget(self.groupBox_3)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(20, 30, 231, 58))
        self.gridLayout_3 = QGridLayout(self.layoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.labelColor = QLabel(self.layoutWidget_3)
        self.labelColor.setObjectName(u"labelColor")

        self.gridLayout_3.addWidget(self.labelColor, 0, 0, 1, 1)

        self.comboBoxColor = QComboBox(self.layoutWidget_3)
        self.comboBoxColor.setObjectName(u"comboBoxColor")

        self.gridLayout_3.addWidget(self.comboBoxColor, 0, 1, 1, 1)

        self.labelLThickness = QLabel(self.layoutWidget_3)
        self.labelLThickness.setObjectName(u"labelLThickness")

        self.gridLayout_3.addWidget(self.labelLThickness, 1, 0, 1, 1)

        self.lineEditLThickness = QLineEdit(self.layoutWidget_3)
        self.lineEditLThickness.setObjectName(u"lineEditLThickness")

        self.gridLayout_3.addWidget(self.lineEditLThickness, 1, 1, 1, 1)

        self.groupBox = QGroupBox(DialogPlotColors)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 150, 271, 231))
        self.groupBox_5 = QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(20, 40, 231, 121))
        self.layoutWidget = QWidget(self.groupBox_5)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 40, 196, 61))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.radioButtonContinuous = QRadioButton(self.layoutWidget)
        self.radioButtonContinuous.setObjectName(u"radioButtonContinuous")

        self.gridLayout.addWidget(self.radioButtonContinuous, 0, 0, 1, 1)

        self.radioButtonDiscrete = QRadioButton(self.layoutWidget)
        self.radioButtonDiscrete.setObjectName(u"radioButtonDiscrete")

        self.gridLayout.addWidget(self.radioButtonDiscrete, 1, 0, 1, 1)

        self.comboBoxDiscrete = QComboBox(self.layoutWidget)
        self.comboBoxDiscrete.setObjectName(u"comboBoxDiscrete")

        self.gridLayout.addWidget(self.comboBoxDiscrete, 1, 1, 1, 1)

        self.comboBoxContinuous = QComboBox(self.layoutWidget)
        self.comboBoxContinuous.setObjectName(u"comboBoxContinuous")

        self.gridLayout.addWidget(self.comboBoxContinuous, 0, 1, 1, 1)

        self.layoutWidget_2 = QWidget(self.groupBox)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(20, 180, 231, 27))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBoxPlotType = QComboBox(self.layoutWidget_2)
        self.comboBoxPlotType.addItem("")
        self.comboBoxPlotType.addItem("")
        self.comboBoxPlotType.setObjectName(u"comboBoxPlotType")

        self.horizontalLayout.addWidget(self.comboBoxPlotType)


        self.retranslateUi(DialogPlotColors)
        self.buttonBox.accepted.connect(DialogPlotColors.accept)
        self.buttonBox.rejected.connect(DialogPlotColors.reject)

        QMetaObject.connectSlotsByName(DialogPlotColors)
    # setupUi

    def retranslateUi(self, DialogPlotColors):
        DialogPlotColors.setWindowTitle(QCoreApplication.translate("DialogPlotColors", u"Plot Colors", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("DialogPlotColors", u"2D Line Plot", None))
        self.labelColor.setText(QCoreApplication.translate("DialogPlotColors", u"Color", None))
        self.labelLThickness.setText(QCoreApplication.translate("DialogPlotColors", u"Line Width", None))
        self.groupBox.setTitle(QCoreApplication.translate("DialogPlotColors", u"Microstructure Plot", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("DialogPlotColors", u"Color Gradient Type", None))
        self.radioButtonContinuous.setText(QCoreApplication.translate("DialogPlotColors", u"Continious ", None))
        self.radioButtonDiscrete.setText(QCoreApplication.translate("DialogPlotColors", u"Discrete ", None))
        self.label.setText(QCoreApplication.translate("DialogPlotColors", u"Plot Type", None))
        self.comboBoxPlotType.setItemText(0, QCoreApplication.translate("DialogPlotColors", u"volume", None))
        self.comboBoxPlotType.setItemText(1, QCoreApplication.translate("DialogPlotColors", u"surface", None))

    # retranslateUi

