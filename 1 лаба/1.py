# Определить принадлежит ли точка прямой. Прямая задана своими
# коэффициентами.
import numpy as np


def is_point_on_line(coef, p):
    return abs(coef[0] * p[0] + coef[1] * p[1] + coef[2]) <= 0.000001


coef = np.array(
    list(map(float, input("Введите коэффициенты прямой(a, b, c)").split(' '))))
p = np.array(
    list(map(float, input("Введите координаты точки(x, y)").split(' '))))
print("Принадлежит" if is_point_on_line(coef, p) else "Не принадлежит")

# 0.5 2 1
# -0.5 0

# 1 -1 0
# 0 0

# 2 -3 6
# 4 1

# 2 3 -6
# 3 0

# -0.8 1.2 0
# 0 0
