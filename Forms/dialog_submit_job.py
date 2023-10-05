# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_submit_job.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogSubmitJob(object):
    def setupUi(self, DialogSubmitJob):
        if not DialogSubmitJob.objectName():
            DialogSubmitJob.setObjectName(u"DialogSubmitJob")
        DialogSubmitJob.resize(250, 190)
        self.pushButtonSubmit = QPushButton(DialogSubmitJob)
        self.pushButtonSubmit.setObjectName(u"pushButtonSubmit")
        self.pushButtonSubmit.setGeometry(QRect(130, 130, 101, 31))
        self.layoutWidget = QWidget(DialogSubmitJob)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(11, 21, 221, 91))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelScheduler = QLabel(self.layoutWidget)
        self.labelScheduler.setObjectName(u"labelScheduler")

        self.gridLayout.addWidget(self.labelScheduler, 0, 0, 1, 1)

        self.comboBoxScheduler = QComboBox(self.layoutWidget)
        self.comboBoxScheduler.addItem("")
        self.comboBoxScheduler.addItem("")
        self.comboBoxScheduler.setObjectName(u"comboBoxScheduler")

        self.gridLayout.addWidget(self.comboBoxScheduler, 0, 1, 1, 1)

        self.labelCores = QLabel(self.layoutWidget)
        self.labelCores.setObjectName(u"labelCores")

        self.gridLayout.addWidget(self.labelCores, 1, 0, 1, 1)

        self.lineEditCores = QLineEdit(self.layoutWidget)
        self.lineEditCores.setObjectName(u"lineEditCores")

        self.gridLayout.addWidget(self.lineEditCores, 1, 1, 1, 1)

        self.labelTime = QLabel(self.layoutWidget)
        self.labelTime.setObjectName(u"labelTime")

        self.gridLayout.addWidget(self.labelTime, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditTimeHour = QLineEdit(self.layoutWidget)
        self.lineEditTimeHour.setObjectName(u"lineEditTimeHour")

        self.horizontalLayout.addWidget(self.lineEditTimeHour)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditTimeMinute = QLineEdit(self.layoutWidget)
        self.lineEditTimeMinute.setObjectName(u"lineEditTimeMinute")

        self.horizontalLayout.addWidget(self.lineEditTimeMinute)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.lineEditTimeSecond = QLineEdit(self.layoutWidget)
        self.lineEditTimeSecond.setObjectName(u"lineEditTimeSecond")

        self.horizontalLayout.addWidget(self.lineEditTimeSecond)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.labelMsg = QLabel(DialogSubmitJob)
        self.labelMsg.setObjectName(u"labelMsg")
        self.labelMsg.setGeometry(QRect(10, 160, 221, 20))

        self.retranslateUi(DialogSubmitJob)

        QMetaObject.connectSlotsByName(DialogSubmitJob)
    # setupUi

    def retranslateUi(self, DialogSubmitJob):
        DialogSubmitJob.setWindowTitle(QCoreApplication.translate("DialogSubmitJob", u"Dialog", None))
        self.pushButtonSubmit.setText(QCoreApplication.translate("DialogSubmitJob", u"Submit Job", None))
        self.labelScheduler.setText(QCoreApplication.translate("DialogSubmitJob", u"Scheduler", None))
        self.comboBoxScheduler.setItemText(0, QCoreApplication.translate("DialogSubmitJob", u"SLURM", None))
        self.comboBoxScheduler.setItemText(1, QCoreApplication.translate("DialogSubmitJob", u"PBS", None))

        self.labelCores.setText(QCoreApplication.translate("DialogSubmitJob", u"Cores", None))
        self.labelTime.setText(QCoreApplication.translate("DialogSubmitJob", u"Time", None))
        self.lineEditTimeHour.setText(QCoreApplication.translate("DialogSubmitJob", u"00", None))
        self.label.setText(QCoreApplication.translate("DialogSubmitJob", u":", None))
        self.lineEditTimeMinute.setText(QCoreApplication.translate("DialogSubmitJob", u"00", None))
        self.label_2.setText(QCoreApplication.translate("DialogSubmitJob", u":", None))
        self.lineEditTimeSecond.setText(QCoreApplication.translate("DialogSubmitJob", u"00", None))
        self.labelMsg.setText("")
    # retranslateUi

