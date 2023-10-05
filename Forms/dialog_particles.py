# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_particles.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogParticles(object):
    def setupUi(self, DialogParticles):
        if not DialogParticles.objectName():
            DialogParticles.setObjectName(u"DialogParticles")
        DialogParticles.resize(277, 337)
        self.groupBox = QGroupBox(DialogParticles)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 20, 251, 181))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelParticlesTop = QLabel(self.groupBox)
        self.labelParticlesTop.setObjectName(u"labelParticlesTop")

        self.verticalLayout.addWidget(self.labelParticlesTop)

        self.scrollArea = QScrollArea(self.groupBox)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 100))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 225, 112))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelParticles = QLabel(self.scrollAreaWidgetContents)
        self.labelParticles.setObjectName(u"labelParticles")
        self.labelParticles.setMinimumSize(QSize(0, 0))

        self.verticalLayout_2.addWidget(self.labelParticles)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.groupBox_2 = QGroupBox(DialogParticles)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 220, 251, 91))
        self.labelAvgParticles = QLabel(self.groupBox_2)
        self.labelAvgParticles.setObjectName(u"labelAvgParticles")
        self.labelAvgParticles.setGeometry(QRect(10, 30, 191, 51))

        self.retranslateUi(DialogParticles)

        QMetaObject.connectSlotsByName(DialogParticles)
    # setupUi

    def retranslateUi(self, DialogParticles):
        DialogParticles.setWindowTitle(QCoreApplication.translate("DialogParticles", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("DialogParticles", u"Particles", None))
        self.labelParticlesTop.setText("")
        self.labelParticles.setText(QCoreApplication.translate("DialogParticles", u"TextLabel ", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("DialogParticles", u"Average", None))
        self.labelAvgParticles.setText(QCoreApplication.translate("DialogParticles", u"TextLabel", None))
    # retranslateUi

