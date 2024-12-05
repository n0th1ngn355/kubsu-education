import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Параметры симуляции
num_agents = 10  # Количество агентов
area_size = 100  # Размер области (100x100)
num_steps = 200  # Количество шагов симуляции
v = 1.0  # Скорость движения агентов за один шаг

# Инициализация позиций и направлений агентов
positions = np.random.rand(num_agents, 2) * area_size
directions = np.random.rand(num_agents, 2) * 2 - 1  # Направления в диапазоне [-1, 1]
directions /= np.linalg.norm(directions, axis=1)[:, np.newaxis]  # Нормализация направлений

# Функция обновления положения агентов
def update(frame):
    global positions, directions
    
    plt.clf()  # Очистка текущего графика
    plt.xlim(0, area_size)
    plt.ylim(0, area_size)
    
    # Обновление позиций агентов с учетом постоянной скорости
    positions += directions * v
    
    # Проверка на столкновение с границами
    for i in range(num_agents):
        for j in range(2):  # Для x и y
            if positions[i, j] < 0 or positions[i, j] > area_size:
                directions[i, j] *= -1  # Изменение направления
                directions[i] /= np.linalg.norm(directions[i])  # Нормализация после изменения направления

    # Отрисовка агентов
    plt.scatter(positions[:, 0], positions[:, 1])
    plt.title(f"Step: {frame}")

# Создание анимации
fig = plt.figure()
ani = animation.FuncAnimation(fig, update, frames=num_steps, interval=20, repeat=False)

plt.show()
