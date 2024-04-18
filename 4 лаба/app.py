import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, RadioButtons, TextBox
from matplotlib.patches import Polygon


INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8
EPS = 0.0001


class Clipping:
    """
        __initAxes(self) - инициализация сетки
        __initPolygon(self) - инициализация области видимости
        __initUI(self) - инициализация элементов управления и фигуры

            __initInputLine(self) - инициализация ввода координат линии
                    __setStartX(self, text) - ввод начальной координаты X для линии
                    __setStartY(self, text) - ввод начальной координаты Y для линии
                    __setEndX(self, text) - ввод конечной координаты X для линии
                    __setEndY(self, text) - ввод конечной координаты Y для линии
            
            __initDrawButton(self) - инициализация кнопки отрисовки
                __drawLine(self, event) - рисует линию для обрезки
                __drawAnyLine(self, line_coords, color) - рисует линию

            __initClippingButton(self) - инициализация кнопки обрезки
                __clip(self, event) - запуск алгоритма обрезки

                    __clipCyrusBeck(self) - запуск алгоритма Цируса-Бэка
                        __cyrusBeck(self) - алгоритм Цируса-Бэка

                    __clipCohenSutherland(self) - запуск алгоритма Сазерлэнда-Коэна
                        __cohenSutherland(self) - алгоритм Сазерлэнда-Коэна
                            __calculateCode(self, point) - подсчет код точки
                            
                    __clipMidlePoint(self) - запуск алгоритма средней точки
                        __midlePoint(self, prev_line) - алгоритм средней точки

            __initChoosingLineType(self) - инициализация выбора алгоритма обрезки
                __choosingAlgorithm(self, label_name) - выбирает алгоритм обрезки
                    __drawFigures(self) - рисует область и линию для обрезки

        __drawPolygon(self) - отрисовка области видимости
        
        run(self) - запуск работы класса
    """
    def __init__(self):
        self.fig = plt.figure(figsize=(9, 9))
        self.fig.canvas.manager.set_window_title('Clipping line')
        self.ax = self.fig.add_subplot()
        self.__initAxes()
        self.fig.subplots_adjust(bottom=0.2)
        self.polygon_file = 'C:/Users/User/PycharmProjects/-----------/4 лаба/polygon.txt'
        self.__initPolygon()
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
        self.ax.set_title('Before clipping')
        self.__initInputLine()
        self.__initDrawButton()
        self.__initClippingButton()
        if self.rectangle:
            self.__initChoosingLineType()

    def __initInputLine(self):
        self.s_x_axes = self.fig.add_axes([0.1, 0.05, 0.05, 0.05])
        self.input_s_x = TextBox(
            self.s_x_axes,
            'Start X ',
            initial='0.0'
        )
        self.input_s_x.on_submit(self.__setStartX)

        self.s_y_axes = self.fig.add_axes([0.208, 0.05, 0.05, 0.05])
        self.input_s_y = TextBox(
            self.s_y_axes,
            'Start Y ',
            initial='0.0'
        )
        self.input_s_y.on_submit(self.__setStartY)

        self.e_x_axes = self.fig.add_axes([0.308, 0.05, 0.05, 0.05])
        self.input_e_x = TextBox(
            self.e_x_axes,
            'End X ',
            initial='0.0'
        )
        self.input_e_x.on_submit(self.__setEndX)

        self.e_y_axes = self.fig.add_axes([0.408, 0.05, 0.05, 0.05])
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

    def __initDrawButton(self):
        self.draw_axes = self.fig.add_axes([0.7, 0.05, 0.1, 0.05])
        self.b_draw = Button(
            self.draw_axes,
            'Draw line',
            hovercolor='white'
        )
        self.b_draw.on_clicked(self.__drawLine)

    def __initClippingButton(self):
        self.b_clip_axes = self.fig.add_axes([0.82, 0.05, 0.15, 0.05])
        self.b_clip = Button(
            self.b_clip_axes,
            'Clip',
            hovercolor='white'
        )
        self.b_clip.on_clicked(self.__clip)

    def __initChoosingLineType(self):
        clipping_line_type = ['Cyrus-Beck', 'Cohen-Sutherland', 'Midle-point']
        self.choose_clipping_line_type_axes = self.fig.add_axes(
            [0.48, 0.05, 0.2, 0.08],
            facecolor='#d9d9d9'
        )
        self.rbs_clipping_line_type = RadioButtons(
            self.choose_clipping_line_type_axes,
            clipping_line_type,
            radio_props={'s': [64, 64, 64]},
            activecolor='black',
        )
        self.rbs_clipping_line_type.on_clicked(self.__choosingAlgorithm)

        self.current_clipping_line_type = clipping_line_type[0]

    def __initPolygon(self):
        self.rectangle = False
        self.polygon_coords = np.genfromtxt(
            self.polygon_file,
            delimiter=' '
        )
        # Многоугольник
        if self.polygon_coords.size / 2 > 2:
            self.rectangle = False
        elif self.polygon_coords.size / 2 < 2:
            raise ValueError("Invalid input data size")
        # Прямоугольник
        else:
            self.rectangle = True
            self.min_x, self.min_y = self.polygon_coords[0]
            self.max_x, self.max_y = self.polygon_coords[1]

    def run(self):
        self.__drawPolygon()
        plt.show()

    def __drawPolygon(self):
        if self.rectangle and self.polygon_coords.size == 4:
            self.polygon_coords = np.array([
                [
                    self.polygon_coords[0][0],
                    self.polygon_coords[0][1]
                ],
                [
                    self.polygon_coords[1][0],
                    self.polygon_coords[0][1]
                ],
                [
                    self.polygon_coords[1][0],
                    self.polygon_coords[1][1]
                ],
                [
                    self.polygon_coords[0][0],
                    self.polygon_coords[1][1]
                ]
            ])
            self
        points = np.array(list(map(lambda x: x[:2], self.polygon_coords)))
        polygon = Polygon(
            points,
            fc='none',
            ec='black',
            closed=True,
            lw=2
        )
        self.ax.add_patch(polygon)

    def __drawLine(self, event):
        self.ax.clear()
        self.__initAxes()

        self.ax.set_title('Before clipping')
        self.__drawPolygon()
        self.__drawAnyLine(self.const_line_coords)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __drawAnyLine(self, line_coords, color='black'):
        x, y = np.hsplit(line_coords, 2)
        line = plt.Line2D(
            x,
            y,
            lw=2,
            color=color
        )
        self.ax.add_line(line)

    def __choosingAlgorithm(self, label_name):
        self.ax.clear()
        self.__initAxes()
        self.ax.set_title('Before clipping')

        if label_name == 'Cyrus-Beck':
            self.current_clipping_line_type = 'Cyrus-Beck'
        elif label_name == 'Cohen-Sutherland':
            self.current_clipping_line_type = 'Cohen-Sutherland'
        elif label_name == 'Midle-point':
            self.current_clipping_line_type = 'Midle-point'

        self.__drawFigures()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __drawFigures(self):
        self.__drawPolygon()
        self.__drawAnyLine(self.const_line_coords)

    def __clip(self, event):
        self.ax.set_title('After clipping')
        if self.rectangle:
            if self.current_clipping_line_type == 'Cyrus-Beck':
                self.__clipCyrusBeck()
            elif self.current_clipping_line_type == 'Cohen-Sutherland':
                self.__clipCohenSutherland()
            elif self.current_clipping_line_type == 'Midle-point':
                self.__clipMidlePoint()
        else:
            self.__clipCyrusBeck()

    def __clipCyrusBeck(self):
        self.clipped_cyrus_beck_line = self.__cyrusBeck()
        if self.clipped_cyrus_beck_line is not None:
            self.__drawAnyLine(self.clipped_cyrus_beck_line, '#7fffd4')
        
        # Рисуем потеницальные точки входа и выхода
        for point in self.intersections_in:
            self.ax.plot(point[0], point[1], 'ro')
        for point in self.intersections_out:
            self.ax.plot(point[0], point[1], 'bo')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __cyrusBeck(self):
        num_vert = int(self.polygon_coords.size / 2)

        P1_P0 = np.array([
            self.const_line_coords[1][0] - self.const_line_coords[0][0],
            self.const_line_coords[1][1] - self.const_line_coords[0][1]
        ])
        
        normal = np.array([[
            self.polygon_coords[i][1] -
            self.polygon_coords[(i + 1) % num_vert][1],
            self.polygon_coords[(i + 1) % num_vert][0] -
            self.polygon_coords[i][0]
        ] for i in range(num_vert)])

        P0_PEi = np.array([[
            self.polygon_coords[i][0] - self.const_line_coords[0][0],
            self.polygon_coords[i][1] - self.const_line_coords[0][1]
        ] for i in range(num_vert)])

        numerator = np.array([np.dot(normal[i], P0_PEi[i])
                             for i in range(num_vert)])
        denominator = np.array([np.dot(normal[i], P1_P0)
                               for i in range(num_vert)])
        
        t = np.array([numerator[i] / denominator[i]
                     if denominator[i] != 0 else 0 for i in range(num_vert)])

        Te = np.array([t[i] for i in range(num_vert) if denominator[i] > 0])
        Tl = np.array([t[i] for i in range(num_vert) if denominator[i] < 0])

        self.intersections_in = np.array([
            (
                self.const_line_coords[0][0] + P1_P0[0] * Te[i],
                self.const_line_coords[0][1] + P1_P0[1] * Te[i]
            ) for i in range(Te.size)
        ])
        self.intersections_out = np.array([
            (
                self.const_line_coords[0][0] + P1_P0[0] * Tl[i],
                self.const_line_coords[0][1] + P1_P0[1] * Tl[i]
            ) for i in range(Tl.size)
        ])

        for i in range(num_vert):
            if 0 == denominator[i]:
                if 0 < numerator[i]:
                    return None
                
        Te = np.array([*Te, 0.0])
        Tl = np.array([*Tl, 1.0])

        temp = np.array([max(Te), min(Tl)])

        if temp[0] > temp[1]:
            return None
        
        self.clipped_cyrus_beck_line = np.array([
            [
                self.const_line_coords[0][0] + P1_P0[0] * temp[0],
                self.const_line_coords[0][1] + P1_P0[1] * temp[0]
            ],
            [
                self.const_line_coords[0][0] + P1_P0[0] * temp[1],
                self.const_line_coords[0][1] + P1_P0[1] * temp[1]
            ]
        ])

        return self.clipped_cyrus_beck_line

    def __clipCohenSutherland(self):
        self.clipped_cohen_sutherland_line = self.__cohenSutherland()
        if self.clipped_cohen_sutherland_line is not None:
            self.__drawAnyLine(self.clipped_cohen_sutherland_line, '#7fffd4')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __calculateCode(self, point):
        code = INSIDE
        if point[0] < self.min_x:
            code |= LEFT
        if point[0] > self.max_x:
            code |= RIGHT
        if point[1] < self.min_y:
            code |= BOTTOM
        if point[1] > self.max_y:
            code |= TOP
        return code

    def __cohenSutherland(self):
        line = np.copy(self.const_line_coords)
        code0 = self.__calculateCode(line[0])
        code1 = self.__calculateCode(line[1])
        accept = False

        while True:
            if code0 == 0 and code1 == 0:
                accept = True
                break
            elif (code0 & code1) != 0:
                break
            else:
                x = 1.0
                y = 1.0
                if code0 != 0:
                    code_out = code0
                else:
                    code_out = code1
                if code_out & TOP:
                    x = line[0][0] + (
                        (line[1][0] - line[0][0]) 
                        * 
                        (self.max_y - line[0][1])
                        / 
                        (line[1][1] - line[0][1])
                    )
                    y = self.max_y
                elif code_out & BOTTOM:
                    x = line[0][0] + (
                        (line[1][0] - line[0][0]) 
                        * 
                        (self.min_y - line[0][1])
                        / 
                        (line[1][1] - line[0][1])
                    )
                    y = self.min_y
                elif code_out & RIGHT:
                    y = line[0][1] + (
                        (line[1][1] - line[0][1]) 
                        * 
                        (self.max_x - line[0][0])
                        / 
                        (line[1][0] - line[0][0])
                    )
                    x = self.max_x
                elif code_out & LEFT:
                    y = line[0][1] + (
                        (line[1][1] - line[0][1]) 
                        * 
                        (self.min_y - line[0][0])
                        / 
                        (line[1][0] - line[0][0])
                    )
                    x = self.min_y

                if code_out == code0:
                    line[0][0] = x
                    line[0][1] = y
                    code0 = self.__calculateCode(line[0])
                else:
                    line[1][0] = x
                    line[1][1] = y
                    code1 = self.__calculateCode(line[1])
            self.ax.plot((line[0][0], line[1][0]), (line[0][1], line[1][1]), 'ro')

        if accept:
            return line
    
    def __clipMidlePoint(self):
        self.__midlePoint(self.const_line_coords)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __midlePoint(self, prev_line):
        line = np.copy(prev_line)
        code0 = self.__calculateCode(line[0])
        code1 = self.__calculateCode(line[1])
        # Если длина отрезка меньше пикселя, то не рассматриваем его
        if np.sqrt(
            np.square(line[0][0] - line[1][0])
            +
            np.square(line[0][1] - line[1][1])
        ) < EPS:
            return

        # Если отрезок целиком внутри области, то отрисовываем его
        if (
            code0 | code1
        ) == INSIDE:
            self.ax.plot((line[0][0], line[1][0]), (line[0][1], line[1][1]), 'ro')
            self.__drawAnyLine(line, '#7fffd4')
            return
        
        # Если отрезок целиком вне области, то не рассматриваем его
        if code0 == code1:
            return

        A = line[0]
        B = line[1]
        new_x = ((A[0] + B[0]) / 2)
        new_y = ((A[1] + B[1]) / 2)

        # Делим отрезок на две части и используем алгоритм для этих частей
        self.__midlePoint(np.array([
            A,
            [
                new_x,
                new_y
            ]
        ]))
        self.__midlePoint(np.array([
            [
                new_x,
                new_y
            ], 
            B
        ]))

    def __setStartX(self, text):
        self.const_line_coords[0][0] = float(text)

    def __setStartY(self, text):
        self.const_line_coords[0][1] = float(text)

    def __setEndX(self, text):
        self.const_line_coords[1][0] = float(text)

    def __setEndY(self, text):
        self.const_line_coords[1][1] = float(text)


app = Clipping()
app.run()
