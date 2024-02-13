# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ActivityWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Dialog_Activity(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(243, 349)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 10, 221, 41))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 10, 211, 21))
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(10, 60, 221, 231))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.LineEdit_ID = QLineEdit(self.frame_2)
        self.LineEdit_ID.setObjectName(u"LineEdit_ID")
        self.LineEdit_ID.setGeometry(QRect(10, 24, 41, 20))
        self.LineEdit_ActivityName = QLineEdit(self.frame_2)
        self.LineEdit_ActivityName.setObjectName(u"LineEdit_ActivityName")
        self.LineEdit_ActivityName.setGeometry(QRect(10, 104, 201, 20))
        self.LineEdit_Responsible = QLineEdit(self.frame_2)
        self.LineEdit_Responsible.setObjectName(u"LineEdit_Responsible")
        self.LineEdit_Responsible.setGeometry(QRect(10, 144, 201, 20))
        self.ComboBox_ImportanceLevel = QComboBox(self.frame_2)
        self.ComboBox_ImportanceLevel.setObjectName(u"ComboBox_ImportanceLevel")
        self.ComboBox_ImportanceLevel.setGeometry(QRect(10, 184, 201, 20))
        self.ComboBox_ImportanceLevel.setEditable(False)
        self.LineEdit_CreatedData = QLineEdit(self.frame_2)
        self.LineEdit_CreatedData.setObjectName(u"LineEdit_CreatedData")
        self.LineEdit_CreatedData.setGeometry(QRect(10, 64, 81, 20))
        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(10, 300, 221, 43))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Button_Create = QPushButton(self.frame_3)
        self.Button_Create.setObjectName(u"Button_Create")

        self.horizontalLayout.addWidget(self.Button_Create)

        self.Button_Clear = QPushButton(self.frame_3)
        self.Button_Clear.setObjectName(u"Button_Clear")

        self.horizontalLayout.addWidget(self.Button_Clear)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Create a New Activity</span></p></body></html>", None))
        self.LineEdit_ID.setPlaceholderText(QCoreApplication.translate("Dialog", u"ID...", None))
        self.LineEdit_ActivityName.setPlaceholderText(QCoreApplication.translate("Dialog", u"Activity Name...", None))
        self.LineEdit_Responsible.setPlaceholderText(QCoreApplication.translate("Dialog", u"Responsible", None))
        self.ComboBox_ImportanceLevel.setCurrentText("")
        self.LineEdit_CreatedData.setPlaceholderText(QCoreApplication.translate("Dialog", u"Created data...", None))
        self.Button_Create.setText(QCoreApplication.translate("Dialog", u"Create", None))
        self.Button_Clear.setText(QCoreApplication.translate("Dialog", u"Clear", None))
    # retranslateUi

