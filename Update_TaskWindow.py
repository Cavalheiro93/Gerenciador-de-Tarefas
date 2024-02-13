# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Update_TaskWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QWidget)

class Ui_Dialog_UpdateTask(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(239, 391)
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
        self.frame_2.setGeometry(QRect(10, 60, 221, 261))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.LineEdit_DataCreated = QLineEdit(self.frame_2)
        self.LineEdit_DataCreated.setObjectName(u"LineEdit_DataCreated")
        self.LineEdit_DataCreated.setGeometry(QRect(10, 110, 133, 20))
        self.LineEdit_TaskName = QLineEdit(self.frame_2)
        self.LineEdit_TaskName.setObjectName(u"LineEdit_TaskName")
        self.LineEdit_TaskName.setGeometry(QRect(10, 144, 201, 20))
        self.RadioButton_NotStarted = QRadioButton(self.frame_2)
        self.RadioButton_NotStarted.setObjectName(u"RadioButton_NotStarted")
        self.RadioButton_NotStarted.setGeometry(QRect(10, 180, 82, 17))
        self.RadioButton_NotStarted.setChecked(True)
        self.RadioButton_OnGoing = QRadioButton(self.frame_2)
        self.RadioButton_OnGoing.setObjectName(u"RadioButton_OnGoing")
        self.RadioButton_OnGoing.setGeometry(QRect(10, 210, 82, 17))
        self.RadioButton_Finished = QRadioButton(self.frame_2)
        self.RadioButton_Finished.setObjectName(u"RadioButton_Finished")
        self.RadioButton_Finished.setGeometry(QRect(10, 240, 82, 17))
        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(0, 0, 211, 91))
        self.LineEdit_ID = QLineEdit(self.groupBox)
        self.LineEdit_ID.setObjectName(u"LineEdit_ID")
        self.LineEdit_ID.setGeometry(QRect(10, 20, 41, 20))
        self.LineEdit_ActivityName = QLineEdit(self.groupBox)
        self.LineEdit_ActivityName.setObjectName(u"LineEdit_ActivityName")
        self.LineEdit_ActivityName.setGeometry(QRect(10, 60, 133, 20))
        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(10, 330, 221, 43))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Button_Update = QPushButton(self.frame_3)
        self.Button_Update.setObjectName(u"Button_Create")

        self.horizontalLayout.addWidget(self.Button_Update)

        self.Button_Clear = QPushButton(self.frame_3)
        self.Button_Clear.setObjectName(u"Button_Clear")

        self.horizontalLayout.addWidget(self.Button_Clear)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Update the Task</span></p></body></html>", None))
        self.LineEdit_DataCreated.setPlaceholderText(QCoreApplication.translate("Dialog", u"Created data...", None))
        self.LineEdit_TaskName.setPlaceholderText(QCoreApplication.translate("Dialog", u"Task Name", None))
        self.RadioButton_NotStarted.setText(QCoreApplication.translate("Dialog", u"Not Started", None))
        self.RadioButton_OnGoing.setText(QCoreApplication.translate("Dialog", u"On Going", None))
        self.RadioButton_Finished.setText(QCoreApplication.translate("Dialog", u"Finished", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Activity Information", None))
        self.LineEdit_ID.setPlaceholderText(QCoreApplication.translate("Dialog", u"ID...", None))
        self.LineEdit_ActivityName.setPlaceholderText(QCoreApplication.translate("Dialog", u"Name of the Activity...", None))
        self.Button_Update.setText(QCoreApplication.translate("Dialog", u"Update", None))
        self.Button_Clear.setText(QCoreApplication.translate("Dialog", u"Clear", None))
    # retranslateUi

