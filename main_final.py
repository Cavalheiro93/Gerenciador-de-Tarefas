#====================================================================================
                        #Importando Bibliotecas do Python
#====================================================================================
import sys                      # Biblioteca usada para acessar os argumentos da linha de comando
import os                       # Biblioteca usada para acessar o sistema operacional
from datetime import datetime   # Biblioteca usada para acessar a data e hora atual

from PySide6.QtCore import Qt, QCoreApplication, QSortFilterProxyModel                      # Biblioteca usada para acessar as funções do Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QStyledItemDelegate       # Biblioteca usada para acessar os Widgets do Qt
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel, QSqlQuery           # Biblioteca usada para acessar o Banco de Dados do Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPainter, QBrush, QColor
from MainWindow2 import Ui_MainWindow                                                       # Janela Principal criada no QtDesigner
from TaskWindow import Ui_Dialog_Task                                                       # Janela de Tarefas criada no QtDesigner
from ActivityWindow import Ui_Dialog_Activity                                               # Janela de Atividades criada no QtDesigner
from Update_TaskWindow import Ui_Dialog_UpdateTask                                          # Janela de Atualização de Atividades criada no QtDesigner
from DarkMode import DarkPallete                                                         # Paleta de cores escuras                                                                      

basedir = os.path.dirname(__file__)                                                         # Define o diretório base do arquivo atual

#====================================================================================
                        #MAIN WINDOW
