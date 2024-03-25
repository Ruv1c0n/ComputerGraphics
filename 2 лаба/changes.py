import numpy as np


def shift_figure(coords, shift_x, shift_y):
    for point in coords:
        point[0] += shift_x
        point[1] += shift_y
    return coords


def xy_reflection(coords):
    for point in coords:
        print(point)
        # point = point[1:0:-1]
        point[0], point[1] = point[1], point[0]
        print(point)
    return coords


def rotate_figure(coords, p_x, p_y, angle):
    angle = np.radians(angle)
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    transformation_matrix = np.array([[cos_angle, -sin_angle, 0],
                                      [sin_angle, cos_angle, 0],
                                      [0, 0, 1]])

    translated_points = coords - np.array([p_x, p_y, 0])
    rotated_points = np.dot(translated_points, transformation_matrix.T)
    coords = rotated_points + np.array([p_x, p_y, 0])

    return coords


def scale_figure(coords, scale_x, scale_y):
    for point in coords:
        point[0] *= scale_x if scale_x != 0 else 1
        point[1] *= scale_y if scale_y != 0 else 1
    return coords
