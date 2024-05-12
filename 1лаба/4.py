# Заданы коэффициенты уравнения плоскости и координаты точки.
# Определить принадлежит ли точка плоскости.
import numpy as np


def is_point_on_plane(c, p, eps=0.000001):
    if abs(c[0] * p[0] + c[1] * p[1] + c[2] * p[2] + c[3]) <= eps:
        return True
    else:
        return False


coefficients = np.array(
    list(map(float, input("Введите коэффициенты плоскости(a, b, c, d)").split(' '))))
point = np.array(
    list(map(float, input("Введите координаты точки(x, y, z)").split(' '))))

print("Принадлежит" if is_point_on_plane(
    coefficients, point) else "Не принадлежит")

# 2 -3 1 -4
# 1 2 -1

# 1 1 1 0
# 0 0 0
