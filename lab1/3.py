# Даны три точки А,В,С, определить является ли обход А-В-С обходом по часовой
# стрелке или против (точки заданы на плоскости).
import numpy as np


def is_clockwise(a, b, c, eps=0.000001):
    return ((c[0] - a[0])*(b[1] - a[1]) - (b[0]-a[0])*(c[1]-a[1])) >= eps


a = np.array(
    list(map(float, input("Введите координаты точки(x, y)").split(' '))))
b = np.array(
    list(map(float, input("Введите координаты точки(x, y)").split(' '))))
c = np.array(
    list(map(float, input("Введите координаты точки(x, y)").split(' '))))
print("По часовой" if is_clockwise(a, b, c) else "Против часовой")

# 0 0
# 1 1
# 1 0

# 1 1
# 3 4
# 5 2
