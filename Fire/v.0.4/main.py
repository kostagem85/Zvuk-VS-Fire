import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer
from scipy import ndimage
import sys

def generate_flame(width, height):
    # Создаем массив случайных значений
    flame = np.random.rand(height, width) * 255
    
    # Применяем размытие Гаусса для создания эффекта пламени
    flame = ndimage.gaussian_filter(flame, sigma=(10, 4))
    
    # Создаем цветовую карту для пламени
    cmap = np.array([[0, 0, 0],
                     [128, 0, 0],
                     [255, 128, 0],
                     [255, 255, 0],
                     [255, 255, 255]], dtype=np.uint8)
    
    # Применяем цветовую карту к пламени
    flame = np.interp(flame, np.linspace(0, 255, len(cmap)), cmap.ravel()).reshape(flame.shape)
    
    return flame

class FlameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пламя свечи")
        self.setGeometry(100, 100, 400, 400)
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_flame)
        self.timer.start(50)
        
        self.show()
    
    def update_flame(self):
        flame = generate_flame(100, 200)
        image = QImage(flame.data, flame.shape[1], flame.shape[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlameWindow()
    sys.exit(app.exec())