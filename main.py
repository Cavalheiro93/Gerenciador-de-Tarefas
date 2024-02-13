#Importando Bibliotecas do Python
import sys
import os
from datetime import datetime
#Importando as bibliotecas do PySide6
from PySide6.QtCore import Qt, QCoreApplication, QSortFilterProxyModel
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel, QSqlQuery
#Importando as janelas criadas no QtDesigner
from MainWindow2 import Ui_MainWindow   # A janela criada no QtDesigner
from TaskWindow import Ui_Dialog_Task  # A janela criada no QtDesigner
from ActivityWindow import Ui_Dialog_Activity  # A janela criada no QtDesigner
from Update_TaskWindow import Ui_Dialog_UpdateTask  # A janela criada no QtDesigner

# Define o diretório base do arquivo atual
basedir = os.path.dirname(__file__)

# Cria a classe da janela principal | Herda a classe QMainWindow e a classe Ui_MainWindow
class MainWindow(QMainWindow, Ui_MainWindow):   
    def __init__(self):
        super().__init__()
        self.setupUi(self)                      # Configura a janela principal
        self.show()                             # Mostra a janela principal
        self.connect_db()                       # Conecta ao banco de dados
        self.show_activities()                  # Mostra as atividades no TableView
        self.show_tasks()                       # Mostra as tarefas no TableView
        self.table_view_loaded = False          # Variavel para verificar se o TableView foi carregado

        self.Button_NewActivity.clicked.connect(self.open_activity_window)   # Abre a janela de atividades ao clicar no botão
        self.TableView_Activity.doubleClicked.connect(self.open_task_window)   # Abre a janela de atividades ao clicar no botão
        self.Button_UpdateTask.clicked.connect(self.open_update_task_window)   # Abre a janela de atividades ao clicar no botão
        self.Button_EditActivity.clicked.connect(self.open_update_activity_window)   # Abre a janela de atividades ao clicar no botão


        self.TableView_Activity.selectionModel().currentChanged.connect(self.filter_tasks_by_activity)    # Conecta o evento de seleção de item da TV_Atividades à função de filtro
        self.Button_ShowAll.clicked.connect(self.show_tasks)   # Mostra todas as tarefas ao clicar no botão

        self.TableView_Activity.setSortingEnabled(True)  # Habilita a ordenação na TV_Atividades
        self.TableView_Activity.horizontalHeader().sectionClicked.connect(self.sort_activity_column)  # Conecta o evento de clique no cabeçalho da TV_Atividades à função de ordenação
        self.TableView_Tasks.setSortingEnabled(True)  # Habilita a ordenação na TV_Atividades
        self.TableView_Tasks.horizontalHeader().sectionClicked.connect(self.sort_task_column)  

        self.RadioButton_AllTasks.toggled.connect(self.filter_tasks_by_radio_button)   # Conecta o evento de seleção do radio button à função de filtro
        self.RadioButton_NotStarted.toggled.connect(self.filter_tasks_by_radio_button)   # Conecta o evento de seleção do radio button à função de filtro
        self.RadioButton_OnGoing.toggled.connect(self.filter_tasks_by_radio_button)   # Conecta o evento de seleção do radio button à função de filtro
        self.RadioButton_Finished.toggled.connect(self.filter_tasks_by_radio_button)   # Conecta o evento de seleção do radio button à função de filtro

        # Conecta o evento de alteração de texto do LineEdit à função de filtro
        self.LineEdit_FilterTask.textChanged.connect(self.custom_filter)

    def connect_db(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(os.path.join(basedir, 'Task_Management.db'))
        if not db.open():
            print('Não foi possível abrir o banco de dados')
            return False
        else:
            print('Banco de dados aberto com sucesso')
            return True     

    def show_activities(self):
        self.activity_model = QSqlQueryModel()
        self.activity_model.setQuery('SELECT * FROM Activity')
        self.TableView_Activity.setModel(self.activity_model)
        return

    def show_tasks(self):
        self.task_model = QSqlQueryModel()                    # Cria uma variavel do tipo QSqlQueryModel, para exibir os dados no TableView
        # Abaixo está a query que será executada, queremos exibir todos os campos de task e o nome da atividade
        # 1. Selecionamos as Tasks que queremos exibir  | 2. Selecionamos o campo de atividade que queremos exibir
        # 3. Selecionamos a tabela de task              | 4. Aplicamos INNER JOIN nos campos ID_Activity de TASK e ID_Activity de ACTIVITY 
        self.task_model.setQuery("""
                SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                Activity.Activity_Name
                FROM Tasks
                INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                """)
        self.TableView_Tasks.setModel(self.task_model)        # Exibe os dados no TableView
        # Crie um proxy model para filtragem
        self.task_proxy_model = QSortFilterProxyModel()         # Cria uma variavel do tipo QSortFilterProxyModel, para filtrar os dados no TableView
        self.task_proxy_model.setSourceModel(self.task_model)   # Configura o modelo de origem do proxy model
        self.TableView_Tasks.setModel(self.task_proxy_model)    # Exibe os dados no TableView
        return

    def open_activity_window(self):
        self.activity_window = ActivityWindow(self)     # Cria a janela de atividades
        self.activity_window.show()                 # Executa a janela de atividades

    def open_task_window(self):
        self.task_window = TaskWindow(self)             # Cria a janela de atividades
        self.task_window.show()                     # Executa a janela de atividades        

    def open_update_activity_window(self):
        self.task_window = UpdateActivityWindow(self)             # Cria a janela de atividades
        self.task_window.show()                     # Executa a janela de atividades      

    def open_update_task_window(self):
        self.task_window = UpdateTaskWindow(self)             # Cria a janela de atividades
        self.task_window.show()                     # Executa a janela de atividades          

    def date_today(self):                                            # Função para carregar a data de criação da atividade
        self.today = datetime.today() 
        return self.today.strftime('%d/%m/%Y') 

    def filter_tasks_by_activity(self):
        if not self.table_view_loaded:
            self.table_view_loaded = True
            return
        
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

    def update_activity_table(self):
        self.show_activities()
        self.filter_tasks_by_activity()

    def sort_activity_column(self, index):                  # Função para ordenar as colunas da TV_Atividadesn ao clicar no cabeçalho
        column_name = {                                     # Dicionario com os nomes das colunas
            0: 'ID_Activity',                               # Chave: Valor | 0: 'ID_Activity'
            1: 'Activity_Name',                             # Chave: Valor | 1: 'Activity_Name'
            2: 'Responsible',                               # Chave: Valor | 2: 'Responsible'
            3: 'Importance_Level',                          # Chave: Valor | 3: 'Importance_Level'
            4: 'Progress',                                  # Chave: Valor | 4: 'Progress'
            5: 'Created_Date'                               # Chave: Valor | 5: 'Created_Date'
        }
        column_name = column_name.get(index)                # Pega o nome da coluna de acordo com o índice
        if column_name is None:                             # Se o nome da coluna for None, não faz nada
            return
        
        if self.activity_model.query().lastQuery().endswith('DESC'):                                 # Se a última query terminar com DESC
            self.activity_model.setQuery(f'SELECT * FROM Activity ORDER BY {column_name} ASC')       # Ordena a coluna de forma crescente
        else:                                                                                        # Do contrario
            self.activity_model.setQuery(f'SELECT * FROM Activity ORDER BY {column_name} DESC')      # Ordena a coluna de forma decrescente

    def sort_task_column(self, index):                      
        column_name = {
            0: 'ID_Task',
            1: 'Task_Name',
            2: 'Status',
            3: 'Created_Date',
            4: 'Activity_Name'
        }

        column_name = column_name.get(index)
        if column_name is None:
            return

        if self.task_model.query().lastQuery().endswith('DESC'):
            self.task_model.setQuery(f"""
                SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                Activity.Activity_Name
                FROM Tasks
                INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                ORDER BY {column_name} ASC
                """)
        else:
            self.task_model.setQuery(f"""
                SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                Activity.Activity_Name
                FROM Tasks
                INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                ORDER BY {column_name} DESC
                """)
            
    def radio_button_toggled(self):                                          # Função para verificar qual radio button foi selecionado
        if self.RadioButton_NotStarted.isChecked():                          # Se o radio button Não Iniciado estiver selecionado
            return 'Not Started'                                             # A variavel Status recebe o valor Não Iniciado)
        elif self.RadioButton_OnGoing.isChecked():                           # Se o radio button Em Progresso estiver selecionado
            return 'On Going'                                                # A variavel Status recebe o valor Em Progresso
        elif self.RadioButton_Finished.isChecked():                          # Se o radio button Concluído estiver selecionado
            return 'Finished'                                                # A variavel Status recebe o valor Concluído
        else:
            return 'All Tasks'

    def filter_tasks_by_radio_button(self):
        radio_toggled = self.radio_button_toggled()
        if radio_toggled == 'All Tasks':
            self.task_model.setQuery("""SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
            Activity.Activity_Name
            FROM Tasks
            INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity""")
        else:
            self.task_model.setQuery(f"""
            SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
            Activity.Activity_Name
            FROM Tasks
            INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
            WHERE Tasks.Status = '{radio_toggled}'
            """)

    def filter_by_text(self, text):
        if text:
            filter_text = f"%{text}%"
            self.task_proxy_model.setFilterByColumn(-1, filter_text)  # Filtrar todas as colunas
        else:
            self.task_proxy_model.setFilterFixedString("")  # Remover o filtro para mostrar todas as tarefas

    def custom_filter(self, text):
        filter_text = text.lower()                                          # Converte o texto para minúsculo, para ignorar a diferença entre maiúsculas e minúsculas
        self.task_proxy_model.setFilterKeyColumn(-1)                        # Configura o filtro para todas as colunas
        self.task_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)  # Ignora a diferença entre maiúsculas e minúsculas
        self.task_proxy_model.setFilterWildcard(f"*{filter_text}*")         # Configura o filtro para usar caracteres curinga


    
