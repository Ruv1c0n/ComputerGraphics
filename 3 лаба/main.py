

# if __name__ == '__main__':
#     app = App()
#     app.run()

import matplotlib.pyplot as plt

# Реализация алгоритма Брезенхема для растеризации отрезка


def bresenham_line(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    error = dx - dy

    x = x1
    y = y1

    while True:
        points.append((x, y))

        if x == x2 and y == y2:
            break

        e2 = 2 * error
        if e2 > -dy:
            error -= dy
            x += sx
        if e2 < dx:
            error += dx
            y += sy

    return points

# Реализация алгоритма Брезенхема для растеризации окружности


def bresenham_circle(radius, x_center, y_center):
    points = []
    x = 0
    y = radius
    delta = 1 - 2 * radius

    while y >= 0:
        points.extend([
            (x_center + x, y_center + y),
            (x_center - x, y_center + y),
            (x_center + x, y_center - y),
            (x_center - x, y_center - y)
        ])

        error = 2 * (delta + y) - 1
        if delta < 0 and error <= 0:
            x += 1
            delta += 2 * x + 1
            continue

        error = 2 * (delta - x) - 1
        if delta > 0 and error > 0:
            y -= 1
            delta += 1 - 2 * y
            continue

        x += 1
        delta += 2 * (x - y)
        y -= 1

    return points


# def bresenham_circle(radius, x_center, y_center):
#     radius += 1
#     x_center -= 1
#     points = []
#     x = 0
#     y = radius
#     delta = 3 - 2 * radius

#     while x <= y:
#         points.extend([
#             (x_center + x, y_center + y),
#             (x_center - x, y_center + y),
#             (x_center + x, y_center - y),
#             (x_center - x, y_center - y),
#             (x_center + y, y_center + x),
#             (x_center - y, y_center + x),
#             (x_center + y, y_center - x),
#             (x_center - y, y_center - x)
#         ])

#         if delta < 0:
#             delta += 4 * x + 6
#         else:
#             delta += 4 * (x - y) + 10
#             y -= 1

#         x += 1

#     return points


# Вызов функций и получение точек
segment_points = bresenham_line(-1, -1, 4, 2)
# circle_points = bresenham_circle(2, 3, 3)

# Отображение точек с помощью matplotlib
x_segment, y_segment = zip(*segment_points)
# x_circle, y_circle = zip(*circle_points)

plt.figure(figsize=(10, 10))
plt.plot(x_segment, y_segment, 'b.')
plt.plot([-1, 4], [-1, 2], 'black', linewidth='3')
# plt.plot(x_circle, y_circle, 'r.')
# circle = plt.Circle((2, 3), 3, color='black', fill=False)
# plt.gca().add_patch(circle)
# plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()
