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

            __initChoosingShape(self) - инициализация выбора фигуры
                __choosingShape(self, label_name) - меняет фигуру
                    __setVisibleUI(self, type) - показывает UI для выбранной фигуры

            __initInputLine(self) - инициализация ввода координат линии
                __setStartX(self, text) - ввод начальной координаты X для линии
                __setStartY(self, text) - ввод начальной координаты Y для линии
                __setEndX(self, text) - ввод конечной координаты X для линии
                __setEndY(self, text) - ввод конечной координаты Y для линии

            __initInputCircle(self) - инициализация ввода координат и радиуса окружности
                __setX(self, text) - ввод координаты X для центра окружности
                __setY(self, text) - ввод координаты Y для центра окружности
                __setRadius(self, text) - ввод радиуса окружности

            __initDrawButton(self) - инициализация кнопки отрисовки
                __drawFigure(self, event, normalized) - запуск отрисовки фигуры
                    __drawLine(self) - рисует ненормализованную линию
                    __drawCircle(self) - рисует ненормализованную окружность

            __initNormalization(self) - инициализация кнопки нормализации
                __normalize(self, event) - запуск нормализации фигуры
                    __normalizeLine(self) - нормализует линию
                    __normalizeCircle(self) - нормализует окружность

            __initRasterization(self) - инициализация кнопки растрезации
                __rasterize(self, event) - запуск растеризации фигуры
                    __rasterizeLine(self) - растеризует линию
                        __line_bresenham(self) - алгоритм Бразенхама для линии
                    __rasterizeCircle(self) - растеризует окружность
                        __circle_bresenham(self) - алгоритм Бразенхама для окружности

            __initReturn(self) - инициализация кнопки, которая возвращает фигуру и растеризованную фигуру в исходную позицию
                __return(self, event) - запуск возврата фигуры к исходному положению
                    __returnLine(self) - возвращает линию к исходной позиции
                    __returnCircle(self) - возвращает окружность к исходной позиции
                    
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
        self.__initDrawButton()
        self.__initNormalization()
        self.__initRasterization()
        self.__initReturn()

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
        self.input_s_x.on_submit(self.__setStartX)

        self.s_y_axes = self.fig.add_axes([0.25, 0.9, 0.05, 0.05])
        self.input_s_y = TextBox(
            self.s_y_axes,
            'Start Y ',
            initial='0.0'
        )
        self.input_s_y.on_submit(self.__setStartY)

        self.e_x_axes = self.fig.add_axes([0.35, 0.9, 0.05, 0.05])
        self.input_e_x = TextBox(
            self.e_x_axes,
            'End X ',
            initial='0.0'
        )
        self.input_e_x.on_submit(self.__setEndX)

        self.e_y_axes = self.fig.add_axes([0.45, 0.9, 0.05, 0.05])
        self.input_e_y = TextBox(
            self.e_y_axes,
            'End Y ',
            initial='0.0'
        )
        self.input_e_y.on_submit(self.__setEndY)

        self.const_line_coords = np.array([
            [
                np.float64(self.input_s_x.text),
                np.float64(self.input_s_y.text)
            ],
            [
                np.float64(self.input_e_x.text),
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
        self.input_x.on_submit(self.__setX)

        self.y_axes = self.fig.add_axes([0.23, 0.9, 0.05, 0.05])
        self.input_y = TextBox(
            self.y_axes,
            'Y ',
            initial='0.0'
        )
        self.input_y.on_submit(self.__setY)

        self.r_axes = self.fig.add_axes([0.34, 0.9, 0.05, 0.05])
        self.input_r = TextBox(
            self.r_axes,
            'Radius ',
            initial='0.0'
        )
        self.input_r.on_submit(self.__setRadius)

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

    def __initNormalization(self):
        self.norm_axes = self.fig.add_axes([0.05, 0.05, 0.15, 0.05])
        self.b_norm = Button(
            self.norm_axes,
            'Нормализовать',
            hovercolor='white'
        )
        self.b_norm.on_clicked(self.__normalize)

    def __initRasterization(self):
        self.raster_axes = self.fig.add_axes([0.25, 0.05, 0.15, 0.05])
        self.b_raster = Button(
            self.raster_axes,
            'Растеризировать',
            hovercolor='white'
        )
        self.b_raster.on_clicked(self.__rasterize)

    def __initReturn(self):
        self.return_axes = self.fig.add_axes([0.45, 0.05, 0.15, 0.05])
        self.b_return = Button(
            self.return_axes,
            'Вернуть',
            hovercolor='white'
        )
        self.b_return.on_clicked(self.__return)

    def run(self):
        plt.show()

    def __choosingShape(self, label_name):
        self.ax.clear()
        self.__initAxes()

        if label_name == 'Line':
            self.current_figure_type = 'Line'
            self.__setVisibleUI('Line')
        elif label_name == 'Circle':
            self.current_figure_type = 'Circle'
            self.__setVisibleUI('Circle')

    def __setVisibleUI(self, type):
        if type == 'Line':
            self.x_axes.axis('off')
            self.y_axes.axis('off')
            self.r_axes.axis('off')
            self.input_x.active = False
            self.input_y.active = False
            self.input_r.active = False
            self.x_axes.set_visible(False)
            self.y_axes.set_visible(False)
            self.r_axes.set_visible(False)
            self.__initInputLine()
        elif type == 'Circle':
            self.s_x_axes.axis('off')
            self.s_y_axes.axis('off')
            self.e_x_axes.axis('off')
            self.e_y_axes.axis('off')
            self.input_s_x.active = False
            self.input_s_y.active = False
            self.input_e_x.active = False
            self.input_e_y.active = False
            self.s_x_axes.set_visible(False)
            self.s_y_axes.set_visible(False)
            self.e_x_axes.set_visible(False)
            self.e_y_axes.set_visible(False)
            self.__initInputCircle()
        self.fig.canvas.draw()

    def __drawFigure(self, event, normalized=False):
        self.ax.clear()
        self.__initAxes()

        if self.current_figure_type == 'Line':
            self.coords = np.copy(
                self.const_line_coords
            ) if not normalized else self.coords
            self.__drawLine()
        elif self.current_figure_type == 'Circle':
            self.coords = np.copy(
                self.const_circle_coords
            ) if not normalized else self.coords
            self.__drawCircle()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __drawLine(self):
        x, y = np.hsplit(self.coords, 2)
        line = plt.Line2D(
            x,
            y,
            lw=2,
            color='black'
        )
        self.ax.add_line(line)

    def __drawCircle(self):
        circle = Circle(
            self.coords,
            self.coords[2],
            fc='none',
            ec='black',
            lw=2
        )
        self.ax.add_patch(circle)

    def __normalize(self, event):
        if self.current_figure_type == 'Line':
            self.__normalizeLine()
        elif self.current_figure_type == 'Circle':
            self.__normalizeCircle()

        self.__drawFigure('', True)

    def __normalizeLine(self):
        shift = np.array([-self.coords[0][0], -self.coords[0][1]])
        shift_figure(self.coords, *shift)

        if self.coords[1][1] < 0:
            self.coords = scale_figure(self.coords, 1, -1)
        if self.coords[1][0] < 0:
            self.coords = scale_figure(self.coords, -1, 1)
        if np.abs(self.coords[1][0]) < np.abs(self.coords[1][1]):
            self.coords = xy_reflection(self.coords)

    def __normalizeCircle(self):
        self.coords[0] += -self.coords[0]
        self.coords[1] += -self.coords[1]

    def __rasterize(self, event):
        if self.current_figure_type == 'Line':
            self.__rasterizeLine()
        elif self.current_figure_type == 'Circle':
            self.__rasterizeCircle()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __rasterizeLine(self):
        self.raster_line = np.array(self.__line_bresenham())
        x, y = np.hsplit(self.raster_line, 2)
        self.ax.plot(
            x, 
            y, 
            marker='s', 
            markersize=29, 
            linewidth=0, 
            color='grey'
        )

    def __rasterizeCircle(self):
        self.raster_circle = np.array(self.__circle_bresenham())
        self.raster_circle = np.concatenate([
            self.raster_circle, 
            xy_reflection(self.raster_circle)
        ])
        self.raster_circle = np.concatenate([
            self.raster_circle, 
            scale_figure(self.raster_circle, 1, -1)
        ])
        self.raster_circle = np.concatenate([
            self.raster_circle, 
            scale_figure(self.raster_circle, -1, 1)
        ])

        x, y = np.hsplit(self.raster_circle, 2)
        self.ax.plot(
            x, 
            y, 
            marker='s', 
            markersize=29, 
            linewidth=0, 
            color='grey'
        )

    def __return(self, event):
        if self.current_figure_type == 'Line':
            self.__returnLine()
        elif self.current_figure_type == 'Circle':
            self.__returnCircle()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __returnLine(self):
        self.coords = np.copy(self.const_line_coords)
        self.__drawFigure('')

        if np.abs(self.coords[1][0]) < np.abs(self.coords[1][1]):
            self.raster_line = xy_reflection(self.raster_line)
        if self.coords[1][0] < 0:
            self.raster_line = scale_figure(self.raster_line, -1, 1)
        if self.coords[1][1] < 0:
            self.raster_line = scale_figure(self.raster_line, 1, -1)

        shift = np.array([self.coords[0][0], self.coords[0][1]])
        self.raster_line = shift_figure(self.raster_line, *shift)

        x, y = np.hsplit(self.raster_line, 2)
        self.ax.plot(
            x, 
            y, 
            marker='s', 
            markersize=29,
            linewidth=0, 
            color='grey'
        )

    def __returnCircle(self):
        self.coords = np.copy(self.const_circle_coords)
        self.__drawFigure('')

        shift = np.array([self.coords[0], self.coords[1]])
        self.raster_circle = shift_figure(self.raster_circle, *shift)

        x, y = np.hsplit(self.raster_circle, 2)
        self.ax.plot(
            x, 
            y, 
            marker='s', 
            markersize=29,
            linewidth=0, 
            color='grey'
        )

    def __line_bresenham(self):
        x1, y1, x2, y2 = self.coords[0][0], self.coords[0][1], self.coords[1][0], self.coords[1][1]
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        error = 2 * dy - dx
        x, y = 0, 0

        points = []

        for i in range(int(x2) + 1):
            points.append([x, y])
            if error > 0:
                y += 1
                error -= 2 * dx
            x += 1
            error += 2 * dy

        return points

    def __circle_bresenham(self):
        r = self.coords[2]
        x = 0
        y = r
        delta = (x + 1) * (x + 1) + (y - 1) * (y - 1) - r * r
        points = []

        while x <= y:
            points.append([x, y])

            if delta == 0:
                x += 1
                y -= 1
            elif delta < 0:
                sigma = abs((x + 1) * (x + 1) + y * y - r * r) - abs((x + 1) * (x + 1) + (y - 1) * (y - 1) - r * r)
                if sigma >= 0:
                    x += 1
                    y -= 1
                else:
                    x += 1
            else:
                sigma = abs((x + 1) * (x + 1) + (y - 1) * (y - 1) - r * r) - abs(x * x + (y - 1) * (y - 1) - r * r)
                if sigma >= 0:
                    x += 1
                    y -= 1
                else:
                    y -= 1
        return points

    def __setStartX(self, text):
        self.const_line_coords[0][0] = float(text)

    def __setStartY(self, text):
        self.const_line_coords[0][1] = float(text)

    def __setEndX(self, text):
        self.const_line_coords[1][0] = float(text)

    def __setEndY(self, text):
        self.const_line_coords[1][1] = float(text)

    def __setX(self, text):
        self.const_circle_coords[0] = float(text)

    def __setY(self, text):
        self.const_circle_coords[1] = float(text)

    def __setRadius(self, text):
        self.const_circle_coords[2] = float(text)


app = Rasterization()
app.run()
