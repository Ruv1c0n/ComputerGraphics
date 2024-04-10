import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from matplotlib.patches import (Polygon, Rectangle)


class Clipping:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 10))
        self.fig.canvas.manager.set_window_title('Растеризация')
        self.ax = self.fig.add_subplot()
        self.__initAxes()
        self.fig.subplots_adjust(bottom=0.2)
        self.__initUI()
        self.polygon_file = 'D:/Users/Даня/Desktop/КомпГрафика/4 лаба/polygon.txt'
        self.cyrus_beck_line_file = 'D:/Users/Даня/Desktop/КомпГрафика/4 лаба/Cyrus-Beck line.txt'
        self.cohen_sutherland_line_file = 'D:/Users/Даня/Desktop/КомпГрафика/4 лаба/Cohen-Sutherland line.txt'
        self.middle_point_line_file = 'D:/Users/Даня/Desktop/КомпГрафика/4 лаба/Middle-point line.txt'
        self.__initFigures()

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
        self.__stateText()
        self.__clippingButton()

    def __stateText(self):
        self.ax.set_title('Before clipping')

    def __clippingButton(self):
        self.b_clip_axes = self.fig.add_axes([0.05, 0.05, 0.15, 0.05])
        self.b_clip = Button(
            self.b_clip_axes,
            'Отсечь',
            hovercolor='white'
        )
        self.b_clip.on_clicked(self.__clip)

    def __initFigures(self):
        self.polygon_coords = np.genfromtxt(
            self.polygon_file, 
            delimiter=' '
        )
        self.cyrus_beck_line = np.genfromtxt(
            self.cyrus_beck_line_file, 
            delimiter=' '
        )
        self.cohen_sutherland_line = np.genfromtxt(
            self.cohen_sutherland_line_file, 
            delimiter=' '
        )
        self.middle_point_line = np.genfromtxt(
            self.middle_point_line_file, 
            delimiter=' '
        )

    def run(self):
        self.__drawFigures()
        plt.show()

    def __drawFigures(self):
        if self.polygon_coords.size / 2 > 2:
            self.__drawPolygon(rectangle=False)
            self.__drawLine(self.cyrus_beck_line)
            print('Цирус-Бек')
        elif self.polygon_coords.size / 2 < 2:
            raise ValueError("Invalid input data size")
        else:
            self.__drawPolygon(rectangle=True)
            self.__drawLine(self.cyrus_beck_line)
            self.__drawLine(self.cohen_sutherland_line)
            self.__drawLine(self.middle_point_line)
            print('3 алгоритма')

    def __drawPolygon(self, rectangle):
        if rectangle:
            xy = np.array(self.polygon_coords[0])
            width = self.polygon_coords[1][0] - self.polygon_coords[0][0]
            height = self.polygon_coords[1][1] - self.polygon_coords[0][1]
            rect = Rectangle(
                xy,
                width,
                height,
                fc='none',
                ec='black',
                lw=2
            )
            self.ax.add_patch(rect)
        else:
            points = np.array(list(map(lambda x: x[:2], self.polygon_coords)))
            polygon = Polygon(
                points,
                fc='none',
                ec='black',
                closed=True,
                lw=2
            )
            self.ax.add_patch(polygon)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __drawLine(self, line_coords, color='black'):
        x, y = np.hsplit(line_coords, 2)
        line = plt.Line2D(
            x,
            y,
            lw=2,
            color=color
        )
        self.ax.add_line(line)

    def __clip(self, event):
        self.ax.set_title('After clipping')

        self.__cyrusBeck()
        self.__drawLine(self.new_cyrus_beck_line, 'red')
        x = np.array([
            self.new_cyrus_beck_line[0][0], 
            self.new_cyrus_beck_line[1][0]
        ])
        y = np.array([
            self.new_cyrus_beck_line[0][1],
              self.new_cyrus_beck_line[1][1]
        ])
        self.ax.plot(x, y, 'ro')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __cyrusBeck(self):
        num_vert = int(self.polygon_coords.size / 2)
        P1_P0 = np.array([
            self.cyrus_beck_line[1][0] - self.cyrus_beck_line[0][0],
            self.cyrus_beck_line[1][1] - self.cyrus_beck_line[0][1]
        ])
        normal = np.array([[
            self.polygon_coords[i][1] - self.polygon_coords[(i + 1) % num_vert][1],
            self.polygon_coords[(i + 1) % num_vert][0] - self.polygon_coords[i][0]
        ] for i in range(num_vert)])
        P0_PEi = np.array([[
            self.polygon_coords[i][0] - self.cyrus_beck_line[0][0],
            self.polygon_coords[i][1] - self.cyrus_beck_line[0][1]
        ] for i in range(num_vert)])
        numerator = np.array([np.dot(normal[i], P0_PEi[i]) for i in range(num_vert)])
        denominator = np.array([np.dot(normal[i], P1_P0) for i in range(num_vert)])
        t = np.array([numerator[i] / denominator[i] if denominator[i] != 0 else 0 for i in range(num_vert)])
        Te = np.array([t[i] for i in range(num_vert) if denominator[i] > 0])
        Tl = np.array([t[i] for i in range(num_vert) if denominator[i] < 0])
        np.append(Te, 0)
        np.append(Tl, 1)
        temp = np.array([max(Te), min(Tl)])
        if temp[0] > temp[1]:
            raise Exception("Error")
            return None
        self.new_cyrus_beck_line = np.array([
            [
                self.cyrus_beck_line[0][0] + P1_P0[0] * temp[0],
                self.cyrus_beck_line[0][1] + P1_P0[1] * temp[0]
            ],
            [
                self.cyrus_beck_line[0][0] + P1_P0[0] * temp[1],
                self.cyrus_beck_line[0][1] + P1_P0[1] * temp[1]
            ]
        ])

app = Clipping()
app.run()
