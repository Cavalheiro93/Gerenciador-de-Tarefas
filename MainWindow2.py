# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QRadioButton, QSizePolicy, QTableView,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(690, 644)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 0, 671, 51))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 9, 601, 31))
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(10, 60, 671, 281))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.TableView_Activity = QTableView(self.frame_2)
        self.TableView_Activity.setObjectName(u"TableView_Activity")
        self.TableView_Activity.setGeometry(QRect(10, 80, 651, 192))
        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 20, 361, 56))
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Button_NewActivity = QPushButton(self.groupBox)
        self.Button_NewActivity.setObjectName(u"Button_NewActivity")

        self.horizontalLayout.addWidget(self.Button_NewActivity)

        self.Button_EditActivity = QPushButton(self.groupBox)
        self.Button_EditActivity.setObjectName(u"Button_EditActivity")

        self.horizontalLayout.addWidget(self.Button_EditActivity)

        self.Button_DeleteActivity = QPushButton(self.groupBox)
        self.Button_DeleteActivity.setObjectName(u"Button_DeleteActivity")

        self.horizontalLayout.addWidget(self.Button_DeleteActivity)

        self.Button_ShowAll = QPushButton(self.groupBox)
        self.Button_ShowAll.setObjectName(u"Button_ShowAll")

        self.horizontalLayout.addWidget(self.Button_ShowAll)

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(10, 350, 671, 291))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.TableView_Tasks = QTableView(self.frame_3)
        self.TableView_Tasks.setObjectName(u"TableView_Tasks")
        self.TableView_Tasks.setGeometry(QRect(10, 61, 651, 221))
        self.groupBox_2 = QGroupBox(self.frame_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 0, 191, 56))
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Button_UpdateTask = QPushButton(self.groupBox_2)
        self.Button_UpdateTask.setObjectName(u"Button_UpdateTask")

        self.horizontalLayout_2.addWidget(self.Button_UpdateTask)

        self.Button_RemoveTask = QPushButton(self.groupBox_2)
        self.Button_RemoveTask.setObjectName(u"Button_RemoveTask")

        self.horizontalLayout_2.addWidget(self.Button_RemoveTask)

        self.groupBox_3 = QGroupBox(self.frame_3)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(210, 0, 451, 56))
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.RadioButton_AllTasks = QRadioButton(self.groupBox_3)
        self.RadioButton_AllTasks.setObjectName(u"RadioButton_AllTasks")

        self.horizontalLayout_3.addWidget(self.RadioButton_AllTasks)

        self.RadioButton_Finished = QRadioButton(self.groupBox_3)
        self.RadioButton_Finished.setObjectName(u"RadioButton_Finished")

        self.horizontalLayout_3.addWidget(self.RadioButton_Finished)

        self.RadioButton_OnGoing = QRadioButton(self.groupBox_3)
        self.RadioButton_OnGoing.setObjectName(u"RadioButton_OnGoing")

        self.horizontalLayout_3.addWidget(self.RadioButton_OnGoing)

        self.RadioButton_NotStarted = QRadioButton(self.groupBox_3)
        self.RadioButton_NotStarted.setObjectName(u"RadioButton_NotStarted")

        self.horizontalLayout_3.addWidget(self.RadioButton_NotStarted)

        self.LineEdit_FilterTask = QLineEdit(self.groupBox_3)
        self.LineEdit_FilterTask.setObjectName(u"LineEdit_FilterTask")

        self.horizontalLayout_3.addWidget(self.LineEdit_FilterTask)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.Button_NewActivity, self.Button_EditActivity)
        QWidget.setTabOrder(self.Button_EditActivity, self.Button_DeleteActivity)
        QWidget.setTabOrder(self.Button_DeleteActivity, self.Button_ShowAll)
        QWidget.setTabOrder(self.Button_ShowAll, self.Button_UpdateTask)
        QWidget.setTabOrder(self.Button_UpdateTask, self.Button_RemoveTask)
        QWidget.setTabOrder(self.Button_RemoveTask, self.RadioButton_AllTasks)
        QWidget.setTabOrder(self.RadioButton_AllTasks, self.RadioButton_Finished)
        QWidget.setTabOrder(self.RadioButton_Finished, self.RadioButton_OnGoing)
        QWidget.setTabOrder(self.RadioButton_OnGoing, self.RadioButton_NotStarted)
        QWidget.setTabOrder(self.RadioButton_NotStarted, self.LineEdit_FilterTask)
        QWidget.setTabOrder(self.LineEdit_FilterTask, self.TableView_Activity)
        QWidget.setTabOrder(self.TableView_Activity, self.TableView_Tasks)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">Task Management</span></p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Activities", None))
        self.Button_NewActivity.setText(QCoreApplication.translate("MainWindow", u"New Activity", None))
        self.Button_EditActivity.setText(QCoreApplication.translate("MainWindow", u"Edit Activity", None))
        self.Button_DeleteActivity.setText(QCoreApplication.translate("MainWindow", u"Delete Activity", None))
        self.Button_ShowAll.setText(QCoreApplication.translate("MainWindow", u"Show All", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Tasks", None))
        self.Button_UpdateTask.setText(QCoreApplication.translate("MainWindow", u"Update Task", None))
        self.Button_RemoveTask.setText(QCoreApplication.translate("MainWindow", u"Remove Task", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Filter the Task", None))
        self.RadioButton_AllTasks.setText(QCoreApplication.translate("MainWindow", u"All Tasks", None))
        self.RadioButton_Finished.setText(QCoreApplication.translate("MainWindow", u"Finished", None))
        self.RadioButton_OnGoing.setText(QCoreApplication.translate("MainWindow", u"On Going", None))
        self.RadioButton_NotStarted.setText(QCoreApplication.translate("MainWindow", u"Not Started", None))
        self.LineEdit_FilterTask.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Filter by part of text...", None))
    # retranslateUi

