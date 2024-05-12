# Дана окружность (центр окружности и радиус) и точка P. Найти точки
# пересечения окружности и касательных прямых проходящих через точку P.
import math
import numpy as np


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


def get_intersections(center, radius, point):
    hypotenuse = np.linalg.norm((point - center))
    if hypotenuse < radius:
        return '\n\tThere are no tangents\n'
    elif hypotenuse == radius:
        return ("\n\tPoint: {}\n".format(point))
    else:
        second_radius = np.sqrt(np.square(hypotenuse) - np.square(radius))
        hypotenuse_part = (np.square(radius) - np.square(second_radius) +
                           np.square(hypotenuse)) / (2 * hypotenuse)
        catheter = math.sqrt(np.square(radius) - np.square(hypotenuse_part))
        p_on_h = np.array([(center[0] + hypotenuse_part * (point[0] - center[0]) / hypotenuse),
                           (center[1] + hypotenuse_part * (point[1] - center[1]) / hypotenuse)])
        p1 = np.array([(p_on_h[0] + catheter * (point[1] - center[1]) / hypotenuse),
                      (p_on_h[1] - catheter * (point[0] - center[0]) / hypotenuse)])
        p2 = np.array([(p_on_h[0] - catheter * (point[1] - center[1]) / hypotenuse),
                      (p_on_h[1] + catheter * (point[0] - center[0]) / hypotenuse)])
        return ("\n\tFirst point: {}\n\tSecond point: {}\n".format(p1, p2))


center = np.array(
    list(map(float, input("\nВведите координаты центра(x, y) ").split(' '))))
radius = float(input("Введите радиус "))
point = np.array(
    list(map(float, input("Введите координаты точки(x, y) ").split(' '))))
print(get_intersections(center, radius, point))