#====================================================================================
class MainWindow(QMainWindow, Ui_MainWindow):           # Cria a classe da janela principal | Herda a classe QMainWindow e a classe Ui_MainWindow
    def __init__(self):                                 # Construtor da classe
        super().__init__()                      
        self.setupUi(self)                              # Configura a janela principal
        self.show()                                     # Mostra a janela principal
        self.connect_db()                               # Conecta ao banco de dados
        self.show_activities()                          # Mostra as atividades no TableView
        #self.TableView_Activity.setModel(self.consulta_atividades('Atividades'))
        #self.TableView_Tasks.setModel(self.consulta_atividades('Tarefas'))
        self.show_tasks()                               # Mostra as tarefas no TableView

                            #INTERAÇÕES COM AS ATIVIDADES                           
        self.Button_NewActivity.clicked.connect(self.open_activity_window)                                  # Abre a janela de Criação de Atividades
        self.Button_EditActivity.clicked.connect(self.open_update_activity_window)                          # Abre a janela de Atualização de Atividades
        self.Button_ShowAll.clicked.connect(self.show_tasks)                                                # Mostra TODAS as tarefas no TableView
        self.TableView_Activity.doubleClicked.connect(self.open_task_window)                                # Abre a janela de Criação de Tarefas ao dar dois cliques na atividade
        self.TableView_Activity.selectionModel().currentChanged.connect(self.filter_tasks_by_activity)      # Filtra as TAREFAS de acordo com a ATIVIDADE selecionada
        self.TableView_Activity.setSortingEnabled(True)                                                     # Habilita a ordenação das colunas
        self.TableView_Activity.horizontalHeader().sectionClicked.connect(self.sort_activity_column)        # Ordena as colunas ao clicar no cabeçalho
        self.Button_DeleteActivity.clicked.connect(self.progress_count)                                    # Deleta a atividade selecionada
        self.TableView_Activity.verticalHeader().setVisible(False)

                            #INTERAÇÕES COM AS TAREFAS
        self.Button_UpdateTask.clicked.connect(self.open_update_task_window)                                # Abre a janela de Atualização de Tarefas
        self.RadioButton_AllTasks.toggled.connect(self.filter_tasks_by_radio_button)                        # Filtra TODAS AS TAREFAS
        self.RadioButton_NotStarted.toggled.connect(self.filter_tasks_by_radio_button)                      # Filtra as TAREFAS NÃO INICIADAS
        self.RadioButton_OnGoing.toggled.connect(self.filter_tasks_by_radio_button)                         # Filtra as TAREFAS EM PROGRESSO
        self.RadioButton_Finished.toggled.connect(self.filter_tasks_by_radio_button)                        # Filtra as TAREFAS CONCLUÍDAS
        self.LineEdit_FilterTask.textChanged.connect(self.custom_filter)                                    # Filtra as tarefas de acordo com o texto digitado no LineEdit
        self.TableView_Tasks.setSortingEnabled(True)                                                        # Habilita a ordenação das colunas
        self.TableView_Tasks.horizontalHeader().sectionClicked.connect(self.sort_task_column)               # Ordena as colunas ao clicar no cabeçalho
        self.TableView_Tasks.verticalHeader().setVisible(False)
        self.Button_RemoveTask.clicked.connect(self.delete_task)                                            # Deleta a tarefa selecionada
        self.size_buttons()

    def size_buttons(self):
        self.Button_NewActivity.setFixedSize(80,20)
        self.Button_EditActivity.setFixedSize(80,20)
        self.Button_ShowAll.setFixedSize(80,20)
        self.Button_DeleteActivity.setFixedSize(80,20)
        self.Button_UpdateTask.setFixedSize(80,20)
        self.Button_RemoveTask.setFixedSize(80,20)
        self.LineEdit_FilterTask.setFixedSize(80,20)

    def connect_db(self):                                                           # Função para conectar ao banco de dados
        db = QSqlDatabase.addDatabase('QSQLITE')                                    # Cria uma variavel do tipo QSqlDatabase, para conectar ao banco de dados
        db.setDatabaseName(os.path.join(basedir, 'Task_Management.db'))             # Define o nome do banco de dados | concatena o diretório base com o nome do banco de dados
        if not db.open():                                                           # Se não for possível abrir o banco de dados
            print('Não foi possível abrir o banco de dados')                        # Exibe a mensagem de erro
            return False                                                            # Retorna False
        else:                                                                       # Se for possível abrir o banco de dados
            print('Banco de dados aberto com sucesso')                              # Exibe a mensagem de sucesso
            return True                                                             # Retorna True

    def show_activities(self):                                                      # Função para exibir as atividades no TableView
        self.activity_model = QSqlQueryModel()                                      # Cria uma variavel do tipo QSqlQueryModel, para exibir os dados no TableView
        self.activity_model.setQuery('SELECT * FROM Activity')                      # Executa a query | Seleciona todos os campos da tabela Activity
        self.TableView_Activity.setModel(self.activity_model)                       # Exibe os dados no TableView
        
        # PARA PINTAR A COLUNA DE PROGRESSO
        progress_column_name = "Progress"                                                           # Nome da coluna "Progress"
        progress_delegate = ProgressDelegate(self)                                                  # Cria uma variavel do tipo ProgressDelegate, para exibir o progresso da atividade
        progress_column_index = self.activity_model.record().indexOf(progress_column_name)          # Pega o índice da coluna "Progress"
        self.TableView_Activity.setItemDelegateForColumn(progress_column_index, progress_delegate)  # Configura o delegate para a coluna "Progress"
        return

    def consulta_atividades(self, tipo):
        model = QSqlQueryModel()
        if tipo == 'Atividades':
            model.setQuery('SELECT * FROM Activity')
        elif tipo == 'Tarefas':
            model.setQuery("""
                    SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                    Activity.Activity_Name
                    FROM Tasks
                    INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                    """)
        return model

    def show_tasks(self):                                                           # Função para exibir as tarefas no TableView
        self.task_model = QSqlQueryModel()                                          # Cria uma variavel do tipo QSqlQueryModel, para exibir os dados no TableView
        # Abaixo está a query que será executada, queremos exibir todos os campos de task e o nome da atividade
        # 1. Selecionamos as Tasks que queremos exibir  | 2. Selecionamos o campo de atividade que queremos exibir
        # 3. Selecionamos a tabela de task              | 4. Aplicamos INNER JOIN nos campos ID_Activity de TASK e ID_Activity de ACTIVITY 
        self.task_model.setQuery("""
                SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                Activity.Activity_Name
                FROM Tasks
                INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                """)
        self.TableView_Tasks.setModel(self.task_model)                              # Exibe os dados no TableView
        self.task_proxy_model = QSortFilterProxyModel()                             # Cria uma variavel do tipo QSortFilterProxyModel, para filtrar os dados no TableView
        self.task_proxy_model.setSourceModel(self.task_model)                       # Configura o modelo de origem do proxy model
        self.TableView_Tasks.setModel(self.task_proxy_model)                        # Exibe os dados no TableView
        return

    def open_activity_window(self):                                                 # Função para abrir a janela de atividades
        self.activity_window = ActivityWindow(self)                                 # Cria a janela de atividades
        self.activity_window.show()                                                 # Abre a janela de atividades

    def open_task_window(self):                                                     # Função para abrir a janela de tarefas
        self.task_window = TaskWindow(self)                                         # Cria a janela de tarefas
        self.task_window.show()                                                     # Abre a janela de tarefas        

    def open_update_activity_window(self):                                          # Função para abrir a janela de atualização de atividades
        self.task_window = UpdateActivityWindow(self)                               # Cria a janela de atualização de atividades
        self.task_window.show()                                                     # Abre a janela de atualização de atividades      

    def open_update_task_window(self):                                              # Função para abrir a janela de atualização de tarefas
        self.task_window = UpdateTaskWindow(self)                                   # Cria a janela de atualização de tarefas
        self.task_window.show()                                                     # Abre a janela de atualização de tarefas          

    def date_today(self):                                                           # Função para carregar a data de criação da atividade
        self.today = datetime.today()                                               # Pega a data atual
        return self.today.strftime('%d/%m/%Y')                                      # Retorna a data atual no formato dia/mês/ano

    def filter_tasks_by_activity(self):                                                             # Função para filtrar as tarefas de acordo com a atividade selecionada
        index = self.TableView_Activity.currentIndex()                                              # Variavel index para pegar o índice da TableView_Activity
        ID_Activity = index.sibling(index.row(), 0).data()                                          # Pega o ID da atividade selecionada
        query = QSqlQuery()                                                                         # Cria uma variavel do tipo QSqlQuery, para executar a query
        query.prepare("""
                SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                Activity.Activity_Name
                FROM Tasks
                INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                WHERE Activity.ID_Activity = :ID_Activity
                """)
        query.bindValue(':ID_Activity', ID_Activity)                                                # Substitui o valor do ID_Activity na query
        if query.exec():                                                                            # Se for possível executar a query
            query_model = QSqlQueryModel()                                                          # Cria uma variavel do tipo QSqlQueryModel, para exibir os dados no TableView
            query_model.setQuery(query)                                                             # Executa a query
            self.TableView_Tasks.setModel(query_model)                                              # Exibe os dados no TableView
        else:
            print('Não foi possível filtrar as tarefas')                                            # Exibe a mensagem de erro

    def sort_activity_column(self, index):                                                          # Função para ordenar as colunas da TV_Atividades ao clicar no cabeçalho
        column_name = {                                                                             # Dicionario com os nomes das colunas
            0: 'ID_Activity',                                                                       # Chave: Valor | 0: 'ID_Activity'
            1: 'Activity_Name',                                                                     # Chave: Valor | 1: 'Activity_Name'
            2: 'Responsible',                                                                       # Chave: Valor | 2: 'Responsible'
            3: 'Importance_Level',                                                                  # Chave: Valor | 3: 'Importance_Level'
            4: 'Progress',                                                                          # Chave: Valor | 4: 'Progress'
            5: 'Created_Date'                                                                       # Chave: Valor | 5: 'Created_Date'
        }
        column_name = column_name.get(index)                                                        # Pega o nome da coluna de acordo com o índice
        if column_name is None:                                                                     # Se o nome da coluna for None, não faz nada
            return
        
        if self.activity_model.query().lastQuery().endswith('DESC'):                                # Se a última query terminar com DESC
            self.activity_model.setQuery(f'SELECT * FROM Activity ORDER BY {column_name} ASC')      # Ordena a coluna de forma crescente
        else:                                                                                       # Do contrario
            self.activity_model.setQuery(f'SELECT * FROM Activity ORDER BY {column_name} DESC')     # Ordena a coluna de forma decrescente
        
    def sort_task_column(self, index):                                                          # Função para ordenar as colunas da TV_Atividades ao clicar no cabeçalho
        column_name = {                                                                         # Dicionario com os nomes das colunas
            0: 'ID_Task',                                                                       # Chave: Valor | 0: 'ID_Task'
            1: 'Task_Name',                                                                     # Chave: Valor | 1: 'Task_Name'
            2: 'Status',                                                                        # Chave: Valor | 2: 'Status'    
            3: 'Created_Date',                                                                  # Chave: Valor | 3: 'Created_Date'
            4: 'Activity_Name'                                                                  # Chave: Valor | 4: 'Activity_Name'
        }

        column_name = column_name.get(index)                                                    # Pega o nome da coluna de acordo com o índice
        if column_name is None:                                                                 # Se o nome da coluna for None, não faz nada
            return

        if self.task_model.query().lastQuery().endswith('DESC'):                                # Se a última query terminar com DESC, ordena a coluna de forma crescente
            self.task_model.setQuery(f"""                                                       
                SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                Activity.Activity_Name
                FROM Tasks
                INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                ORDER BY {column_name} ASC
                """)
        else:                                                                                   # Do contrario, ordena a coluna de forma decrescente
            self.task_model.setQuery(f"""
                SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                Activity.Activity_Name
                FROM Tasks
                INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                ORDER BY {column_name} DESC
                """)
            
    def radio_button_toggled(self):                                                             # Função para verificar qual radio button foi selecionado
        if self.RadioButton_NotStarted.isChecked():                                             # Se o radio button Não Iniciado estiver selecionado
            return 'Not Started'                                                                # A variavel Status recebe o valor Não Iniciado)
        elif self.RadioButton_OnGoing.isChecked():                                              # Se o radio button Em Progresso estiver selecionado
            return 'On Going'                                                                   # A variavel Status recebe o valor Em Progresso
        elif self.RadioButton_Finished.isChecked():                                             # Se o radio button Concluído estiver selecionado
            return 'Finished'                                                                   # A variavel Status recebe o valor Concluído
        else:                                                                                   # Se nenhum radio button estiver selecionado
            return 'All Tasks'                                                                  # A variavel Status recebe o valor All Tasks    

    def filter_tasks_by_radio_button(self):                                                     # Função para filtrar as tarefas de acordo com o radio button selecionado
        radio_toggled = self.radio_button_toggled()                                             # Pega o valor do radio button selecionado
        if radio_toggled == 'All Tasks':                                                        # Se o valor do radio button for All Tasks, exibe todas as tarefas
            self.task_model.setQuery("""SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
            Activity.Activity_Name
            FROM Tasks
            INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity""")
        else:                                                                                   # Do contrario, filtra as tarefas de acordo com o radio button selecionado
            self.task_model.setQuery(f"""
            SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
            Activity.Activity_Name
            FROM Tasks
            INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
            WHERE Tasks.Status = '{radio_toggled}'
            """)

    def custom_filter(self, text):                                                              # Função para filtrar as tarefas de acordo com o texto digitado no LineEdit
        filter_text = text.lower()                                                              # Converte o texto para minúsculo, para ignorar a diferença entre maiúsculas e minúsculas
        self.task_proxy_model.setFilterKeyColumn(-1)                                            # Configura o filtro para todas as colunas
        self.task_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)                      # Ignora a diferença entre maiúsculas e minúsculas
        self.task_proxy_model.setFilterWildcard(f"*{filter_text}*")                             # Configura o filtro para usar caracteres curinga

    
    def count_finished_tasks(self):                                                             # Função para contar quantas tarefas estão concluídas
        index = self.TableView_Activity.currentIndex()                                          # Criamos a variavel index para pegar o índice da TableView_Activity
        ID_Activity = index.sibling(index.row(), 0).data()                                      # Pega o INDEX da atividade selecionada
        query_finished = QSqlQuery()                                                            # Cria uma variavel do tipo QSqlQuery, que contará quantas tarefas estão concluídas
        query_finished.prepare("""  
            SELECT COUNT(*) FROM Tasks
            WHERE Status = 'Finished' AND ID_Activity = :ID_Activity
        """)
        query_finished.bindValue(':ID_Activity', ID_Activity)                                   # Substitui o valor do ID_Activity na query
        query_finished.exec()                                                                   # Executa a query
        query_finished.next()                                                                   # Pega o resultado da query
        return query_finished.value(0)                                                          # Retorna o resultado da query

    def count_all_tasks(self):                                                                  # Função para contar quantas tarefas existem no banco de dados
        index = self.TableView_Activity.currentIndex()                                          # Criamos a variavel index para pegar o índice da TableView_Activity
        ID_Activity = index.sibling(index.row(), 0).data()                                      # Pega o INDEX da atividade selecionada
        query_all = QSqlQuery()                                                                 # Cria uma variavel do tipo QSqlQuery, que contará quantas tarefas existem no banco de dados
        query_all.prepare("""
            SELECT COUNT(*) FROM Tasks
            WHERE ID_Activity = :ID_Activity
        """)
        query_all.bindValue(':ID_Activity', ID_Activity)                                        # Substitui o valor do ID_Activity na query
        query_all.exec()                                                                        # Executa a query
        query_all.next()                                                                        # Pega o resultado da query
        return query_all.value(0)                                                               # Retorna o resultado da query

    def progress_count(self):                                                                   # Função para contar quantas tarefas estão concluídas
        index = self.TableView_Activity.currentIndex()                                          # Criamos a variavel index para pegar o índice da TableView_Activity
        ID_Activity = index.sibling(index.row(), 0).data()                                      # Pega o INDEX da atividade selecionada
        finished_tasks = self.count_finished_tasks()                                            # Conta quantas tarefas estão concluídas
        all_tasks = self.count_all_tasks()                                                      # Conta quantas tarefas existem no banco de dados
        progress = (finished_tasks) / all_tasks                                                 # Calcula o progresso da atividade

        query = QSqlQuery()                                                                     # Cria uma variavel do tipo QSqlQuery, para executar a query
        query.prepare("""
            UPDATE Activity SET Progress = :Progress
            WHERE ID_Activity = :ID_Activity
        """)
        query.bindValue(':ID_Activity', ID_Activity)                                            # Substitui o valor do ID_Activity na query
        query.bindValue(':Progress', f'{progress:.0%}')                                         # Substitui o valor do Progress na query
    
        if query.exec():                                                                        # Se for possível executar a query
            self.activity_model.setQuery('SELECT * FROM Activity')                              # Atualiza o modelo com uma nova query
            

    def delete_task(ID_Task):
        db = QSqlDatabase.database()  # Conecta ao banco de dados
        query = QSqlQuery()  # Cria uma query SQL
        query.prepare("DELETE FROM Tasks WHERE ID_Task = :ID_Task")  # Prepara a query para deletar o item com o ID_Task desejado
        query.bindValue(":ID_Task", ID_Task)  # Substitui o valor do ID_Task na query
        if query.exec():  # Executa a query
            print("Item deletado com sucesso!")
        else:
            print("Não foi possível deletar o item:", query.lastError().text())  # Exibe a mensagem de erro
    
    def delete_task(id_task):
        db = QSqlDatabase.database()  # Conecta ao banco de dados
        if not db.isValid():
            print("Não foi possível conectar ao banco de dados.")
            return
        query = QSqlQuery()  # Cria uma query SQL
        query.prepare("DELETE FROM tasks WHERE id_task = :id_task")  # Prepara a query para deletar o item com o id_task desejado
        query.bindValue(":id_task", id_task)  # Substitui o valor do id_task na query
        if query.exec():  # Executa a query
            print("Tarefa deletada com sucesso!")
        else:
            print("Não foi possível deletar a tarefa:", query.lastError().text())  # Exibe a mensagem de erro
        
