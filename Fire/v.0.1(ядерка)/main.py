import sys
import numpy as np
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QApplication, QWidget

class FlameSimulation(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Параметры симуляции
        self.grid_size = (100, 100)
        self.flame = np.zeros(self.grid_size)
        self.heat_source = np.zeros(self.grid_size)
        
        # Установка источника тепла
        self.heat_source[-1, self.grid_size[1] // 2 - 5:self.grid_size[1] // 2 + 5] = 1000
        
        # Таймер для обновления симуляции
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_flame)
        self.timer.start(50)
    
    def initUI(self):
        self.setWindowTitle('Flame Simulation')
        self.setGeometry(100, 100, 400, 400)
    
    def update_flame(self):
        # Расчет теплопередачи (простая модель)
        new_flame = np.copy(self.flame)
        for i in range(1, self.grid_size[0] - 1):
            for j in range(1, self.grid_size[1] - 1):
                new_flame[i, j] = (
                    0.25 * (self.flame[i + 1, j] + self.flame[i - 1, j] +
                            self.flame[i, j + 1] + self.flame[i, j - 1]) +
                    0.95 * self.flame[i, j]
                ) * 0.99

        # Добавление источника тепла
        new_flame += self.heat_source
        
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
    sim = FlameSimulation()
    sim.show()
    sys.exit(app.exec())
