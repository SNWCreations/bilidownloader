# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

import icon_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(460, 150)
        icon = QIcon()
        icon.addFile(u":/icon/icon.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.download = QPushButton(self.centralwidget)
        self.download.setObjectName(u"download")
        self.download.setEnabled(True)
        self.download.setGeometry(QRect(340, 60, 71, 23))
        self.download.setCheckable(False)
        self.download.setAutoDefault(False)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(40, 30, 381, 20))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(105, 10, 271, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(40, 63, 61, 16))
        self.quality = QComboBox(self.centralwidget)
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.setObjectName(u"quality")
        self.quality.setGeometry(QRect(85, 60, 69, 22))
        self.saveAtButton = QPushButton(self.centralwidget)
        self.saveAtButton.setObjectName(u"saveAtButton")
        self.saveAtButton.setGeometry(QRect(260, 60, 75, 23))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 130, 331, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(360, 130, 91, 16))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(40, 90, 31, 16))
        self.videoName = QLabel(self.centralwidget)
        self.videoName.setObjectName(u"videoName")
        self.videoName.setGeometry(QRect(10, 110, 441, 20))
        self.videoName.setAlignment(Qt.AlignCenter)
        self.videoPage = QSpinBox(self.centralwidget)
        self.videoPage.setObjectName(u"videoPage")
        self.videoPage.setGeometry(QRect(70, 87, 42, 22))
        self.videoPage.setMinimum(1)
        self.videoPage.setMaximum(999999999)
        self.saveOriginalVideo = QCheckBox(self.centralwidget)
        self.saveOriginalVideo.setObjectName(u"saveOriginalVideo")
        self.saveOriginalVideo.setGeometry(QRect(320, 90, 91, 16))
        self.videoFormatType = QComboBox(self.centralwidget)
        self.videoFormatType.addItem("")
        self.videoFormatType.addItem("")
        self.videoFormatType.addItem("")
        self.videoFormatType.setObjectName(u"videoFormatType")
        self.videoFormatType.setGeometry(QRect(225, 87, 51, 22))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(145, 90, 81, 16))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.download.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Bilibili Downloader", None))
        self.download.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d!", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5728\u4e0b\u9762\u7684\u6846\u91cc\u8f93\u5165 BV \u53f7\u6216\u8005\u5b8c\u6574\u7684B\u7ad9\u89c6\u9891\u94fe\u63a5:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u6670\u5ea6:", None))
        self.quality.setItemText(0, QCoreApplication.translate("MainWindow", u"1080P", None))
        self.quality.setItemText(1, QCoreApplication.translate("MainWindow", u"720P", None))
        self.quality.setItemText(2, QCoreApplication.translate("MainWindow", u"480P", None))
        self.quality.setItemText(3, QCoreApplication.translate("MainWindow", u"360P", None))

        self.saveAtButton.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u5230...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u793a: \u4e0b\u8f7d\u7684\u89c6\u9891\u9ed8\u8ba4\u4fdd\u5b58\u5230\u5f53\u524d\u76ee\u5f55\u4e0b\u7684 \"Downloads\" \u76ee\u5f55", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"by SNWCreations", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u9875\u53f7:", None))
        self.videoName.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u5b8c BV \u53f7\u540e, \u5728\u8f93\u5165\u6846\u91cc\u6309\u4e0b\u56de\u8f66\u5373\u53ef\u5728\u8fd9\u91cc\u770b\u5230\u89c6\u9891\u540d\u79f0", None))
        self.saveOriginalVideo.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u7559\u539f\u59cb\u89c6\u9891", None))
        self.videoFormatType.setItemText(0, QCoreApplication.translate("MainWindow", u"MP4", None))
        self.videoFormatType.setItemText(1, QCoreApplication.translate("MainWindow", u"MP3", None))
        self.videoFormatType.setItemText(2, QCoreApplication.translate("MainWindow", u"FLV", None))

        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u683c\u5f0f:", None))
    # retranslateUi