#====================================================================================
                        #JANELA DE ATIVIDADES
#====================================================================================
class ActivityWindow(QDialog, Ui_Dialog_Activity):                  # Cria a classe da janela de tarefas | Herda a classe QDialog e a classe Ui_Dialog_Task                                                                  
    def __init__(self, parent=None):                                # O parent=None é para que a janela de atividades não seja fechada quando a janela principal for fechada
        super().__init__(parent)                                    # Configura a janela de atividades
        self.setupUi(self)                                          # Configura a janela de atividades
        self.show()                                                 # Mostra a janela de atividades
        self.load_importance_levels()                               # Carrega os níveis de importância no ComboBox
        self.load_created_date()                                    # Carrega a data de criação da atividade

        self.LineEdit_ID.setText(str(self.count_activity()))        # Pega o ID da atividade e exibe no LineEdit
        self.LineEdit_ID.setReadOnly(True)                          # Deixa o LineEdit apenas para leitura
        self.Button_Create.clicked.connect(self.create_activity)    # Cria a atividade ao clicar no botão

    def count_activity(self):                                       # Função para contar quantas atividades existem no banco de dados
        query = QSqlQuery()                                         # Cria uma variavel do tipo QSqlQuery, para executar a query
        query.exec('SELECT COUNT(*) FROM Activity')                 # Executa a query | Conta quantas atividades existem no banco de dados
        query.next()                                                # Pega o resultado da query
        return query.value(0) +1                                    # Retorna o resultado da query +1
    
    def load_importance_levels(self):                               # Função para carregar os níveis de importância no ComboBox
        importance_levels = ['Baixa', 'Média', 'Alta']              # Cria uma lista com os níveis de importância
        self.ComboBox_ImportanceLevel.addItems(importance_levels)   # Adiciona os níveis de importância no ComboBox

    def load_created_date(self):                                    # Função para carregar a data de criação da atividade
        self.LineEdit_CreatedData.setText(self.parent().date_today()) # Exibe a data atual no LineEdit
        self.LineEdit_CreatedData.setReadOnly(True)                 # Deixa o LineEdit apenas para leitura

    def create_activity(self):                                      # Função para criar a atividade
        initial_progress = '0%'                                     # Define o progresso inicial da atividade, que é 0%
        today = datetime.today()                                    # Pega a data atual, para inserir no banco de dados

        query = QSqlQuery()                                         # Cria uma variavel do tipo QSqlQuery, para executar a query
        query.prepare("""
            INSERT INTO Activity (ID_Activity, Activity_Name, Responsible, Importance_Level, Progress, Created_Date)
            VALUES (:ID_Activity, :Activity_Name, :Responsible, :Importance_Level, :Progress, :Created_Date)
        """)
        query.bindValue(':ID_Activity', self.LineEdit_ID.text())                                # Substitui o valor do ID_Activity na query
        query.bindValue(':Activity_Name', self.LineEdit_ActivityName.text())                    # Substitui o valor do Activity_Name na query
        query.bindValue(':Responsible', self.LineEdit_Responsible.text())                       # Substitui o valor do Responsible na query
        query.bindValue(':Importance_Level', self.ComboBox_ImportanceLevel.currentText())       # Substitui o valor do Importance_Level na query
        query.bindValue(':Progress', initial_progress)                                          # Substitui o valor do Progress na query
        query.bindValue(':Created_Date', today.strftime('%d/%m/%Y'))                            # Substitui o valor do Created_Date na query

        if query.exec():                                                                        # Se for possível executar a query
            self.parent().activity_model.setQuery('SELECT * FROM Activity')                     # Atualiza o modelo com uma nova query
            self.parent().show_tasks()                                                          # Atualiza o modelo com uma nova query
            self.accept()                                                                       # Fecha a janela de atividades
    

