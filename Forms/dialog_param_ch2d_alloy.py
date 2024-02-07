# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_param_ch2d_alloy.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogParamCH2DAlloy(object):
    def setupUi(self, DialogParamCH2DAlloy):
        if not DialogParamCH2DAlloy.objectName():
            DialogParamCH2DAlloy.setObjectName(u"DialogParamCH2DAlloy")
        DialogParamCH2DAlloy.resize(410, 320)
        self.layoutWidget = QWidget(DialogParamCH2DAlloy)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(21, 20, 368, 71))
        self.gridLayout_2 = QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.labelAlloy = QLabel(self.layoutWidget)
        self.labelAlloy.setObjectName(u"labelAlloy")
        self.labelAlloy.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.labelAlloy, 0, 0, 1, 1)

        self.comboBoxAlloy = QComboBox(self.layoutWidget)
        self.comboBoxAlloy.setObjectName(u"comboBoxAlloy")

        self.gridLayout_2.addWidget(self.comboBoxAlloy, 0, 1, 1, 1)

        self.pushButtonViewPhaseDiagram = QPushButton(self.layoutWidget)
        self.pushButtonViewPhaseDiagram.setObjectName(u"pushButtonViewPhaseDiagram")

        self.gridLayout_2.addWidget(self.pushButtonViewPhaseDiagram, 0, 2, 1, 1)

        self.labelTemperature = QLabel(self.layoutWidget)
        self.labelTemperature.setObjectName(u"labelTemperature")
        self.labelTemperature.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.labelTemperature, 1, 0, 1, 1)

        self.comboBoxTemperature = QComboBox(self.layoutWidget)
        self.comboBoxTemperature.setObjectName(u"comboBoxTemperature")

        self.gridLayout_2.addWidget(self.comboBoxTemperature, 1, 1, 1, 1)

        self.pushButtonViewParameters = QPushButton(self.layoutWidget)
        self.pushButtonViewParameters.setObjectName(u"pushButtonViewParameters")

        self.gridLayout_2.addWidget(self.pushButtonViewParameters, 1, 2, 1, 1)

        self.buttonBoxPramCH2DAlloy = QPushButton(DialogParamCH2DAlloy)
        self.buttonBoxPramCH2DAlloy.setObjectName(u"buttonBoxPramCH2DAlloy")
        self.buttonBoxPramCH2DAlloy.setGeometry(QRect(310, 260, 81, 31))
        self.widget = QWidget(DialogParamCH2DAlloy)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 110, 371, 121))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelFluctuation = QLabel(self.widget)
        self.labelFluctuation.setObjectName(u"labelFluctuation")
        self.labelFluctuation.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelFluctuation, 0, 0, 1, 1)

        self.lineEditFluctuation = QLineEdit(self.widget)
        self.lineEditFluctuation.setObjectName(u"lineEditFluctuation")

        self.gridLayout.addWidget(self.lineEditFluctuation, 0, 1, 2, 1)

        self.labelLx = QLabel(self.widget)
        self.labelLx.setObjectName(u"labelLx")
        self.labelLx.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelLx, 0, 2, 2, 1)

        self.lineEditLx = QLineEdit(self.widget)
        self.lineEditLx.setObjectName(u"lineEditLx")

        self.gridLayout.addWidget(self.lineEditLx, 0, 3, 2, 1)

        self.labelCAvg = QLabel(self.widget)
        self.labelCAvg.setObjectName(u"labelCAvg")
        self.labelCAvg.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelCAvg, 1, 0, 2, 1)

        self.lineEditCAvg = QLineEdit(self.widget)
        self.lineEditCAvg.setObjectName(u"lineEditCAvg")

        self.gridLayout.addWidget(self.lineEditCAvg, 2, 1, 1, 1)

        self.labelLy = QLabel(self.widget)
        self.labelLy.setObjectName(u"labelLy")
        self.labelLy.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelLy, 2, 2, 1, 1)

        self.lineEditLy = QLineEdit(self.widget)
        self.lineEditLy.setObjectName(u"lineEditLy")

        self.gridLayout.addWidget(self.lineEditLy, 2, 3, 1, 1)

        self.labelDelT = QLabel(self.widget)
        self.labelDelT.setObjectName(u"labelDelT")
        self.labelDelT.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelDelT, 3, 0, 1, 1)

        self.lineEditDelT = QLineEdit(self.widget)
        self.lineEditDelT.setObjectName(u"lineEditDelT")

        self.gridLayout.addWidget(self.lineEditDelT, 3, 1, 1, 1)

        self.labelDelX = QLabel(self.widget)
        self.labelDelX.setObjectName(u"labelDelX")
        self.labelDelX.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelDelX, 3, 2, 1, 1)

        self.lineEditDelX = QLineEdit(self.widget)
        self.lineEditDelX.setObjectName(u"lineEditDelX")

        self.gridLayout.addWidget(self.lineEditDelX, 3, 3, 1, 1)

        self.labelDelY = QLabel(self.widget)
        self.labelDelY.setObjectName(u"labelDelY")
        self.labelDelY.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelDelY, 4, 2, 1, 1)

        self.lineEditDelY = QLineEdit(self.widget)
        self.lineEditDelY.setObjectName(u"lineEditDelY")

        self.gridLayout.addWidget(self.lineEditDelY, 4, 3, 1, 1)


        self.retranslateUi(DialogParamCH2DAlloy)

        QMetaObject.connectSlotsByName(DialogParamCH2DAlloy)
    # setupUi

    def retranslateUi(self, DialogParamCH2DAlloy):
        DialogParamCH2DAlloy.setWindowTitle(QCoreApplication.translate("DialogParamCH2DAlloy", u"Edit Parameters", None))
        self.labelAlloy.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"Alloy", None))
        self.pushButtonViewPhaseDiagram.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"View Phase Diagram", None))
        self.labelTemperature.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"Temperature(\u00b0C)", None))
        self.pushButtonViewParameters.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"View Parameters", None))
        self.buttonBoxPramCH2DAlloy.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"Ok", None))
        self.labelFluctuation.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"fluctuation", None))
        self.labelLx.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"lx", None))
        self.labelCAvg.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"Average\n"
"composition", None))
        self.labelLy.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"ly", None))
        self.labelDelT.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"delta t", None))
        self.labelDelX.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"delta x", None))
        self.labelDelY.setText(QCoreApplication.translate("DialogParamCH2DAlloy", u"delta y", None))
    # retranslateUi

