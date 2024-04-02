'''
Выполнил Матвеев Даниил Евгеньевич, группа ПМИ-32БО
Лабораторная работа №3

Numpy - хранение данных(точек фигуры; векторов сдвига, растяжения, поворота) и копирование данных
Matplotlib - Отрисовка и обновление фигуры и окна, виджеты для внесения изменений
Transformations - основной класс программы для отрисовки и внесения изменений
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.widgets import (
    Button,
    RadioButtons,
    TextBox
)

# Методы преобразований
from changes import *


class Rasterization:
    '''
        self.__initAxes() - инициализация сетки
        __initUI(self) - инициализация элементов управления и фигуры
        
        run(self) - запуск работы класса
    '''

    def __init__(self):
        self.fig = plt.figure(figsize=(11, 11))
        self.fig.canvas.manager.set_window_title('Растеризация')
        self.ax = self.fig.add_subplot()
        self.__initAxes()
        self.fig.subplots_adjust(bottom=0.2)
        self.__initUI()

    def __initAxes(self):
        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('center')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set(
            xlim=(-10, 10),
            xticks=np.arange(-10, 10, 1),
            ylim=(-10, 10),
            yticks=np.arange(-10, 10, 1)
        )
        self.ax.grid(True)

    def __initUI(self):
        self.__initChoosingShape()
        self.__initInputLine()
        # self.__initInputCircle()
        self.__initDrawButton()

    def __initChoosingShape(self):
        figure_type = ['Line', 'Circle']
        self.choose_figure_type_axes = self.fig.add_axes(
            [0.01, 0.89, 0.08, 0.08],
            facecolor='#d9d9d9'
        )
        self.rbs_figure_type = RadioButtons(
            self.choose_figure_type_axes,
            figure_type,
            radio_props={'s': [64, 64]},
            activecolor='black',
        )
        self.rbs_figure_type.on_clicked(self.__choosingShape)

        self.current_figure_type = figure_type[0]

    def __initInputLine(self):
        self.s_x_axes = self.fig.add_axes([0.15, 0.9, 0.05, 0.05])
        self.input_s_x = TextBox(
            self.s_x_axes,
            'Start X ',
            initial='0.0'
        )
        self.cid_isx = self.input_s_x.on_submit(self.__setStartX)

        self.s_y_axes = self.fig.add_axes([0.25, 0.9, 0.05, 0.05])
        self.input_s_y = TextBox(
            self.s_y_axes,
            'Start Y ',
            initial='0.0'
        )
        self.cid_isy = self.input_s_y.on_submit(self.__setStartY)

        self.e_x_axes = self.fig.add_axes([0.35, 0.9, 0.05, 0.05])
        self.input_e_x = TextBox(
            self.e_x_axes,
            'End X ',
            initial='0.0'
        )
        self.cid_iex = self.input_e_x.on_submit(self.__setEndX)

        self.e_y_axes = self.fig.add_axes([0.45, 0.9, 0.05, 0.05])
        self.input_e_y = TextBox(
            self.e_y_axes,
            'End Y ',
            initial='0.0'
        )
        self.cid_iey = self.input_e_y.on_submit(self.__setEndY)

        self.const_line_coords = np.array([
            [
                np.float64(self.input_s_x.text),
                np.float64(self.input_e_x.text)
            ],
            [
                np.float64(self.input_s_y.text),
                np.float64(self.input_e_y.text)
            ]
        ])

    def __initInputCircle(self):
        self.x_axes = self.fig.add_axes([0.15, 0.9, 0.05, 0.05])
        self.input_x = TextBox(
            self.x_axes,
            'X ',
            initial='0.0'
        )
        self.cid_ix = self.input_x.on_submit(self.__setX)

        self.y_axes = self.fig.add_axes([0.23, 0.9, 0.05, 0.05])
        self.input_y = TextBox(
            self.y_axes,
            'Y ',
            initial='0.0'
        )
        self.cid_iy = self.input_y.on_submit(self.__setY)

        self.r_axes = self.fig.add_axes([0.34, 0.9, 0.05, 0.05])
        self.input_r = TextBox(
            self.r_axes,
            'Radius ',
            initial='0.0'
        )
        self.cid_ir = self.input_r.on_submit(self.__setRadius)

        self.const_circle_coords = np.array([
            np.float64(self.input_x.text),
            np.float64(self.input_y.text),
            np.float64(self.input_r.text)
        ])

    def __initDrawButton(self):
        self.draw_axes = self.fig.add_axes([0.52, 0.9, 0.1, 0.05])
        self.b_draw = Button(
            self.draw_axes,
            'Нарисовать',
            hovercolor='white'
        )
        self.b_draw.on_clicked(self.__drawFigure)

    def run(self):
        plt.show()

    def __choosingShape(self, label_name):
        if label_name == 'Line':
            self.current_figure_type = 'Line'
            self.__setVisibleUI('Line')
        elif label_name == 'Circle':
            self.current_figure_type = 'Circle'
            self.__setVisibleUI('Circle')

    def __setVisibleUI(self, type):
        if type == 'Line':
            self.x_axes.set_axis_off()
            self.y_axes.set_axis_off()
            self.r_axes.set_axis_off()
            self.__initInputLine()
        elif type == 'Circle':
            self.__initInputCircle()
            self.s_x_axes.set_axis_off()
            self.s_y_axes.set_axis_off()
            self.e_x_axes.set_axis_off()
            self.e_y_axes.set_axis_off()
        self.fig.canvas.draw()
    
    def __drawFigure(self, event):
        if self.current_figure_type == 'Line':
            self.__drawLine()
        elif self.current_figure_type == 'Circle':
            self.__drawCircle()

    def __drawLine(self):
        self.ax.clear()
        self.__initAxes()
        self.coords = np.copy(self.const_line_coords)
        line = plt.Line2D(
            *self.coords,
            lw=2,
            color='black'
        )
        self.ax.add_line(line)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __drawCircle(self):
        self.ax.clear()
        self.__initAxes()
        self.coords = np.copy(self.const_circle_coords)
        circle = Circle(
            self.coords,
            self.coords[2],
            fc='none',
            ec='black',
            lw=2
        )
        self.ax.add_patch(circle)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    # def __initUI(self):
    #     self.__initInputLine()
    #     self.__initBresenham()
    #     self.__initReflection()
    #     self.__initShift()
    #     self.__initScale()
    #     self.__initRotate()
    #     self.__initRecover()
    #     self.__initFigure()

    # def __initInputLine(self):
    #     self.s_x_axes = self.fig.add_axes([0.05, 0.9, 0.05, 0.05])
    #     self.input_s_x = TextBox(
    #         self.s_x_axes,
    #         'Start X ',
    #         initial='0.0'
    #     )
    #     self.input_s_x.on_submit(self.__setStartX)

    #     self.s_y_axes = self.fig.add_axes([0.15, 0.9, 0.05, 0.05])
    #     self.input_s_y = TextBox(
    #         self.s_y_axes,
    #         'Start Y ',
    #         initial='0.0'
    #     )
    #     self.input_s_y.on_submit(self.__setStartY)

    #     self.e_x_axes = self.fig.add_axes([0.25, 0.9, 0.05, 0.05])
    #     self.input_e_x = TextBox(
    #         self.e_x_axes,
    #         'End X ',
    #         initial='0.0'
    #     )
    #     self.input_e_x.on_submit(self.__setEndX)

    #     self.e_y_axes = self.fig.add_axes([0.35, 0.9, 0.05, 0.05])
    #     self.input_e_y = TextBox(
    #         self.e_y_axes,
    #         'End Y ',
    #         initial='0.0'
    #     )
    #     self.input_e_y.on_submit(self.__setEndY)

    #     self.const_coords = np.array([
    #         [
    #             np.float64(self.input_s_x.text),
    #             np.float64(self.input_s_y.text),
    #             1
    #         ],
    #         [
    #             np.float64(self.input_e_x.text),
    #             np.float64(self.input_e_y.text),
    #             1
    #         ]
    #     ])

    #     self.draw_axes = self.fig.add_axes([0.42, 0.9, 0.1, 0.05])
    #     self.b_draw = Button(
    #         self.draw_axes,
    #         'Нарисовать',
    #         hovercolor='white'
    #     )
    #     self.b_draw.on_clicked(self.__new_line)

    # def __initBresenham(self):
    #     self.br_axes = self.fig.add_axes([0.54, 0.9, 0.1, 0.05])
    #     self.b_br = Button(
    #         self.br_axes,
    #         'Растеризация',
    #         hovercolor='white'
    #     )
    #     self.b_br.on_clicked(self.__raster)

    # def __initReflection(self):
    #     # Типы отражений по осям
    #     reflection_types = ['X', 'Y', 'X = Y']

    #     # Виджет выбора оси
    #     self.reflection_type_axes = self.fig.add_axes(
    #         [0.01, 0.07, 0.08, 0.1],
    #         facecolor='#d9d9d9'
    #     )
    #     self.rbs_reflection_type = RadioButtons(
    #         self.reflection_type_axes,
    #         reflection_types,
    #         radio_props={'s': [64, 64, 64]},
    #         activecolor='black'
    #     )
    #     self.rbs_reflection_type.on_clicked(self.__reflectTypeChanger)

    #     self.current_reflect_type = reflection_types[0]

    #     # Кнопка вызова операции отражения
    #     self.reflection_run_axes = self.fig.add_axes([0.01, 0.01, 0.08, 0.05])
    #     self.b_reflection = Button(
    #         self.reflection_run_axes,
    #         'Отразить',
    #         hovercolor='white'
    #     )
    #     self.b_reflection.on_clicked(self.__reflect)

    # def __initShift(self):
    #     # Поля ввода значения сдвига для каждой оси
    #     self.input_x_shift_axes = self.fig.add_axes([0.15, 0.12, 0.15, 0.05])
    #     self.input_x_shift = TextBox(
    #         self.input_x_shift_axes,
    #         ' X ',
    #         initial='0.0'
    #     )
    #     self.input_x_shift.on_submit(self.__setX)

    #     self.input_y_shift_axes = self.fig.add_axes([0.15, 0.065, 0.15, 0.05])
    #     self.input_y_shift = TextBox(
    #         self.input_y_shift_axes,
    #         ' Y ',
    #         initial='0.0'
    #     )
    #     self.input_y_shift.on_submit(self.__setY)

    #     self.current_change = np.array([
    #         np.float64(self.input_x_shift.text),
    #         np.float64(self.input_y_shift.text)
    #     ])

    #     # Кнопка вызова операции сдвига
    #     self.shift_axes = self.fig.add_axes([0.15, 0.01, 0.15, 0.05])
    #     self.b_shift = Button(
    #         self.shift_axes,
    #         'Переместить',
    #         hovercolor='white'
    #     )
    #     self.b_shift.on_clicked(self.__shift)

    # def __initScale(self):
    #     # Поля ввода значения растягивания для каждой оси
    #     self.input_x_scale_axes = self.fig.add_axes([0.35, 0.12, 0.15, 0.05])
    #     self.input_x_scale = TextBox(
    #         self.input_x_scale_axes, ' X ', initial='0.0')
    #     self.input_x_scale.on_submit(self.__setX)

    #     self.input_y_scale_axes = self.fig.add_axes([0.35, 0.065, 0.15, 0.05])
    #     self.input_y_scale = TextBox(
    #         self.input_y_scale_axes,
    #         ' Y ',
    #         initial='0.0'
    #     )
    #     self.input_y_scale.on_submit(self.__setY)

    #     self.current_change = np.array([
    #         np.float64(self.input_x_scale.text),
    #         np.float64(self.input_y_scale.text)
    #     ])

    #     # Кнопка вызова операции растягивания
    #     self.scale_axes = self.fig.add_axes([0.35, 0.01, 0.15, 0.05])
    #     self.b_scale = Button(
    #         self.scale_axes,
    #         'Масштабировать',
    #         hovercolor='white'
    #     )
    #     self.b_scale.on_clicked(self.__scale)

    # def __initRotate(self):
    #     # Поля ввода значения относительно какой точки будет производиться поворот
    #     self.input_x_rotate_axes = self.fig.add_axes([0.57, 0.12, 0.15, 0.05])
    #     self.input_x_rotate = TextBox(
    #         self.input_x_rotate_axes,
    #         ' X ',
    #         initial='0.0'
    #     )
    #     self.input_x_rotate.on_submit(self.__setX)

    #     self.input_y_rotate_axes = self.fig.add_axes([0.57, 0.065, 0.15, 0.05])
    #     self.input_y_rotate = TextBox(
    #         self.input_y_rotate_axes,
    #         ' Y ',
    #         initial='0.0'
    #     )
    #     self.input_y_rotate.on_submit(self.__setY)

    #     self.current_change = np.array([
    #         np.float64(self.input_x_rotate.text),
    #         np.float64(self.input_y_rotate.text)
    #     ])

    #     # Поле ввода значения угла поворота
    #     self.angle_axes = self.fig.add_axes([0.57, 0.01, 0.15, 0.05])
    #     self.angle_entry = TextBox(
    #         self.angle_axes,
    #         ' Angle ',
    #         initial='0'
    #     )
    #     self.angle_entry.on_submit(self.__setAngle)

    #     self.current_angle = float(self.angle_entry.text)

    #     # Кнопка вызова операции поворота
    #     self.rotate_axes = self.fig.add_axes([0.74, 0.065, 0.1, 0.05])
    #     self.b_rotate = Button(
    #         self.rotate_axes,
    #         'Повернуть',
    #         hovercolor='white'
    #     )
    #     self.b_rotate.on_clicked(self.__rotate)

    # def __initRecover(self):
    #     self.reset_axes = self.fig.add_axes([0.86, 0.065, 0.12, 0.05])
    #     self.reset_button = Button(
    #         self.reset_axes, 'Восстановить', hovercolor='green')
    #     self.reset_button.on_clicked(self.__reset)

    # def __initFigure(self):
    #     self.coords = np.copy(self.const_coords)

    # def run(self):
    #     self.__draw()
    #     plt.show()

    # def __draw(self):
    #     self.ax.clear()
    #     self.__initAxes()
    #     points = np.array(list(map(lambda x: x[:2], self.coords)))
    #     polygon = Polygon(
    #         points,
    #         fc='none',
    #         ec='black',
    #         closed=False
    #     )
    #     self.ax.add_patch(polygon)

    #     self.fig.canvas.draw()
    #     self.fig.canvas.flush_events()

    # def __reflectTypeChanger(self, label_name):
    #     if label_name == 'X':
    #         self.current_reflect_type = 'X'
    #     elif label_name == 'Y':
    #         self.current_reflect_type = 'Y'
    #     elif label_name == 'X = Y':
    #         self.current_reflect_type = 'X = Y'

    # def __reflect(self, event):
    #     if self.current_reflect_type == 'X':
    #         self.coords = scale_figure(self.coords, 1, -1)
    #     elif self.current_reflect_type == 'Y':
    #         self.coords = scale_figure(self.coords, -1, 1)
    #     elif self.current_reflect_type == 'X = Y':
    #         self.coords = xy_reflection(self.coords)
    #     self.__draw()

    def __setStartX(self, text):
        self.const_line_coords[0][0] = float(text)

    def __setStartY(self, text):
        self.const_line_coords[1][0] = float(text)

    def __setEndX(self, text):
        self.const_line_coords[0][1] = float(text)

    def __setEndY(self, text):
        self.const_line_coords[1][1] = float(text)

    def __setX(self, text):
        self.const_circle_coords[0] = float(text)

    def __setY(self, text):
        self.const_circle_coords[1] = float(text)

    def __setRadius(self, text):
        self.const_circle_coords[2] = float(text)

    # def __setAngle(self, text):
    #     self.current_angle = float(text)

    # def __shift(self, event):
    #     self.coords = shift_figure(
    #         self.coords,
    #         self.current_change[0],
    #         self.current_change[1]
    #     )
    #     self.__draw()
    #     self.__resetInputShift()

    # def __scale(self, event):
    #     self.coords = scale_figure(
    #         self.coords,
    #         self.current_change[0],
    #         self.current_change[1]
    #     )
    #     self.__draw()
    #     self.__resetInputScale()

    # def __rotate(self, event):
    #     self.coords = rotate_figure(
    #         self.coords,
    #         self.current_change[0],
    #         self.current_change[1],
    #         self.current_angle
    #     )
    #     self.__draw()

    # def __new_line(self, event):
    #     self.__initFigure()
    #     self.__draw()

    # def __bresenham(self):
    #     x1, y1, x2, y2 = self.coords[0][0], self.coords[0][1], self.coords[1][0], self.coords[1][1]
    #     points = []
    #     dx = abs(x2 - x1)
    #     dy = abs(y2 - y1)
    #     sx = 1 if x1 < x2 else -1
    #     sy = 1 if y1 < y2 else -1
    #     error = dx - dy

    #     x = x1
    #     y = y1

    #     while True:
    #         points.append((x, y))

    #         if x == x2 and y == y2:
    #             break

    #         e2 = 2 * error
    #         if e2 > -dy:
    #             error -= dy
    #             x += sx
    #         if e2 < dx:
    #             error += dx
    #             y += sy

    #     return points

    # def __raster(self, event):
    #     self.segment_points = self.__bresenham()
    #     # polygon = Polygon(
    #     #     self.segment_points,
    #     #     fc='none',
    #     #     ec='none',
    #     #     closed=False,
    #     # )
    #     # self.ax.add_patch(polygon)
    #     for vertex in self.segment_points:
    #         square = RegularPolygon(vertex, numVertices=4, radius=0.1,
    #                                 orientation=np.pi/4, edgecolor='black', facecolor='black')
    #         self.ax.add_patch(square)

    #     self.fig.canvas.draw()
    #     self.fig.canvas.flush_events()

    # def __reset(self, event):
    #     self.coords = np.copy(self.const_coords)
    #     self.__draw()
    #     self.__resetInputShift()
    #     self.__resetInputScale()
    #     self.__resetInputRotate()

    # def __resetInputShift(self):
    #     self.input_x_shift.set_val('0.0')
    #     self.input_y_shift.set_val('0.0')

    # def __resetInputScale(self):
    #     self.input_x_scale.set_val('0.0')
    #     self.input_y_scale.set_val('0.0')

    # def __resetInputRotate(self):
    #     self.input_x_rotate.set_val('0.0')
    #     self.input_y_rotate.set_val('0.0')
    #     self.angle_entry.set_val('0')


app = Rasterization()
app.run()