#====================================================================================
                        #JANELA DE TAREFAS
#====================================================================================
class TaskWindow(QDialog, Ui_Dialog_Task):                                      # Cria a classe da janela de tarefas | Herda a classe QDialog e a classe Ui_Dialog_Task          
    def __init__(self, parent=None):                                            # O parent=None é para que a janela de tarefas não seja fechada quando a janela principal for fechada
        super().__init__(parent)                                                # Configura a janela de tarefas
        self.setupUi(self)                                                      # Configura a janela de tarefas
        self.update_task_window()                                               # Atualiza a janela de tarefas
        self.show()                                                             # Mostra a janela de tarefas
        self.Button_Create.clicked.connect(self.create_task)                    # Cria a tarefa ao clicar no botão

    def selected_activity_data(self):                                           # Função para pegar os dados da atividade selecionada
            index = self.parent().TableView_Activity.currentIndex()             # Criamos a variavel index para pegar o índice da TableView_Activity
            model = self.parent().TableView_Activity.model()                    # Criamos a variavel model para pegar o modelo da TableView_Activity
            self.Activity_Index = model.data(model.index(index.row(), 0))       # Pega o INDEX da atividade selecionada
            self.Activity_Name = model.data(model.index(index.row(), 1))        # Pega o NOME da atividade selecionada

    def count_tasks(self):                                                      # Função para contar quantas tarefas existem no banco de dados
        self.query = QSqlQuery()                                                # Cria uma variavel do tipo QSqlQuery, para executar a query
        self.query.exec('SELECT COUNT(*) FROM Tasks')                           # Executa a query | Conta quantas tarefas existem no banco de dados
        self.query.next()                                                       # Pega o resultado da query
        return self.query.value(0) +1                                           # Retorna o resultado da query +1

    def update_task_window(self):                                               # Função para atualizar a janela de tarefas
        self.selected_activity_data()                                           # Pega os dados da atividade selecionada
        self.LineEdit_ActivityName.setText(str(self.Activity_Name))             # Exibe o nome da atividade no LineEdit
        self.LineEdit_ActivityName.setReadOnly(True)                            # Deixa o LineEdit apenas para leitura
        self.LineEdit_ID.setText(str(self.count_tasks()))                       # Pega o ID da tarefa e exibe no LineEdit
        self.LineEdit_ID.setReadOnly(True)                                      # Deixa o LineEdit apenas para leitura
        self.LineEdit_DataCreated.setText(self.parent().date_today())           # Exibe a data atual no LineEdit
        self.RadioButton_NotStarted.toggled.connect(self.radio_button_toggled)  # Conecta o evento de seleção do radio button à função de verificação
        self.RadioButton_OnGoing.toggled.connect(self.radio_button_toggled)     # Conecta o evento de seleção do radio button à função de verificação
        self.RadioButton_Finished.toggled.connect(self.radio_button_toggled)    # Conecta o evento de seleção do radio button à função de verificação

    def radio_button_toggled(self):                                             # Função para verificar qual radio button foi selecionado
        if self.RadioButton_NotStarted.isChecked():                             # Se o radio button Não Iniciado estiver selecionado
            return 'Not Started'                                                # A variavel Status recebe o valor Não Iniciado)
        elif self.RadioButton_OnGoing.isChecked():                              # Se o radio button Em Progresso estiver selecionado
            return 'On Going'                                                   # A variavel Status recebe o valor Em Progresso
        elif self.RadioButton_Finished.isChecked():                             # Se o radio button Concluído estiver selecionado
            return 'Finished'                                                   # A variavel Status recebe o valor Concluído
        
    def create_task(self):                                                                  # Função para criar a tarefa
        query = QSqlQuery()                                                                 # Cria uma variavel do tipo QSqlQuery, para executar a query
        query.prepare("""
            INSERT INTO Tasks (ID_Task, Task_Name, Status, Created_Date, ID_Activity)
            VALUES (:ID_Task, :Task_Name, :Status, :Created_Date, :ID_Activity)
        """)
        query.bindValue(':ID_Task', self.LineEdit_ID.text())                                # Substitui o valor do ID_Task na query
        query.bindValue(':Task_Name', self.LineEdit_TaskName.text())                        # Substitui o valor do Task_Name na query
        query.bindValue(':Status', self.radio_button_toggled())                             # Substitui o valor do Status na query
        query.bindValue(':Created_Date', self.LineEdit_DataCreated.text())                  # Substitui o valor do Created_Date na query
        query.bindValue(':ID_Activity', self.Activity_Index)                                # Substitui o valor do ID_Activity na query

        if query.exec():                                                                    # Se for possível executar a query
            self.parent().task_model.setQuery("""   
                SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                Activity.Activity_Name
                FROM Tasks
                INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                """)
            self.parent().progress_count()                                                  # Atualiza o modelo com uma nova query
            #self.parent().show_tasks()
            self.accept()                                                                   # Fecha a janela de tarefas
        else:
            print('Não foi possível criar a tarefa')

