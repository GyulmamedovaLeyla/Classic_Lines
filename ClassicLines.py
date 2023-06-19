import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QPushButton, QDesktopWidget, QStatusBar, QApplication, QMessageBox
from yroven import Board
from yroven2 import Board2
from yroven3 import Board3
# Константы
CELL_SIZE = 45
GRID_SIZE = 9
WINDOW_SIZE = CELL_SIZE * GRID_SIZE

class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        self.main_window = MainWindow
        MainWindow.setObjectName("Главное меню")
        MainWindow.setStyleSheet("background-color: rgb(161,202,241);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        desktop = QDesktopWidget()
        screen_geometry = desktop.screenGeometry()
        center_x = (screen_geometry.width() - 600) // 2
        center_y = (screen_geometry.height() - 450) // 2
        self.main_window.setGeometry(center_x, center_y, 600, 450)

        self.rules_dialog = None  # Переменная-член для окна правил игры
        self.game_window = None 
        # QVBoxLayout для размещения виджетов вертикально
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)

    
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAutoFillBackground(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.layout.addWidget(self.label) 


        #  кнопки "Уровень 1", "Уровень 2" и "Уровень 3"
        self.btn_lvl1 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_lvl2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_lvl3 = QtWidgets.QPushButton(self.centralwidget)

        self.btn_lvl1.setStyleSheet("background-color: rgb(220,195,232);")
        self.btn_lvl2.setStyleSheet("background-color: rgb(220,195,232);")
        self.btn_lvl3.setStyleSheet("background-color: rgb(220,195,232);")

        font = QtGui.QFont()
        font.setFamily("Exotc350 DmBd BT")
        font.setPointSize(14)
        self.btn_lvl1.setFont(font)
        self.btn_lvl2.setFont(font)
        self.btn_lvl3.setFont(font)

        self.btn_lvl1.setText("Уровень 1")
        self.btn_lvl2.setText("Уровень 2")
        self.btn_lvl3.setText("Уровень 3")

        self.btn_lvl1.setObjectName("btn_lvl1")
        self.btn_lvl2.setObjectName("btn_lvl2")
        self.btn_lvl3.setObjectName("btn_lvl3")

        self.layout.addWidget(self.btn_lvl1)
        self.layout.addWidget(self.btn_lvl2)
        self.layout.addWidget(self.btn_lvl3)

        # кнопка "Правила игры"
        self.btn_pr = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        self.btn_pr.setStyleSheet("background-color: rgb(220,195,232);")
        font.setFamily("Exotc350 DmBd BT")
        font.setPointSize(14)
        self.btn_pr.setFont(font)
        self.btn_pr.setObjectName("btn_pr")
        self.layout.addWidget(self.btn_pr)  

        # кнопка "Выход из игры"
        self.btn_ex = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        self.btn_ex.setStyleSheet("background-color: rgb(220,195,232);")
        font.setFamily("Exotc350 DmBd BT")
        font.setPointSize(14)
        self.btn_ex.setFont(font)
        self.btn_ex.setObjectName("btn_ex")
        self.layout.addWidget(self.btn_ex) 

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # функции для обработки событий кнопок
        self.add_functions()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Главное меню"))
        self.label.setText(_translate("MainWindow", "Lines"))
        self.btn_pr.setText(_translate("MainWindow", "Правила игры"))
        self.btn_ex.setText(_translate("MainWindow", "Выход из игры"))

    def add_functions(self):
        self.btn_lvl1.clicked.connect(self.start_game1)
        self.btn_lvl2.clicked.connect(self.start_game2)
        self.btn_lvl3.clicked.connect(self.start_game3)
        self.btn_pr.clicked.connect(self.pravila_game)
        self.btn_ex.clicked.connect(self.close_game)

    def start_game1(self):
        self.main_window.close()
        self.game = Lines()
        self.game.main_window = self.main_window
        self.game.board.init_grid() # генерация шариков
        print('игра запущена')
        self.game.show()

    def start_game2(self):
        self.main_window.close()
        self.game = Lines2()
        self.game.main_window = self.main_window
        self.game.board.init_grid()  
        self.game.show()

    def start_game3(self):
        self.main_window.close()
        self.game = Lines3()
        self.game.main_window = self.main_window
        self.game.board.init_grid()  
        self.game.show()

    def close_game(self):
        reply = QMessageBox.question(
        self.main_window, "Выход", "Вы уверены, что хотите выйти из игры?", QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.main_window.close()
        else:
            self.main_window.show()




    def pravila_game(self):
        self.rules_dialog = QMessageBox(self.main_window)
        self.rules_dialog.setWindowTitle("Правила игры")
        self.rules_dialog.setText("Цель игры - собрать как можно больше линий из пяти и более шариков одного цвета.\n\n"
                                "1. Вы можете выбрать шарик, кликнув по нему левой кнопкой мыши.\n"
                                "2. Далее кликните на пустую ячейку, куда хотите передвинуть выбранный шарик.\n"
                                "3. Если при этом образуется линия из пяти или более шариков одного цвета, они исчезнут, "
                                "и вы получите очки.\n"
                                "4. Если после удаления шариков образуются новые линии, они тоже исчезнут, и вы получите еще "
                                "очки.\n"
                                "5. Игра заканчивается, когда на поле не остается возможных ходов (нет пустых ячеек для "
                                "перемещения шариков).\n\n"
                                "Удачи!")
        self.rules_dialog.setStandardButtons(QMessageBox.Ok)
        self.rules_dialog.exec_()

class Lines(QMainWindow):
    WINDOW_SIZE = CELL_SIZE * GRID_SIZE
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lines")
        self.setGeometry(100, 100, 500, 600)  # Устанавливает размеры окна
        self.resize(470, 470)
        self.center_window()
        self.main_window = MainWindow
        self.board = Board()
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)
        self.setCentralWidget(self.board)
        self.setStyleSheet("background-color: #F5F5F5;")  # Установка светло-серого цвета фона
        self.add_main_menu_button()
        self.board.game_over_signal.connect(self.show_game_over_dialog)

    def center_window(self):
        frame_geo = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geo.moveCenter(center_point)
        self.move(frame_geo.topLeft())

    def resizeEvent(self, event):
        new_size = min(self.width(), self.height())
        if new_size < Lines.WINDOW_SIZE:
            new_size = Lines.WINDOW_SIZE
        self.resize(new_size, new_size)


    def add_main_menu_button(self):
        main_menu_button = QPushButton("Главное меню", self)
        main_menu_button.setGeometry(0, 0, 100, 30)
        main_menu_button.clicked.connect(self.menu)

    def show_game_over_dialog(self):
        game_over_dialog = QMessageBox()
        game_over_dialog.setWindowTitle("Конец игры")
        game_over_dialog.setText("Игра окончена. Выберите дальнейшее действие. \n Вы набрали: "+ str(self.board.score) + " очков!")
        game_over_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        game_over_dialog.setDefaultButton(QMessageBox.Yes)
        
        new_game_button = game_over_dialog.button(QMessageBox.Yes)
        new_game_button.setText("Новая игра")
        
        main_menu_button = game_over_dialog.button(QMessageBox.No)
        main_menu_button.setText("Главное меню")
        
        reply = game_over_dialog.exec()
        
        if reply == QMessageBox.Yes:
            self.board.init_grid()
        elif reply == QMessageBox.No:
            self.menu()

    def menu(self):
        self.board.close()
        self.close()  # Закрыть окно игры
        self.main_window.show()  # Показать главное меню

class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()

        self.showMessage("Счёт: 0")

    def update_score(self, score):
        self.showMessage("Счёт: {}".format(score))

class Lines2(QMainWindow):
    WINDOW_SIZE = CELL_SIZE * GRID_SIZE
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lines")
        self.setGeometry(100, 100, 500, 600)  # Устанавливает размеры окна
        self.resize(470, 470)
        self.center_window()
        self.main_window = MainWindow
        self.board = Board2()
        self.status_bar = StatusBar2()
        self.setStatusBar(self.status_bar)
        self.setCentralWidget(self.board)
        self.setStyleSheet("background-color: #F5F5F5;")  # Установка светло-серого цвета фона
        self.add_main_menu_button()
        self.board.game_over_signal.connect(self.show_game_over_dialog)

    def center_window(self):
        frame_geo = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geo.moveCenter(center_point)
        self.move(frame_geo.topLeft())

    def resizeEvent(self, event):
        new_size = min(self.width(), self.height())
        if new_size < Lines2.WINDOW_SIZE:
            new_size = Lines2.WINDOW_SIZE
        self.resize(new_size, new_size)


    def add_main_menu_button(self):
        main_menu_button = QPushButton("Главное меню", self)
        main_menu_button.setGeometry(0, 0, 100, 30)
        main_menu_button.clicked.connect(self.menu)

    def show_game_over_dialog(self):
        game_over_dialog = QMessageBox()
        game_over_dialog.setWindowTitle("Конец игры")
        game_over_dialog.setText("Игра окончена. Выберите дальнейшее действие. \n Вы набрали: "+ str(self.board.score) + " очков!")
        game_over_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        game_over_dialog.setDefaultButton(QMessageBox.Yes)
        
        new_game_button = game_over_dialog.button(QMessageBox.Yes)
        new_game_button.setText("Новая игра")
        
        main_menu_button = game_over_dialog.button(QMessageBox.No)
        main_menu_button.setText("Главное меню")
        
        reply = game_over_dialog.exec()
        
        if reply == QMessageBox.Yes:
            self.board.init_grid()
        elif reply == QMessageBox.No:
            self.menu()

    def menu(self):
        self.board.close()
        self.close()  # Закрыть окно игры
        self.main_window.show()  # Показать главное меню

class StatusBar2(QStatusBar):
    def __init__(self):
        super().__init__()

        self.showMessage("Счёт: 0")

    def update_score(self, score):
        self.showMessage("Счёт: {}".format(score))

class Lines3(QMainWindow):
    WINDOW_SIZE = CELL_SIZE * GRID_SIZE
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lines")
        self.setGeometry(100, 100, 500, 600)  # Устанавливает размеры окна
        self.resize(470, 470)
        self.center_window()
        self.main_window = MainWindow
        self.board = Board3()
        self.status_bar = StatusBar3()
        self.setStatusBar(self.status_bar)
        self.setCentralWidget(self.board)
        self.setStyleSheet("background-color: #F5F5F5;")  # Установка светло-серого цвета фона
        self.add_main_menu_button()
        self.board.game_over_signal.connect(self.show_game_over_dialog)

    def center_window(self):
        frame_geo = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geo.moveCenter(center_point)
        self.move(frame_geo.topLeft())

    def resizeEvent(self, event):
        new_size = min(self.width(), self.height())
        if new_size < Lines3.WINDOW_SIZE:
            new_size = Lines3.WINDOW_SIZE
        self.resize(new_size, new_size)


    def add_main_menu_button(self):
        main_menu_button = QPushButton("Главное меню", self)
        main_menu_button.setGeometry(0, 0, 100, 30)
        main_menu_button.clicked.connect(self.menu)

    def show_game_over_dialog(self):
        game_over_dialog = QMessageBox()
        game_over_dialog.setWindowTitle("Конец игры")
        game_over_dialog.setText("Игра окончена. Выберите дальнейшее действие. \n Вы набрали: "+ str(self.board.score) + " очков!")
        game_over_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        game_over_dialog.setDefaultButton(QMessageBox.Yes)
        
        new_game_button = game_over_dialog.button(QMessageBox.Yes)
        new_game_button.setText("Новая игра")
        
        main_menu_button = game_over_dialog.button(QMessageBox.No)
        main_menu_button.setText("Главное меню")
        
        reply = game_over_dialog.exec()
        
        if reply == QMessageBox.Yes:
            self.board.init_grid()
        elif reply == QMessageBox.No:
            self.menu()

    def menu(self):
        self.board.close()
        self.close()  # Закрыть окно игры
        self.main_window.show()  # Показать главное меню

class StatusBar3(QStatusBar):
    def __init__(self):
        super().__init__()

        self.showMessage("Счёт: 0")

    def update_score(self, score):
        self.showMessage("Счёт: {}".format(score))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())