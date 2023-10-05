# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_convert_to_video.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_DialogConvertToVideo(object):
    def setupUi(self, DialogConvertToVideo):
        if not DialogConvertToVideo.objectName():
            DialogConvertToVideo.setObjectName(u"DialogConvertToVideo")
        DialogConvertToVideo.resize(460, 140)
        self.labelConvertingStatus = QLabel(DialogConvertToVideo)
        self.labelConvertingStatus.setObjectName(u"labelConvertingStatus")
        self.labelConvertingStatus.setGeometry(QRect(20, 100, 111, 21))
        self.layoutWidget = QWidget(DialogConvertToVideo)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(240, 20, 201, 27))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.labelVideoFormat = QLabel(self.layoutWidget)
        self.labelVideoFormat.setObjectName(u"labelVideoFormat")

        self.horizontalLayout_3.addWidget(self.labelVideoFormat)

        self.comboBoxVideoFormat = QComboBox(self.layoutWidget)
        self.comboBoxVideoFormat.addItem("")
        self.comboBoxVideoFormat.addItem("")
        self.comboBoxVideoFormat.addItem("")
        self.comboBoxVideoFormat.setObjectName(u"comboBoxVideoFormat")

        self.horizontalLayout_3.addWidget(self.comboBoxVideoFormat)

        self.layoutWidget_1 = QWidget(DialogConvertToVideo)
        self.layoutWidget_1.setObjectName(u"layoutWidget_1")
        self.layoutWidget_1.setGeometry(QRect(20, 20, 191, 27))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget_1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.labelTimeInterval = QLabel(self.layoutWidget_1)
        self.labelTimeInterval.setObjectName(u"labelTimeInterval")

        self.horizontalLayout_2.addWidget(self.labelTimeInterval)

        self.lineEditTimeInterval = QLineEdit(self.layoutWidget_1)
        self.lineEditTimeInterval.setObjectName(u"lineEditTimeInterval")

        self.horizontalLayout_2.addWidget(self.lineEditTimeInterval)

        self.pushButtonBrowse = QPushButton(DialogConvertToVideo)
        self.pushButtonBrowse.setObjectName(u"pushButtonBrowse")
        self.pushButtonBrowse.setGeometry(QRect(20, 60, 41, 31))
        self.lineEditFilePath = QLineEdit(DialogConvertToVideo)
        self.lineEditFilePath.setObjectName(u"lineEditFilePath")
        self.lineEditFilePath.setGeometry(QRect(60, 60, 281, 31))
        self.pushButtonExport = QPushButton(DialogConvertToVideo)
        self.pushButtonExport.setObjectName(u"pushButtonExport")
        self.pushButtonExport.setGeometry(QRect(350, 60, 91, 31))

        self.retranslateUi(DialogConvertToVideo)

        QMetaObject.connectSlotsByName(DialogConvertToVideo)
    # setupUi

    def retranslateUi(self, DialogConvertToVideo):
        DialogConvertToVideo.setWindowTitle(QCoreApplication.translate("DialogConvertToVideo", u"Export Animation", None))
        self.labelConvertingStatus.setText("")
        self.labelVideoFormat.setText(QCoreApplication.translate("DialogConvertToVideo", u"Video Format", None))
        self.comboBoxVideoFormat.setItemText(0, QCoreApplication.translate("DialogConvertToVideo", u"mp4", None))
        self.comboBoxVideoFormat.setItemText(1, QCoreApplication.translate("DialogConvertToVideo", u"mov", None))
        self.comboBoxVideoFormat.setItemText(2, QCoreApplication.translate("DialogConvertToVideo", u"avi", None))

        self.labelTimeInterval.setText(QCoreApplication.translate("DialogConvertToVideo", u"Time interval(ms)", None))
        self.pushButtonBrowse.setText("")
        self.pushButtonExport.setText(QCoreApplication.translate("DialogConvertToVideo", u"Export", None))
    # retranslateUi