#====================================================================================
                        #JANELA DE ATUALIZAÇÃO DE TAREFAS
#====================================================================================
class UpdateTaskWindow(QDialog, Ui_Dialog_UpdateTask):                                          # Cria a classe da janela de tarefas | Herda a classe QDialog e a classe Ui_Dialog_Task
    def __init__(self, parent=None):                                                            # O parent=None é para que a janela de tarefas não seja fechada quando a janela principal for fechada
        super().__init__(parent)                                                                # Configura a janela de tarefas
        self.setupUi(self)                                                                      # Configura a janela de tarefas
        self.update_task_window()                                                               # Atualiza a janela de tarefas
        self.Button_Update.clicked.connect(self.update_task)                                    # Atualiza a tarefa ao clicar no botão
        self.show()                                                                             # Mostra a janela de tarefas
        

    def selected_task_data(self):                                                                       # Função para pegar os dados da atividade selecionada
        index_activity = self.parent().TableView_Activity.currentIndex()                                # Criamos a variavel index para pegar o índice da TableView_Activity
        model_activity = self.parent().TableView_Activity.model()                                       # Criamos a variavel model para pegar o modelo da TableView_Activity
        self.Activity_Index = model_activity.data(model_activity.index(index_activity.row(), 0))        # Pega o INDEX da atividade selecionada
        self.Activity_Name = model_activity.data(model_activity.index(index_activity.row(), 1))         # Pega o NOME da atividade selecionada

        index_task = self.parent().TableView_Tasks.currentIndex()                                       # Criamos a variavel index para pegar o índice da TableView_Activity
        model_task = self.parent().TableView_Tasks.model()                                              # Criamos a variavel model para pegar o modelo da TableView_Activity
        self.Task_Index = model_task.data(model_task.index(index_task.row(), 0))                        # Pega o INDEX da atividade selecionada
        self.Task_Name = model_task.data(model_task.index(index_task.row(), 1))                         # Pega o NOME da atividade selecionada
        self.Task_Status = model_task.data(model_task.index(index_task.row(), 2))                       # Pega o STATUS da atividade selecionada
        self.Task_CreatedDate = model_task.data(model_task.index(index_task.row(), 3))                  # Pega o DATA da atividade selecionada

    def update_task_window(self):                                                                       # Função para atualizar a janela de tarefas
        self.selected_task_data()                                                                       # Pega os dados da atividade selecionada
        self.LineEdit_ActivityName.setText(str(self.Activity_Name))                                     # Exibe o nome da atividade no LineEdit
        self.LineEdit_ActivityName.setReadOnly(True)                                                    # Deixa o LineEdit apenas para leitura
        self.LineEdit_ID.setText(str(self.Task_Index))                                                  # Pega o ID da tarefa e exibe no LineEdit
        self.LineEdit_ID.setReadOnly(True)                                                              # Deixa o LineEdit apenas para leitura

        self.LineEdit_DataCreated.setText(self.Task_CreatedDate)                                        # Exibe a data atual no LineEdit
        self.LineEdit_TaskName.setText(self.Task_Name)                                                  # Exibe a data atual no LineEdit

        if self.Task_Status == 'Not Started':                                                           # Se o status da tarefa for Não Iniciado
            self.RadioButton_NotStarted.setChecked(True)                                                # Marca o radio button Não Iniciado
        elif self.Task_Status == 'On Going':                                                            # Se o status da tarefa for Em Progresso
            self.RadioButton_OnGoing.setChecked(True)                                                   # Marca o radio button Em Progresso
        elif self.Task_Status == 'Finished':                                                            # Se o status da tarefa for Concluído
            self.RadioButton_Finished.setChecked(True)                                                  # Marca o radio button Concluído

    def radio_button_toggled(self):                                                                     # Função para verificar qual radio button foi selecionado
        if self.RadioButton_NotStarted.isChecked():                                                     # Se o radio button Não Iniciado estiver selecionado
            return 'Not Started'                                                                        # A variavel Status recebe o valor Não Iniciado)
        elif self.RadioButton_OnGoing.isChecked():                                                      # Se o radio button Em Progresso estiver selecionado
            return 'On Going'                                                                           # A variavel Status recebe o valor Em Progresso
        elif self.RadioButton_Finished.isChecked():                                                     # Se o radio button Concluído estiver selecionado
            return 'Finished'                                                                           # A variavel Status recebe o valor Concluído

    def update_task(self):                                                                              # Função para criar a tarefa
        self.radio_toggled = self.radio_button_toggled()                                                # Pega o valor do radio button selecionado

        query = QSqlQuery()                                                                             # Cria uma variavel do tipo QSqlQuery, para executar a query
        query.prepare("""
            UPDATE Tasks SET Task_Name = :Task_Name, Status = :Status, Created_Date = :Created_Date, ID_Activity = :ID_Activity
            WHERE ID_Task = :ID_Task
        """)
        query.bindValue(':ID_Task', self.LineEdit_ID.text())                                            # Substitui o valor do ID_Task na query
        query.bindValue(':Task_Name', self.LineEdit_TaskName.text())                                    # Substitui o valor do Task_Name na query
        query.bindValue(':Status', self.radio_toggled)                                                  # Substitui o valor do Status na query
        query.bindValue(':Created_Date', self.LineEdit_DataCreated.text())                              # Substitui o valor do Created_Date na query
        query.bindValue(':ID_Activity', self.Activity_Index)                                            # Substitui o valor do ID_Activity na query

        if query.exec():                                                                                # Se for possível executar a query
            self.parent().progress_count()                                                              # Atualiza o modelo com uma nova query
            self.parent().show_tasks()                                                                  # Atualiza o modelo com uma nova query
            self.parent().task_model.setQuery("""   
                SELECT Tasks.ID_Task, Tasks.Task_Name, Tasks.Status, Tasks.Created_Date,            
                Activity.Activity_Name
                FROM Tasks
                INNER JOIN Activity ON Tasks.ID_Activity = Activity.ID_Activity
                """)
            self.accept()                                                                               # Fecha a janela de tarefas
        else:
            print('Não foi possível atualizar a tarefa')


