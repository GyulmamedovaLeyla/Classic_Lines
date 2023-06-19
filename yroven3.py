import sys
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QPushButton, QDesktopWidget, QStatusBar, QApplication, QMessageBox, QFrame
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
# Константы
CELL_SIZE = 45
GRID_SIZE = 9
WINDOW_SIZE = CELL_SIZE * GRID_SIZE

class Board3(QFrame):
    game_over_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.selected_cell = None
        self.selected_ball = None  
        self.ball_is_selected = False 
        self.score = 0  # Переменная для хранения количества очков
        self.music_file = "zvuk.mp3"
        self.sound_effect = QMediaPlayer()
        self.sound_effect.setMedia(QMediaContent(QUrl.fromLocalFile(self.music_file)))

        self.init_grid()

    def init_grid(self):
        self.grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.update()
        # Генерация 5 шариков в случайных местах
        balls_generated = 0
        while balls_generated < 5:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            if self.grid[row][col] is None:
                self.set_ball(row, col, None)
                balls_generated += 1

    def set_ball(self, row, col, color):
        valid_colors = [QColor(255, 0, 255), QColor(0, 0, 255), QColor(255, 255, 0), QColor(0, 255, 0), QColor(255, 0, 0)]

        if color not in valid_colors:
            color = random.choice(valid_colors)
        self.grid[row][col] = color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)  # Установка белого цвета фона

        # Расчет размера клетки в зависимости от размера окна
        cell_size = CELL_SIZE


        # Рисование сетки
        painter.setPen(QColor(0, 0, 0))
        for i in range(GRID_SIZE + 1):
            painter.drawLine(0, i * cell_size + 30, GRID_SIZE * cell_size, i * cell_size + 30)
            painter.drawLine(i * cell_size, 30, i * cell_size, GRID_SIZE * cell_size + 30)

        # Рисование шариков
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                color = self.grid[row][col]
                if color:
                    painter.setBrush(color)
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(col * cell_size, row * cell_size + 30, cell_size, cell_size)

                    # Проверяем, является ли текущий шарик выбранным
                    if self.ball_is_selected and (row, col) == self.selected_ball:
                        painter.setBrush(QColor(255, 255, 255, 200))
                        painter.drawEllipse(col * cell_size, row * cell_size + 30, cell_size, cell_size)

        if self.selected_cell:
            painter.setPen(QColor(0, 0, 0))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.selected_cell[1] * cell_size, self.selected_cell[0] * cell_size + 30, cell_size, cell_size)


    def mousePressEvent(self, event):
        row = (event.y() - 30) // CELL_SIZE
        col = event.x() // CELL_SIZE


        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return

        if not self.selected_cell:
            self.selected_cell = (row, col)
            self.selected_ball = (row, col)  
            self.ball_is_selected = True  
        else:
            if self.move_is_valid(self.selected_cell, (row, col)):
                self.make_move(self.selected_cell, (row, col))
                self.selected_cell = None
                self.selected_ball = None  
                self.ball_is_selected = False  
            else:
                self.selected_cell = (row, col)
                self.selected_ball = (row, col)  
                self.ball_is_selected = True  

        self.sound_effect.play()
        QtCore.QTimer.singleShot(1000, self.sound_effect.stop)
        self.update()



    def move_is_valid(self, start, end):
        if start == end:
            return False

        if self.grid[end[0]][end[1]] is not None:
            return False

        # Проверка возможности перемещения шарика
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])

        # Проверка по горизонтали и вертикали
        if row_diff == 0 or col_diff == 0:
            if row_diff > 0:
                min_row = min(start[0], end[0])
                max_row = max(start[0], end[0])
                for row in range(min_row + 1, max_row):
                    if self.grid[row][start[1]] is not None:
                        return False
            else:
                min_col = min(start[1], end[1])
                max_col = max(start[1], end[1])
                for col in range(min_col + 1, max_col):
                    if self.grid[start[0]][col] is not None:
                        return False
        # Проверка по диагонали
        elif row_diff == col_diff:
            min_row = min(start[0], end[0])
            max_row = max(start[0], end[0])
            min_col = min(start[1], end[1])
            max_col = max(start[1], end[1])
            for i in range(1, max_row - min_row):
                row = min_row + i
                col = min_col + i
                if self.grid[row][col] is not None:
                    return False
        else:
            return False

        # Перемещение возможно
        return True



    def make_move(self, start, end):
        color = self.grid[start[0]][start[1]]
        self.grid[start[0]][start[1]] = None
        self.grid[end[0]][end[1]] = color

        if self.line_is_formed(end[0], end[1]):
            self.remove_line(end[0], end[1])
        else:
            self.fill_random_balls(start, end)  # Передаем стартовую и конечную позиции для определения количества новых шариков

        self.update()
        self.parent().status_bar.update_score(self.score)



    def line_is_formed(self, row, col):
        color = self.grid[row][col]
        if color is None:
            return False

        # Проверка по горизонтали
        count = 1
        i = 1
        while col - i >= 0 and self.grid[row][col - i] == color:
            count += 1
            i += 1
        i = 1
        while col + i < GRID_SIZE and self.grid[row][col + i] == color:
            count += 1
            i += 1
        if count >= 5:
            return True

        # Проверка по вертикали
        count = 1
        i = 1
        while row - i >= 0 and self.grid[row - i][col] == color:
            count += 1
            i += 1
        i = 1
        while row + i < GRID_SIZE and self.grid[row + i][col] == color:
            count += 1
            i += 1
        if count >= 5:
            return True

        # Проверка по диагонали (левая верхняя - правая нижняя)
        count = 1
        i = 1
        while row - i >= 0 and col - i >= 0 and self.grid[row - i][col - i] == color:
            count += 1
            i += 1
        i = 1
        while row + i < GRID_SIZE and col + i < GRID_SIZE and self.grid[row + i][col + i] == color:
            count += 1
            i += 1
        if count >= 5:
            return True

        # Проверка по диагонали (правая верхняя - левая нижняя)
        count = 1
        i = 1
        while row - i >= 0 and col + i < GRID_SIZE and self.grid[row - i][col + i] == color:
            count += 1
            i += 1
        i = 1
        while row + i < GRID_SIZE and col - i >= 0 and self.grid[row + i][col - i] == color:
            count += 1
            i += 1
        if count >= 5:
            return True

        return False

    def remove_line(self, row, col):
        color = self.grid[row][col]
        self.grid[row][col] = None

        # Удаление линии по горизонтали
        i = 1
        while col - i >= 0 and self.grid[row][col - i] == color:
            self.grid[row][col - i] = None
            i += 1
        i = 1
        while col + i < GRID_SIZE and self.grid[row][col + i] == color:
            self.grid[row][col + i] = None
            i += 1

        # Удаление линии по вертикали
        i = 1
        while row - i >= 0 and self.grid[row - i][col] == color:
            self.grid[row - i][col] = None
            i += 1
        i = 1
        while row + i < GRID_SIZE and self.grid[row + i][col] == color:
            self.grid[row + i][col] = None
            i += 1

        # Удаление линии по диагонали (левая верхняя - правая нижняя)
        i = 1
        while row - i >= 0 and col - i >= 0 and self.grid[row - i][col - i] == color:
            self.grid[row - i][col - i] = None
            i += 1
        i = 1
        while row + i < GRID_SIZE and col + i < GRID_SIZE and self.grid[row + i][col + i] == color:
            self.grid[row + i][col + i] = None
            i += 1

        # Удаление линии по диагонали (правая верхняя - левая нижняя)
        i = 1
        while row - i >= 0 and col + i < GRID_SIZE and self.grid[row - i][col + i] == color:
            self.grid[row - i][col + i] = None
            i += 1
        i = 1
        while row + i < GRID_SIZE and col - i >= 0 and self.grid[row + i][col - i] == color:
            self.grid[row + i][col - i] = None
            i += 1

        # Увеличение количества очков
        self.score += 5



    def fill_random_balls(self, start, end):
        empty_cells = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if self.grid[row][col] is None]
        
        if len(empty_cells) >= 5:
            new_balls = random.sample(empty_cells, 5)
            colors = [QColor(255, 0, 255), QColor(0, 0, 255), QColor(255, 255, 0), QColor(0, 255, 0), QColor(255, 0, 0)]
            for (row, col) in new_balls:
                color = random.choice(colors)
                self.grid[row][col] = color
            self.game_over()

        elif len(empty_cells) >= 4:
            new_balls = random.sample(empty_cells, 4)
            colors = [QColor(255, 0, 255), QColor(0, 0, 255), QColor(255, 255, 0), QColor(0, 255, 0), QColor(255, 0, 0)]
            for (row, col) in new_balls:
                color = random.choice(colors)
                self.grid[row][col] = color
            self.game_over()

        elif len(empty_cells) >= 3:
            new_balls = random.sample(empty_cells, 3)
            colors = [QColor(255, 0, 255), QColor(0, 0, 255), QColor(255, 255, 0), QColor(0, 255, 0), QColor(255, 0, 0)]
            for (row, col) in new_balls:
                color = random.choice(colors)
                self.grid[row][col] = color
            self.game_over()

        elif len(empty_cells) >= 2:
            new_balls = random.sample(empty_cells, 2)
            colors = [QColor(255, 0, 255), QColor(0, 0, 255), QColor(255, 255, 0), QColor(0, 255, 0), QColor(255, 0, 0)]
            for (row, col) in new_balls:
                color = random.choice(colors)
                self.grid[row][col] = color
            self.game_over()

        elif len(empty_cells) >= 1:
            new_balls = random.sample(empty_cells, 1)
            colors = [QColor(255, 0, 255), QColor(0, 0, 255), QColor(255, 255, 0), QColor(0, 255, 0), QColor(255, 0, 0)]
            for (row, col) in new_balls:
                color = random.choice(colors)
                self.grid[row][col] = color
            self.game_over()

        else:
            self.game_over()


        

        

    def get_random_color(self):
        colors = [QColor(255, 0, 255), QColor(0, 0, 255), QColor(255, 255, 0), QColor(0, 255, 0), QColor(255, 0, 0)]
        return random.choice(colors)


    def game_over(self):
        # Проверка на окончание игры (отсутствие возможных ходов)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] is None:
                    return False

                if row - 1 >= 0 and self.move_is_valid((row, col), (row - 1, col)):
                    return False
                if row + 1 < GRID_SIZE and self.move_is_valid((row, col), (row + 1, col)):
                    return False
                if col - 1 >= 0 and self.move_is_valid((row, col), (row, col - 1)):
                    return False
                if col + 1 < GRID_SIZE and self.move_is_valid((row, col), (row, col + 1)):
                    return False
    
        self.game_over_signal.emit()
        return True

    def update_grid(self):
        # Обновление сетки и отображение изменений
        self.update()

        if self.game_over():
            self.game_over_signal.emit()

