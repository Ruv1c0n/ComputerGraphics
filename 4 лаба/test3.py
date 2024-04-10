import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np


def dot(p0, p1):
    return p0[0] * p1[0] + p0[1] * p1[1]

# Function to calculate the max from a list of floats


def max(t):
    return np.max(t)

# Function to calculate the min from a list of floats


def min(t):
    return np.min(t)


def cyrus_beck(vertices, line):
    n = len(vertices)
    P1_P0 = (line[1][0] - line[0][0], line[1][1] - line[0][1])

    normal = [(vertices[i][1] - vertices[(i + 1) % n][1],
               vertices[(i + 1) % n][0] - vertices[i][0]) for i in range(n)]

    P0_PEi = [(vertices[i][0] - line[0][0],
               vertices[i][1] - line[0][1]) for i in range(n)]

    numerator = [dot(normal[i], P0_PEi[i]) for i in range(n)]

    denominator = [dot(normal[i], P1_P0) for i in range(n)]

    t = [numerator[i] / denominator[i]
         if denominator[i] != 0 else 0 for i in range(n)]

    points = [(vertices[i][0] + P1_P0[0] * t[i], vertices[i][1] + P1_P0[1] * t[i])
              for i in range(n)]
    for point in points:
        plt.plot(point[0], point[1], 'ro')

    tE = [t[i] for i in range(n) if denominator[i] > 0]
    tL = [t[i] for i in range(n) if denominator[i] < 0]
    tE.append(0)
    tL.append(1)
    temp = [max(tE), min(tL)]
    if temp[0] > temp[1]:
        return None
    newPair = [(line[0][0] + P1_P0[0] * temp[0], line[0][1] + P1_P0[1] * temp[0]),
               (line[0][0] + P1_P0[0] * temp[1], line[0][1] + P1_P0[1] * temp[1])]

    return newPair

    # Входные данные: координаты вершин многоугольника (прямоугольника) и координаты концов отрезка
polygon = [[0, 0], [3, -2], [6, 0], [6, 4], [3, 6], [0, 3]]
line_p1 = [-2, 0]
line_p2 = [8, 2]
points = []

# Создание изображения многоугольника и отрезка

fig = plt.figure(figsize=(10, 10))

# Выполнение алгоритма Цируса-Бека
intersect_points = cyrus_beck(polygon, [line_p1, line_p2])
fig.canvas.manager.set_window_title('Растеризация')
ax = fig.add_subplot()
polygon_patch = Polygon(polygon, edgecolor='black', facecolor='none')
line = plt.Line2D([line_p1[0], line_p2[0]], [
                  line_p1[1], line_p2[1]], color='blue')
ax.add_line(line)
clip_line = plt.Line2D([intersect_points[0][0], intersect_points[1][0]], [
    intersect_points[0][1], intersect_points[1][1]], color='red', lw=3)
ax.add_line(clip_line)

# Отмечаем все потенциальные точки входа и выхода
for point in intersect_points:
    plt.plot(point[0], point[1], 'ro')

# Выделение части отрезка внутри многоугольника другим цветом
# Тут нужно будет использовать результаты алгоритма Цируса-Бека

# Добавляем на график многоугольник и отрезок
ax.add_patch(polygon_patch)
ax.add_line(line)

# Настройка пределов осей для лучшего отображения
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

plt.show()