#====================================================================================
                        #JANELA DE ATUALIZAÇÃO DE ATIVIDADES
#====================================================================================

class UpdateActivityWindow(QDialog, Ui_Dialog_Activity):                                    # Cria a classe da janela de tarefas | Herda a classe QDialog e a classe Ui_Dialog_Task
    def __init__(self, parent=None):                                                        # O parent=None é para que a janela de atividades não seja fechada quando a janela principal for fechada       
        super().__init__(parent)                                                            # Configura a janela de atividades
        self.setupUi(self)                                                                  # Configura a janela de atividades
        self.show()                                                                         # Mostra a janela de atividades
        self.load_importance_levels()                                                       # Carrega os níveis de importância no ComboBox
        self.load_activity_selected()                                                       # Carrega os dados da atividade selecionada
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body>"      # Altera o texto do label
                                                      "<p align=\"center\">"                
                                                      "<span style=\" font-size:12pt;\">"
                                                      "Update the Activity"
                                                      "</span></p></body></html>", None))


        self.Button_Create.clicked.connect(self.update_activity)                                        # Cria a atividade ao clicar no botão

    def load_importance_levels(self):                                                                   # Função para carregar os níveis de importância no ComboBox
        importance_levels = ['Baixa', 'Média', 'Alta']                                                  # Cria uma lista com os níveis de importância
        self.ComboBox_ImportanceLevel.addItems(importance_levels)                                       # Adiciona os níveis de importância no ComboBox

    def selected_activity_data(self):                                                                   # Função para pegar os dados da atividade selecionada
        index_activity = self.parent().TableView_Activity.currentIndex()                                # Criamos a variavel index para pegar o índice da TableView_Activity
        model_activity = self.parent().TableView_Activity.model()                                       # Criamos a variavel model para pegar o modelo da TableView_Activity
        self.Activity_Index = model_activity.data(model_activity.index(index_activity.row(), 0))        # Pega o INDEX da atividade selecionada
        self.Activity_Name = model_activity.data(model_activity.index(index_activity.row(), 1))         # Pega o NOME da atividade selecionada
        self.Responsible = model_activity.data(model_activity.index(index_activity.row(), 2))           # Pega o RESPONSÁVEL da atividade selecionada
        self.Importance_Level = model_activity.data(model_activity.index(index_activity.row(), 3))      # Pega a NIVEL DE IMPORTANCIA da atividade selecionada
        self.Created_Date = model_activity.data(model_activity.index(index_activity.row(), 5))          # Pega o DATA CRIADA da atividade selecionada
    
    def load_activity_selected(self):                                                                   # Função para carregar os dados da atividade selecionada
        self.selected_activity_data()                                                                   # Pega os dados da atividade selecionada
        self.LineEdit_ID.setText(str(self.Activity_Index))                                              # Pega o ID da atividade e exibe no LineEdit
        self.LineEdit_ActivityName.setText(str(self.Activity_Name))                                     # Exibe o nome da atividade no LineEdit
        self.LineEdit_Responsible.setText(str(self.Responsible))                                        # Exibe o responsável da atividade no LineEdit
        self.ComboBox_ImportanceLevel.setCurrentText(str(self.Importance_Level))                        # Exibe o nível de importância da atividade no ComboBox
        self.LineEdit_CreatedData.setText(str(self.Created_Date))                                       # Exibe a data de criação da atividade no LineEdit

    def update_activity(self):                                                                          # Função para atualizar a atividade
        query = QSqlQuery()                                                                             # Cria uma variavel do tipo QSqlQuery, para executar a query
        query.prepare("""
            UPDATE Activity 
            SET Activity_Name = :Activity_Name, Responsible = :Responsible, Importance_Level = :Importance_Level, Created_Date = :Created_Date
            WHERE ID_Activity = :ID_Activity
        """)
        query.bindValue(':ID_Activity', self.LineEdit_ID.text())                                        # Substitui o valor do ID_Activity na query
        query.bindValue(':Activity_Name', self.LineEdit_ActivityName.text())                            # Substitui o valor do Activity_Name na query
        query.bindValue(':Responsible', self.LineEdit_Responsible.text())                               # Substitui o valor do Responsible na query
        query.bindValue(':Importance_Level', self.ComboBox_ImportanceLevel.currentText())               # Substitui o valor do Importance_Level na query
        query.bindValue(':Created_Date', self.LineEdit_CreatedData.text())                              # Substitui o valor do Created_Date na query

        if query.exec():                                                                                # Se for possível executar a query
            self.parent().activity_model.setQuery('SELECT * FROM Activity')                             # Atualiza o modelo com uma nova query
            self.parent().show_tasks()                                                                  # Atualiza o modelo com uma nova query
            self.accept()                                                                               # Fecha a janela de atividades


