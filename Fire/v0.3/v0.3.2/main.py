import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Задаем размеры сетки и начальные параметры
nx, ny = 100, 100
flame = np.zeros((nx, ny))
source = (50, 25)  # Источник огня

# Параметры симуляции
diffusion = 0.1  # Коэффициент диффузии
frequency = 0.1  # Частота колебаний

# Начальное распределение температуры (имитация источника огня)
flame[source] = 1.0

def update(frame):
    global flame
    # Копируем текущую матрицу пламени для расчета следующего шага
    new_flame = flame.copy()

    # Диффузия и конвекция
    new_flame[1:-1, 1:-1] += diffusion * (
        flame[:-2, 1:-1] + flame[2:, 1:-1] +
        flame[1:-1, :-2] + flame[1:-1, 2:] - 
        4 * flame[1:-1, 1:-1]
    )

    # Подпитка огня с колебаниями
    oscillation = 0.5 * (1 + np.sin(2 * np.pi * frequency * frame))
    new_flame[source] = 1.0 * oscillation

    # Обновляем матрицу пламени
    flame = new_flame

    # Ограничиваем значения, чтобы они не превышали 1
    flame = np.clip(flame, 0, 1)

    # Обновляем изображение
    img.set_array(flame)
    return [img]

# Настройка графического интерфейса
fig, ax = plt.subplots()
img = ax.imshow(flame, cmap='hot', vmin=0, vmax=1)

# Создаем анимацию
ani = FuncAnimation(fig, update, frames=200, blit=True, interval=50)
plt.show()