# Cria a classe da janela de tarefas | Herda a classe QDialog e a classe Ui_Dialog_Task
class ActivityWindow(QDialog, Ui_Dialog_Activity):
    # O parent=None é para que a janela de atividades não seja fechada quando a janela principal for fechada
    def __init__(self, parent=None):                    
        super().__init__(parent)                        # Configura a janela de atividades
        self.setupUi(self)                              # Configura a janela de atividades
        self.show()                                     # Mostra a janela de atividades
        self.load_importance_levels()                   # Carrega os níveis de importância no ComboBox
        self.load_created_date()                        # Carrega a data de criação da atividade

        self.LineEdit_ID.setText(str(self.count_activity()))   # Pega o ID da atividade e exibe no LineEdit
        self.LineEdit_ID.setReadOnly(True)                     # Deixa o LineEdit apenas para leitura
        self.Button_Create.clicked.connect(self.create_activity)   # Cria a atividade ao clicar no botão

    def count_activity(self):                           # Função para contar quantas atividades existem no banco de dados
        query = QSqlQuery()                             # Cria uma variavel do tipo QSqlQuery, para executar a query
        query.exec('SELECT COUNT(*) FROM Activity')     # Executa a query | Conta quantas atividades existem no banco de dados
        query.next()                                    # Pega o resultado da query
        return query.value(0) +1                        # Retorna o resultado da query +1
    
    def load_importance_levels(self):                               # Função para carregar os níveis de importância no ComboBox
        importance_levels = ['Baixa', 'Média', 'Alta']              # Cria uma lista com os níveis de importância
        self.ComboBox_ImportanceLevel.addItems(importance_levels)   # Adiciona os níveis de importância no ComboBox

    def load_created_date(self):                                    # Função para carregar a data de criação da atividade
        self.LineEdit_CreatedData.setText(self.parent().date_today()) # Exibe a data atual no LineEdit
        self.LineEdit_CreatedData.setReadOnly(True)                 # Deixa o LineEdit apenas para leitura

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
            self.parent().activity_model.setQuery('SELECT * FROM Activity')  # Atualiza o modelo com uma nova query
            self.parent().show_tasks()
            self.accept()
    

