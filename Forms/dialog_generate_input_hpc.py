# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_generate_input_hpc.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogGenerateHPCInput(object):
    def setupUi(self, DialogGenerateHPCInput):
        if not DialogGenerateHPCInput.objectName():
            DialogGenerateHPCInput.setObjectName(u"DialogGenerateHPCInput")
        DialogGenerateHPCInput.resize(370, 230)
        self.pushButtonGenerateInput = QPushButton(DialogGenerateHPCInput)
        self.pushButtonGenerateInput.setObjectName(u"pushButtonGenerateInput")
        self.pushButtonGenerateInput.setGeometry(QRect(240, 190, 111, 31))
        self.labelMsg = QLabel(DialogGenerateHPCInput)
        self.labelMsg.setObjectName(u"labelMsg")
        self.labelMsg.setGeometry(QRect(20, 200, 221, 20))
        self.widget = QWidget(DialogGenerateHPCInput)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 21, 341, 151))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.comboBoxScheduler = QComboBox(self.widget)
        self.comboBoxScheduler.addItem("")
        self.comboBoxScheduler.addItem("")
        self.comboBoxScheduler.setObjectName(u"comboBoxScheduler")

        self.gridLayout.addWidget(self.comboBoxScheduler, 0, 1, 1, 2)

        self.labelTime = QLabel(self.widget)
        self.labelTime.setObjectName(u"labelTime")

        self.gridLayout.addWidget(self.labelTime, 2, 0, 1, 1)

        self.lineEditCores = QLineEdit(self.widget)
        self.lineEditCores.setObjectName(u"lineEditCores")

        self.gridLayout.addWidget(self.lineEditCores, 1, 1, 1, 2)

        self.pushButtonOutDir = QPushButton(self.widget)
        self.pushButtonOutDir.setObjectName(u"pushButtonOutDir")

        self.gridLayout.addWidget(self.pushButtonOutDir, 3, 1, 1, 1)

        self.labelOutDir = QLabel(self.widget)
        self.labelOutDir.setObjectName(u"labelOutDir")

        self.gridLayout.addWidget(self.labelOutDir, 3, 0, 1, 1)

        self.labelScheduler = QLabel(self.widget)
        self.labelScheduler.setObjectName(u"labelScheduler")

        self.gridLayout.addWidget(self.labelScheduler, 0, 0, 1, 1)

        self.lineEditOutDir = QLineEdit(self.widget)
        self.lineEditOutDir.setObjectName(u"lineEditOutDir")

        self.gridLayout.addWidget(self.lineEditOutDir, 3, 2, 1, 1)

        self.labelCores = QLabel(self.widget)
        self.labelCores.setObjectName(u"labelCores")

        self.gridLayout.addWidget(self.labelCores, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditTimeHour = QLineEdit(self.widget)
        self.lineEditTimeHour.setObjectName(u"lineEditTimeHour")

        self.horizontalLayout.addWidget(self.lineEditTimeHour)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditTimeMinute = QLineEdit(self.widget)
        self.lineEditTimeMinute.setObjectName(u"lineEditTimeMinute")

        self.horizontalLayout.addWidget(self.lineEditTimeMinute)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.lineEditTimeSecond = QLineEdit(self.widget)
        self.lineEditTimeSecond.setObjectName(u"lineEditTimeSecond")

        self.horizontalLayout.addWidget(self.lineEditTimeSecond)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 2)


        self.retranslateUi(DialogGenerateHPCInput)

        QMetaObject.connectSlotsByName(DialogGenerateHPCInput)
    # setupUi

    def retranslateUi(self, DialogGenerateHPCInput):
        DialogGenerateHPCInput.setWindowTitle(QCoreApplication.translate("DialogGenerateHPCInput", u"Dialog", None))
        self.pushButtonGenerateInput.setText(QCoreApplication.translate("DialogGenerateHPCInput", u"Generate Input", None))
        self.labelMsg.setText("")
        self.comboBoxScheduler.setItemText(0, QCoreApplication.translate("DialogGenerateHPCInput", u"SLURM", None))
        self.comboBoxScheduler.setItemText(1, QCoreApplication.translate("DialogGenerateHPCInput", u"PBS", None))

        self.labelTime.setText(QCoreApplication.translate("DialogGenerateHPCInput", u"Time", None))
        self.pushButtonOutDir.setText("")
        self.labelOutDir.setText(QCoreApplication.translate("DialogGenerateHPCInput", u"Out Dir", None))
        self.labelScheduler.setText(QCoreApplication.translate("DialogGenerateHPCInput", u"Scheduler", None))
        self.labelCores.setText(QCoreApplication.translate("DialogGenerateHPCInput", u"Cores", None))
        self.lineEditTimeHour.setText(QCoreApplication.translate("DialogGenerateHPCInput", u"00", None))
        self.label.setText(QCoreApplication.translate("DialogGenerateHPCInput", u":", None))
        self.lineEditTimeMinute.setText(QCoreApplication.translate("DialogGenerateHPCInput", u"00", None))
        self.label_2.setText(QCoreApplication.translate("DialogGenerateHPCInput", u":", None))
        self.lineEditTimeSecond.setText(QCoreApplication.translate("DialogGenerateHPCInput", u"00", None))
    # retranslateUi

