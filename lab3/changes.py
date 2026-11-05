
import numpy as np

'''
    coords - параметры фигуры
    shift_x - значение сдвига по оси Ox
    shift_y - значение сдвига по оси Oy
    (p_x, p_y) - точка относительно которой совершается поворот
    angle - угол поворота против часовой стрелки
    scale_x - коэффициент растяжения по оси Ox
    scale_y - коэффициент растяжения по оси Oy

    shift_figure(coords, shift_x, shift_y) - сдвиг относительно текущего положения
    xy_reflection(coords) - отражение относительно осей
    rotate_figure(coords, p_x, p_y, angle) - поворот относительно точки
    scale_figure(coords, scale_x, scale_y) - растяжение по осям
'''


def shift_figure(coords, shift_x, shift_y):
    for point in coords:
        point[0] += shift_x
        point[1] += shift_y
    return coords


def xy_reflection(coords):
    c = np.copy(coords)
    for point in c:
        point[0], point[1] = point[1], point[0]
    return c


def rotate_figure(coords, p_x, p_y, angle):
    angle_rad = np.radians(angle)
    cos_angle = np.cos(angle_rad)
    sin_angle = np.sin(angle_rad)
    transformation_matrix = np.array([
        [cos_angle, -sin_angle, 0],
        [sin_angle, cos_angle, 0],
        [0, 0, 1]
    ])

    translated_points = coords - np.array([p_x, p_y, 0])
    rotated_points = np.dot(translated_points, transformation_matrix.T)
    coords = rotated_points + np.array([p_x, p_y, 0])

    return coords


def scale_figure(coords, scale_x, scale_y):
    c = np.copy(coords)
    for point in c:
        point[0] *= scale_x if scale_x != 0 else 1
        point[1] *= scale_y if scale_y != 0 else 1
    return c
