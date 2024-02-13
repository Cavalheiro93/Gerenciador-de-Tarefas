import sys
import os
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel, QSqlQuery
from MainWindow import Ui_MainWindow
from TaskWindow import Ui_Dialog_Task
from ActivityWindow import Ui_Dialog_Activity

basedir = os.path.dirname(__file__)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.connect_db()
        self.setup_ui()

    def connect_db(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(os.path.join(basedir, 'Task_Management.db'))
        if not db.open():
            print('Não foi possível abrir o banco de dados')
            return False
        else:
            print('Banco de dados aberto com sucesso')
            return True

    def setup_ui(self):
        self.setup_activity_table()
        self.setup_task_table()
        self.setup_connections()

    def setup_activity_table(self):
        self.activity_model = QSqlTableModel()
        self.activity_model.setTable('Activity')
        self.activity_model.select()
        self.TableView_Activity.setModel(self.activity_model)

    def setup_task_table(self):
        query = QSqlQueryModel()
        query.setQuery("""
            SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,
            Activity.Activity_Name
            FROM Tasks
            INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
        """)
        self.TableView_Tasks.setModel(query)

    def setup_connections(self):
        self.Button_NewActivity.clicked.connect(self.open_activity_window)
        self.TableView_Activity.doubleClicked.connect(self.open_task_window)
        self.Button_ShowAll.clicked.connect(self.setup_task_table)
        self.TableView_Activity.selectionModel().currentChanged.connect(self.filter_tasks_by_activity)

    def open_activity_window(self):
        self.activity_window = ActivityWindow(self.activity_model, self)
        self.activity_window.show()

    def open_task_window(self):
        self.task_window = TaskWindow(self)
        self.task_window.show()

    def filter_tasks_by_activity(self):
        index = self.TableView_Activity.currentIndex()
        if not index.isValid():
            return

        ID_Activity = index.sibling(index.row(), 0).data()
        query = QSqlQuery()
        query.prepare("""
            SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,
            Activity.Activity_Name
            FROM Tasks
            INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
            WHERE Activity.ID_Activity = :ID_Activity
        """)
        query.bindValue(':ID_Activity', ID_Activity)
        if query.exec():
            query_model = QSqlQueryModel()
            query_model.setQuery(query)
            self.TableView_Tasks.setModel(query_model)
        else:
            print('Não foi possível filtrar as tarefas')


class ActivityWindow(QDialog, Ui_Dialog_Activity):
    def __init__(self, activity_model, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.activity_model = activity_model
        self.show()
        self.setup_ui()

    def setup_ui(self):
        self.setup_importance_levels()
        self.load_created_date()
        self.setup_buttons_and_connections()

    def setup_importance_levels(self):
        importance_levels = ['Baixa', 'Média', 'Alta']
        self.ComboBox_ImportanceLevel.addItems(importance_levels)

    def load_created_date(self):
        today = datetime.today()
        self.LineEdit_CreatedData.setText(today.strftime('%d/%m/%Y'))
        self.LineEdit_CreatedData.setReadOnly(True)

    def setup_buttons_and_connections(self):
        self.LineEdit_ID.setText(str(self.count_activity()))
        self.LineEdit_ID.setReadOnly(True)
        self.Button_Create.clicked.connect(self.create_activity)

    def count_activity(self):
        query = QSqlQuery()
        query.exec('SELECT COUNT(*) FROM Activity')
        query.next()
        return query.value(0) + 1

    def create_activity(self):
        initial_progress = '0%'
        today = datetime.today()

        query = QSqlQuery()
        query.prepare("""
            INSERT INTO Activity (ID_Activity, Activity_Name, Responsible, Importance_Level, Progress, Created_Date)
            VALUES (:ID_Activity, :Activity_Name, :Responsible, :Importance_Level, :Progress, :Created_Date)
        """)
        query.bindValue(':ID_Activity', self.LineEdit_ID.text())
        query.bindValue(':Activity_Name', self.LineEdit_ActivityName.text())
        query.bindValue(':Responsible', self.LineEdit_Responsible.text())
        query.bindValue(':Importance_Level', self.ComboBox_ImportanceLevel.currentText())
        query.bindValue(':Progress', initial_progress)
        query.bindValue(':Created_Date', today.strftime('%d/%m/%Y'))

        if query.exec():
            self.activity_model.select()
            self.parent().filter_tasks_by_activity()
            self.accept()

class TaskWindow(QMainWindow, Ui_Dialog_Task):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

app = QApplication(sys.argv)
w = MainWindow()
app.exec()
