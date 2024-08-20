import sys
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import QTimer, QPoint, Qt

class FlameSimulation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flame Simulation")
        self.setGeometry(100, 100, 400, 600)

        self.flame_height = 300
        self.flame_width = 100
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_flame)
        self.timer.start(50)  # обновление каждые 50 мс

        self.initUI()
        self.time = 0  # Переменная для отслеживания времени

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

    def update_flame(self):
        self.time += 0.05  # Увеличиваем время
        self.update()  # Запрашиваем перерисовку окна

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_flame(painter)

    def draw_flame(self, painter):
        # Определяем цвет пламени
        color = QColor(255, 165, 0)  # Оранжевый цвет
        painter.setBrush(color)

        # Получаем текущую высоту пламени в зависимости от времени
        pulse_amplitude = 3000  # Амплитуда пульсации
        pulse_frequency = 2 * math.pi  # Частота пульсации
        flame_height = self.flame_height + pulse_amplitude * math.sin(pulse_frequency * self.time)

        # Рисуем пламя
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Устанавливаем перо как невидимое
        painter.setPen(QPen(Qt.GlobalColor.transparent))  # Используем прозрачное перо

        # Пламя в форме треугольника
        points = [
            (self.width() / 2, self.height() - 100),  # Нижняя точка
            (self.width() / 2 - self.flame_width / 2, self.height() - 100 - flame_height),  # Левый угол
            (self.width() / 2 + self.flame_width / 2, self.height() - 100 - flame_height),  # Правый угол
        ]
        painter.drawPolygon(*[QPoint(*point) for point in points])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlameSimulation()
    window.show()
    sys.exit(app.exec())