#====================================================================================
                        #CLASSE PARA RENDERIZAR O TEXTO DA COLUNA PROGRESSO
#====================================================================================
class ProgressDelegate(QStyledItemDelegate):                                                            # Cria a classe ProgressDelegate | Herda a classe QStyledItemDelegate
    def paint(self, painter, option, index):                                                            # Função para renderizar o texto                                                     
        progress_value = index.data()                                                                   # Obtém o valor da célula
        
        if progress_value == '100%':                                                                    # Se o valor for 100%
            text_color = QColor(0, 255, 0)                                                              # Verde para 100%
        elif progress_value == '0%':                                                                    # Se o valor for 0%
            text_color = QColor(255, 0, 0)                                                              # Vermelho para 0%
        else:                                                                                           # Se o valor for outro
            text_color = QColor(255, 165, 0)                                                            # Laranja para outros valores
        
        painter.setPen(text_color)                                                                      # Configura a cor do texto
        text_rect = option.rect                                                                         # Obtém o retângulo da célula
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignCenter, progress_value)                   # Desenha o texto no centro da célula  

#====================================================================================

app = QApplication(sys.argv)                                                                            # Configura a aplicação Qt
app.setStyle('Fusion')
app.setPalette(DarkPallete().darkPalette_color)
w = MainWindow()                                                                                        # Cria a janela principal
app.exec()                                                                                              # Executa a aplicação