class TaskWindow(QDialog, Ui_Dialog_Task):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self) 
        self.update_task_window()
        self.show()
        self.Button_Create.clicked.connect(self.create_task)

    def selected_activity_data(self):                                           # Função para pegar os dados da atividade selecionada
            index = self.parent().TableView_Activity.currentIndex()             # Criamos a variavel index para pegar o índice da TableView_Activity
            model = self.parent().TableView_Activity.model()                    # Criamos a variavel model para pegar o modelo da TableView_Activity
            self.Activity_Index = model.data(model.index(index.row(), 0))        # Pega o INDEX da atividade selecionada
            self.Activity_Name = model.data(model.index(index.row(), 1))        # Pega o NOME da atividade selecionada

    def count_tasks(self):                                                   # Função para contar quantas tarefas existem no banco de dados
        self.query = QSqlQuery()                                             # Cria uma variavel do tipo QSqlQuery, para executar a query
        self.query.exec('SELECT COUNT(*) FROM Tasks')                        # Executa a query | Conta quantas tarefas existem no banco de dados
        self.query.next()                                                    # Pega o resultado da query
        return self.query.value(0) +1                                        # Retorna o resultado da query +1

    def update_task_window(self):                                                # Função para atualizar a janela de tarefas
        self.selected_activity_data()                                            # Pega os dados da atividade selecionada
        self.LineEdit_ActivityName.setText(str(self.Activity_Name))              # Exibe o nome da atividade no LineEdit
        self.LineEdit_ActivityName.setReadOnly(True)                             # Deixa o LineEdit apenas para leitura
        self.LineEdit_ID.setText(str(self.count_tasks()))                        # Pega o ID da tarefa e exibe no LineEdit
        self.LineEdit_ID.setReadOnly(True)                                       # Deixa o LineEdit apenas para leitura
        self.LineEdit_DataCreated.setText(self.parent().date_today())            # Exibe a data atual no LineEdit
        self.RadioButton_NotStarted.toggled.connect(self.radio_button_toggled)   # Conecta o evento de seleção do radio button à função de verificação
        self.RadioButton_OnGoing.toggled.connect(self.radio_button_toggled)      # Conecta o evento de seleção do radio button à função de verificação
        self.RadioButton_Finished.toggled.connect(self.radio_button_toggled)     # Conecta o evento de seleção do radio button à função de verificação

    def radio_button_toggled(self):                                          # Função para verificar qual radio button foi selecionado
        if self.RadioButton_NotStarted.isChecked():                          # Se o radio button Não Iniciado estiver selecionado
            return 'Not Started'                                             # A variavel Status recebe o valor Não Iniciado)
        elif self.RadioButton_OnGoing.isChecked():                           # Se o radio button Em Progresso estiver selecionado
            return 'On Going'                                                # A variavel Status recebe o valor Em Progresso
        elif self.RadioButton_Finished.isChecked():                          # Se o radio button Concluído estiver selecionado
            return 'Finished'                                                # A variavel Status recebe o valor Concluído
        
    def create_task(self):
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO Tasks (ID_Task, Task_Name, Status, Created_Date, ID_Activity)
            VALUES (:ID_Task, :Task_Name, :Status, :Created_Date, :ID_Activity)
        """)
        query.bindValue(':ID_Task', self.LineEdit_ID.text())
        query.bindValue(':Task_Name', self.LineEdit_TaskName.text())
        query.bindValue(':Status', self.radio_button_toggled())
        query.bindValue(':Created_Date', self.LineEdit_DataCreated.text())
        query.bindValue(':ID_Activity', self.Activity_Index)

        if query.exec():
            self.parent().task_model.setQuery("""
                SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                Activity.Activity_Name
                FROM Tasks
                INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                """)
            self.parent().show_tasks()
            self.accept()
        else:
            print('Não foi possível criar a tarefa')


class UpdateTaskWindow(QDialog, Ui_Dialog_UpdateTask):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.update_task_window()
        self.Button_Update.clicked.connect(self.update_task)
        self.show()
        

    def selected_task_data(self):                                           # Função para pegar os dados da atividade selecionada
        index_activity = self.parent().TableView_Activity.currentIndex()             # Criamos a variavel index para pegar o índice da TableView_Activity
        model_activity = self.parent().TableView_Activity.model()                    # Criamos a variavel model para pegar o modelo da TableView_Activity
        self.Activity_Index = model_activity.data(model_activity.index(index_activity.row(), 0))        # Pega o INDEX da atividade selecionada
        self.Activity_Name = model_activity.data(model_activity.index(index_activity.row(), 1))        # Pega o NOME da atividade selecionada

        index_task = self.parent().TableView_Tasks.currentIndex()             # Criamos a variavel index para pegar o índice da TableView_Activity
        model_task = self.parent().TableView_Tasks.model()                    # Criamos a variavel model para pegar o modelo da TableView_Activity
        self.Task_Index = model_task.data(model_task.index(index_task.row(), 0))            # Pega o INDEX da atividade selecionada
        self.Task_Name = model_task.data(model_task.index(index_task.row(), 1))             # Pega o NOME da atividade selecionada
        self.Task_Status = model_task.data(model_task.index(index_task.row(), 2))           # Pega o STATUS da atividade selecionada
        self.Task_CreatedDate = model_task.data(model_task.index(index_task.row(), 3))      # Pega o DATA da atividade selecionada

    def update_task_window(self):                                                # Função para atualizar a janela de tarefas
        self.selected_task_data()                                            # Pega os dados da atividade selecionada
        self.LineEdit_ActivityName.setText(str(self.Activity_Name))              # Exibe o nome da atividade no LineEdit
        self.LineEdit_ActivityName.setReadOnly(True)                             # Deixa o LineEdit apenas para leitura
        self.LineEdit_ID.setText(str(self.Task_Index))                           # Pega o ID da tarefa e exibe no LineEdit
        self.LineEdit_ID.setReadOnly(True)                                       # Deixa o LineEdit apenas para leitura

        self.LineEdit_DataCreated.setText(self.Task_CreatedDate)            # Exibe a data atual no LineEdit

        self.LineEdit_TaskName.setText(self.Task_Name)            # Exibe a data atual no LineEdit
        if self.Task_Status == 'Not Started':
            self.RadioButton_NotStarted.setChecked(True)
        elif self.Task_Status == 'On Going':
            self.RadioButton_OnGoing.setChecked(True)
        elif self.Task_Status == 'Finished':
            self.RadioButton_Finished.setChecked(True)

    def radio_button_toggled(self):                                          # Função para verificar qual radio button foi selecionado
        if self.RadioButton_NotStarted.isChecked():                          # Se o radio button Não Iniciado estiver selecionado
            return 'Not Started'                                             # A variavel Status recebe o valor Não Iniciado)
        elif self.RadioButton_OnGoing.isChecked():                           # Se o radio button Em Progresso estiver selecionado
            return 'On Going'                                                # A variavel Status recebe o valor Em Progresso
        elif self.RadioButton_Finished.isChecked():                          # Se o radio button Concluído estiver selecionado
            return 'Finished'                                                # A variavel Status recebe o valor Concluído

    def update_task(self):
        self.radio_toggled = self.radio_button_toggled()

        query = QSqlQuery()
        query.prepare("""
            UPDATE Tasks SET Task_Name = :Task_Name, Status = :Status, Created_Date = :Created_Date, ID_Activity = :ID_Activity
            WHERE ID_Task = :ID_Task
        """)
        query.bindValue(':ID_Task', self.LineEdit_ID.text())
        query.bindValue(':Task_Name', self.LineEdit_TaskName.text())
        query.bindValue(':Status', self.radio_toggled)
        query.bindValue(':Created_Date', self.LineEdit_DataCreated.text())
        query.bindValue(':ID_Activity', self.Activity_Index)

        if query.exec():
            self.parent().task_model.setQuery("""
                SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                Activity.Activity_Name
                FROM Tasks
                INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                """)
            self.parent().show_tasks()
            self.accept()
        else:
            print('Não foi possível atualizar a tarefa')


# Cria a classe da janela de tarefas | Herda a classe QDialog e a classe Ui_Dialog_Task
class UpdateActivityWindow(QDialog, Ui_Dialog_Activity):
    # O parent=None é para que a janela de atividades não seja fechada quando a janela principal for fechada
    def __init__(self, parent=None):                    
        super().__init__(parent)                        # Configura a janela de atividades
        self.setupUi(self)                              # Configura a janela de atividades
        self.show()                                     # Mostra a janela de atividades
        self.load_importance_levels()                   # Carrega os níveis de importância no ComboBox
        self.load_activity_selected()
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Update the Activity</span></p></body></html>", None))

        self.Button_Create.clicked.connect(self.update_activity)   # Cria a atividade ao clicar no botão

    def load_importance_levels(self):                               # Função para carregar os níveis de importância no ComboBox
        importance_levels = ['Baixa', 'Média', 'Alta']              # Cria uma lista com os níveis de importância
        self.ComboBox_ImportanceLevel.addItems(importance_levels)   # Adiciona os níveis de importância no ComboBox

    def selected_activity_data(self):                                           # Função para pegar os dados da atividade selecionada
        index_activity = self.parent().TableView_Activity.currentIndex()             # Criamos a variavel index para pegar o índice da TableView_Activity
        model_activity = self.parent().TableView_Activity.model()                    # Criamos a variavel model para pegar o modelo da TableView_Activity
        self.Activity_Index = model_activity.data(model_activity.index(index_activity.row(), 0))        # Pega o INDEX da atividade selecionada
        self.Activity_Name = model_activity.data(model_activity.index(index_activity.row(), 1))        # Pega o NOME da atividade selecionada
        self.Responsible = model_activity.data(model_activity.index(index_activity.row(), 2))        # Pega o NOME da atividade selecionada
        self.Importance_Level = model_activity.data(model_activity.index(index_activity.row(), 3))        # Pega o NOME da atividade selecionada
        self.Created_Date = model_activity.data(model_activity.index(index_activity.row(), 5))        # Pega o NOME da atividade selecionada
    
    def load_activity_selected(self):
        self.selected_activity_data()
        self.LineEdit_ID.setText(str(self.Activity_Index))   # Pega o ID da atividade e exibe no LineEdit
        self.LineEdit_ActivityName.setText(str(self.Activity_Name))   # Pega o ID da atividade e exibe no LineEdit
        self.LineEdit_Responsible.setText(str(self.Responsible))
        self.ComboBox_ImportanceLevel.setCurrentText(str(self.Importance_Level))
        self.LineEdit_CreatedData.setText(str(self.Created_Date))

    def update_activity(self):
        query = QSqlQuery()
        query.prepare("""
            UPDATE Activity SET Activity_Name = :Activity_Name, Responsible = :Responsible, Importance_Level = :Importance_Level, Created_Date = :Created_Date
            WHERE ID_Activity = :ID_Activity
        """)
        query.bindValue(':ID_Activity', self.LineEdit_ID.text())
        query.bindValue(':Activity_Name', self.LineEdit_ActivityName.text())
        query.bindValue(':Responsible', self.LineEdit_Responsible.text())
        query.bindValue(':Importance_Level', self.ComboBox_ImportanceLevel.currentText())
        query.bindValue(':Created_Date', self.LineEdit_CreatedData.text())

        if query.exec():
            self.parent().activity_model.setQuery('SELECT * FROM Activity')  # Atualiza o modelo com uma nova query
            self.parent().show_tasks()
            self.accept()


app = QApplication(sys.argv)    # Configura a aplicação Qt
w = MainWindow()                # Cria a janela principal
app.exec()                      # Executa a aplicação