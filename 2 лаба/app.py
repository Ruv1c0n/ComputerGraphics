'''
Выполнил Матвеев Даниил Евгеньевич, группа ПМИ-32БО
Лабораторная работа №2
'''
'''
Numpy - хранение данных(точек фигуры; векторов сдвига, растяжения, поворота) и копирование данных
Matplotlib - Отрисовка и обновление фигуры и окна, виджеты для внесения изменений
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import (
    Button,
    RadioButtons,
    TextBox
)

# Методы преобразований
from changes import *

# Класс программы отрисовки и внесения изменений
class Transformations:
    def __init__(self):
        self.fig = plt.figure(figsize=(11, 11))
        self.fig.canvas.manager.set_window_title('Звезда и шестиугольник')
        self.ax = self.fig.add_subplot()
        self.__initAxes()
        self.fig.subplots_adjust(bottom=0.2)
        self.__initUI()

    # Определение сетки
    def __initAxes(self):
        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('center')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set(xlim=(-10, 10), ylim=(-10, 10))
        self.ax.grid(True)

    # Инициализация элементов управления и фигуры
    def __initUI(self):
        self.__initReflection()
        self.__initShift()
        self.__initScale()
        self.__initRotate()
        self.__initRecover()
        self.__initFigure()

    # Инициализация блока отражений
    def __initReflection(self):
        # Типы отражений по осям
        reflection_types = ['X', 'Y', 'X = Y']

        # Виджет выбора оси
        self.reflection_type_axes = self.fig.add_axes(
            [0.01, 0.07, 0.08, 0.1], 
            facecolor='#d9d9d9'
        )
        self.rbs_reflection_type = RadioButtons(
            self.reflection_type_axes,
            reflection_types,
            radio_props={'s': [64, 64, 64]},
            activecolor='black'
        )
        self.rbs_reflection_type.on_clicked(self.__reflectTypeChanger)

        self.current_reflect_type = reflection_types[0]

        # Кнопка вызова операции отражения
        self.reflection_run_axes = self.fig.add_axes([0.01, 0.01, 0.08, 0.05])
        self.b_reflection = Button(
            self.reflection_run_axes, 
            'Отразить', hovercolor='white'
        )
        self.b_reflection.on_clicked(lambda x: self.__reflect())

    # Инициализация блока сдвигов
    def __initShift(self):
        # Поля ввода значения сдвига для каждой оси
        self.input_x_shift_axes = self.fig.add_axes([0.15, 0.12, 0.15, 0.05])
        self.input_x_shift = TextBox(
            self.input_x_shift_axes, ' X ', initial='0.0')
        self.input_x_shift.on_submit(self.__setX)

        self.input_y_shift_axes = self.fig.add_axes([0.15, 0.065, 0.15, 0.05])
        self.input_y_shift = TextBox(
            self.input_y_shift_axes, ' Y ', initial='0.0')
        self.input_y_shift.on_submit(self.__setY)

        self.current_coords = np.array([
            float(self.input_x_shift.text),
            float(self.input_y_shift.text),
        ])

        # Кнопка вызова операции сдвига
        self.shift_axes = self.fig.add_axes([0.15, 0.01, 0.15, 0.05])
        self.b_shift = Button(
            self.shift_axes, 'Переместить', hovercolor='white')
        self.b_shift.on_clicked(self.__shift)

    def __initScale(self):
        self.input_x_scale_axes = self.fig.add_axes([0.35, 0.12, 0.15, 0.05])
        self.input_x_scale = TextBox(
            self.input_x_scale_axes, ' X ', initial='0.0')
        self.input_x_scale.on_submit(self.__setX)

        self.input_y_scale_axes = self.fig.add_axes([0.35, 0.065, 0.15, 0.05])
        self.input_y_scale = TextBox(
            self.input_y_scale_axes, ' Y ', initial='0.0')
        self.input_y_scale.on_submit(self.__setY)

        self.current_coords = np.array([
            float(self.input_x_scale.text),
            float(self.input_y_scale.text),
        ])

        self.scale_axes = self.fig.add_axes([0.35, 0.01, 0.15, 0.05])
        self.b_scale = Button(
            self.scale_axes, 'Масштабировать', hovercolor='white')
        self.b_scale.on_clicked(self.__scale)

    def __initRotate(self):
        self.input_x_rotate_axes = self.fig.add_axes([0.57, 0.12, 0.15, 0.05])
        self.input_x_rotate = TextBox(
            self.input_x_rotate_axes, ' X ', initial='0.0')
        self.input_x_rotate.on_submit(self.__setX)

        self.input_y_rotate_axes = self.fig.add_axes([0.57, 0.065, 0.15, 0.05])
        self.input_y_rotate = TextBox(
            self.input_y_rotate_axes, ' Y ', initial='0.0')
        self.input_y_rotate.on_submit(self.__setY)

        self.angle_axes = self.fig.add_axes([0.57, 0.01, 0.15, 0.05])
        self.angle_entry = TextBox(
            self.angle_axes, ' Angle ', initial='0'
        )
        self.angle_entry.on_submit(self.__setAngle)

        self.current_coords = np.array([
            float(self.input_x_rotate.text),
            float(self.input_y_rotate.text),
        ])
        self.current_angle = float(self.angle_entry.text)

        self.rotate_axes = self.fig.add_axes([0.74, 0.065, 0.1, 0.05])
        self.b_rotate = Button(
            self.rotate_axes, 'Повернуть', hovercolor='white')
        self.b_rotate.on_clicked(self.__rotate)

    def __initRecover(self):
        self.reset_axes = self.fig.add_axes([0.86, 0.065, 0.12, 0.05])
        self.reset_button = Button(
            self.reset_axes, 'Восстановить', hovercolor='green')
        self.reset_button.on_clicked(self.__reset)

    def __initFigure(self):
        self.const_coords = np.array([
            [0, 4, 1],
            [1, 0.9, 1],
            [4.1, 0.9, 1],
            [1.6, -0.9, 1],
            [2.5, -3.8, 1],
            [0, -2, 1],
            [-1.6, -1.1, 1],
            [-1.6, 0.6, 1],
            [0, 1.4, 1],
            [1.6, 0.6, 1],
            [1.6, -1.1, 1],
            [0, -2, 1],
            [-2.5, -3.8, 1],
            [-1.6, -0.9, 1],
            [-4.1, 0.9, 1],
            [-1, 0.9, 1]
        ])
        self.coords = np.copy(self.const_coords)

    def run(self):
        self.__draw()
        plt.show()

    def __draw(self):
        self.ax.clear()
        self.__initAxes()
        points = np.array(list(map(lambda x: x[:2], self.coords)))
        polygon = Polygon(points, fc='none', ec='black', closed=True)
        self.ax.add_patch(polygon)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __reflectTypeChanger(self, label_name):
        if label_name == 'X':
            self.current_reflect_type = 'X'
        elif label_name == 'Y':
            self.current_reflect_type = 'Y'
        elif label_name == 'X = Y':
            self.current_reflect_type = 'X = Y'

    def __reflect(self):
        if self.current_reflect_type == 'X':
            self.coords = scale_figure(self.coords, 1, -1)
        elif self.current_reflect_type == 'Y':
            self.coords = scale_figure(self.coords, -1, 1)
        elif self.current_reflect_type == 'X = Y':
            self.coords = xy_reflection(self.coords)
        self.__draw()

    def __setX(self, text):
        self.current_coords[0] = float(text)

    def __setY(self, text):
        self.current_coords[1] = float(text)

    def __setAngle(self, text):
        self.current_angle = float(text)

    def __shift(self, event):
        self.coords = shift_figure(
            self.coords, self.current_coords[0], self.current_coords[1])
        self.__draw()

    def __scale(self, event):
        self.coords = scale_figure(
            self.coords, self.current_coords[0], self.current_coords[1])
        self.__draw()

    def __rotate(self, event):
        self.coords = rotate_figure(
            self.coords, self.current_coords[0], self.current_coords[1], self.current_angle)
        self.__draw()

    def __reset(self, event):
        self.coords = np.copy(self.const_coords)
        self.__draw()


app = Transformations()
app.run()
