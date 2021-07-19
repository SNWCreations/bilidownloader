# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uiAYSZMM.ui'
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
        MainWindow.resize(451, 161)
        icon = QIcon()
        icon.addFile(u":/icon/icon.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.download = QPushButton(self.centralwidget)
        self.download.setObjectName(u"download")
        self.download.setEnabled(True)
        self.download.setGeometry(QRect(330, 70, 75, 23))
        self.download.setCheckable(False)
        self.download.setAutoDefault(False)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(50, 40, 351, 20))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(90, 20, 281, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(53, 73, 61, 16))
        self.quality = QComboBox(self.centralwidget)
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.setObjectName(u"quality")
        self.quality.setGeometry(QRect(120, 70, 69, 22))
        self.saveat = QPushButton(self.centralwidget)
        self.saveat.setObjectName(u"saveat")
        self.saveat.setGeometry(QRect(240, 70, 75, 23))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 140, 211, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(350, 140, 91, 16))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(180, 100, 16, 16))
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(250, 100, 16, 16))
        self.videoname = QLabel(self.centralwidget)
        self.videoname.setObjectName(u"videoname")
        self.videoname.setGeometry(QRect(10, 120, 431, 20))
        self.videoname.setAlignment(Qt.AlignCenter)
        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(200, 100, 42, 16))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(999999999)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.download.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Bilibili Downloader", None))
        self.download.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d!", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5728\u4e0b\u9762\u7684\u6846\u91cc\u8f93\u5165 BV \u53f7\u6216\u8005\u5b8c\u6574\u7684B\u7ad9\u89c6\u9891\u94fe\u63a5:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6e05\u6670\u5ea6", None))
        self.quality.setItemText(0, QCoreApplication.translate("MainWindow", u"1080P", None))
        self.quality.setItemText(1, QCoreApplication.translate("MainWindow", u"720P", None))
        self.quality.setItemText(2, QCoreApplication.translate("MainWindow", u"480P", None))
        self.quality.setItemText(3, QCoreApplication.translate("MainWindow", u"360P", None))

        self.saveat.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u5230...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u793a: \u4e0b\u8f7d\u7684\u89c6\u9891\u9ed8\u8ba4\u4fdd\u5b58\u5230\u5f53\u524d\u76ee\u5f55", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"by SNWCreations", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u7b2c", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u9875", None))
        self.videoname.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u540d\u79f0: \u65e0", None))
    # retranslateUi

