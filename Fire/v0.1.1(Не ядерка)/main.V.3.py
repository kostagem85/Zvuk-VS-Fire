import sys
import numpy as np
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QApplication, QWidget

class MatchFlameSimulation(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Параметры симуляции
        self.grid_size = (150, 100)  # Размер сетки
        self.flame = np.zeros(self.grid_size)  # Состояние пламени
        self.heat_source = np.zeros(self.grid_size)  # Источник тепла

        # Установка источника тепла (внизу сетки, в центре)
        self.heat_source[-5:, self.grid_size[1] // 2 - 2:self.grid_size[1] // 2 + 2] = 800
        
        # Таймер для обновления симуляции
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_flame)
        self.timer.start(50)
    
    def initUI(self):
        self.setWindowTitle('Match Flame Simulation')
        self.setGeometry(100, 100, 500, 750)
    
    def update_flame(self):
        # Простая модель теплопередачи и турбулентности
        new_flame = np.copy(self.flame)
        for i in range(1, self.grid_size[0] - 1):
            for j in range(1, self.grid_size[1] - 1):
                # Обновление только в верхних ячейках над источником тепла
                if new_flame[i, j] > 10 or self.heat_source[i, j] > 0:
                    new_flame[i, j] = (
                        0.15 * (self.flame[i + 1, j] + self.flame[i - 1, j] +
                                self.flame[i, j + 1] + self.flame[i, j - 1]) +
                        0.7 * self.flame[i, j]
                    ) * 0.97
                    
                    # Добавление случайных флуктуаций
                    new_flame[i, j] += np.random.uniform(-0.1, 0.1)

        # Добавление источника тепла
        new_flame += self.heat_source

        # Ограничение температуры и предотвращение роста пламени
        new_flame[new_flame > 1000] = 1000
        new_flame[new_flame < 0] = 0

        # Ограничение области пламени
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if not (self.grid_size[0] - 50 <= i <= self.grid_size[0] - 5 and
                        self.grid_size[1] // 2 - 10 <= j <= self.grid_size[1] // 2 + 10):
                    new_flame[i, j] = 0
        
        # Обновление состояния пламени
        self.flame = new_flame
        
        # Обновление окна
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        cell_width = self.width() / self.grid_size[1]
        cell_height = self.height() / self.grid_size[0]
        
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                temp = self.flame[i, j]
                color = QColor(
                    min(255, int(255 * temp / 1000)),
                    min(255, int(150 * temp / 1000)),
                    min(255, int(50 * temp / 1000))
                )
                painter.fillRect(j * cell_width, i * cell_height, cell_width, cell_height, color)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sim = MatchFlameSimulation()
    sim.show()
    sys.exit(app.exec())
