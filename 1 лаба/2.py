# Даны три точки А,В,С. Определить принадлежит ли точка С лучу АВ.
import numpy as np


def is_point_on_ray(a, b, c, eps=0.000001):
    if (c[0] - a[0])*(b[1] - a[1]) == (b[0]-a[0])*(c[1]-a[1]):
        if (c[0] - a[0])*(b[1] - a[1]) >= eps and (b[0]-a[0])*(c[1]-a[1]) >= eps:
            return True
    return False


a = np.array(
    list(map(float, input("Введите координаты точки(x, y)").split(' '))))
b = np.array(
    list(map(float, input("Введите координаты точки(x, y)").split(' '))))
c = np.array(
    list(map(float, input("Введите координаты точки(x, y)").split(' '))))
print("Принадлежит" if is_point_on_ray(a, b, c) else "Не принадлежит")

# 1 2
# 5 6
# 3 4

# 1 2
# 5 6
# 3 3

# 1.5 2.3
# 4.7 6.2
# 2.9 4.1

# 0.8 1.2
# 3.9 5.7
# 1.5 2.0

# 2.2 3.1
# 5.5 6.4
# 4.3 5.9
