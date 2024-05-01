import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, TextBox
from matplotlib.patches import Polygon
from time import sleep


class Filling:
    def __init__(self):
        self.fig = plt.figure(figsize=(9, 9))
        self.fig.canvas.manager.set_window_title('Filling polygon')
        self.ax = self.fig.add_subplot()
        self.__initAxes()
        self.fig.subplots_adjust(bottom=0.2)
        self.polygon_file = 'D:/Users/Даня/Desktop/КомпГрафика/5 лаба/polygon.txt'
        self.__initPolygon()
        self.__initUI()
        self.__initPolygon()

    def __initAxes(self):
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set(
            xlim=(-5, 80),
            xticks=np.arange(-5, 80, 1),
            ylim=(-5, 80),
            yticks=np.arange(-5, 80, 1)
        )
        self.ax.grid(True)

    def __initPolygon(self):
        self.polygon_coords = np.genfromtxt(
            self.polygon_file,
            delimiter=' '
        )

    def __initUI(self):
        self.__initInputPolygon()
        self.__initAddButton()
        self.__initBackButton()
        self.__initDrawButton()
        self.__initClearButton()

    def __initInputPolygon(self):
        self.input_x_axes = self.fig.add_axes([0.05, 0.05, 0.15, 0.05])
        self.input_x = TextBox(
            self.input_x_axes,
            ' X ',
            initial='0'
        )
        self.input_x.on_submit(self.__setX)

        self.input_y_axes = self.fig.add_axes([0.25, 0.05, 0.15, 0.05])
        self.input_y = TextBox(
            self.input_y_axes,
            ' Y ',
            initial='0'
        )
        self.input_y.on_submit(self.__setY)

        self.point = np.array([
            np.float64(self.input_x.text),
            np.float64(self.input_y.text)
        ])

    def __initAddButton(self):
        self.add_point_axes = self.fig.add_axes([0.45, 0.05, 0.15, 0.05])
        self.b_add_point = Button(
            self.add_point_axes,
            'Add point',
            hovercolor='white'
        )
        self.b_add_point.label.set_fontsize(14)
        self.b_add_point.on_clicked(self.__addPoint)

        self.polygon_coords = np.append(
            self.polygon_coords,
            [self.point],
            axis=0
        )

    def __initBackButton(self):
        self.back_axes = self.fig.add_axes([0.62, 0.05, 0.1, 0.05])
        self.b_back = Button(
            self.back_axes,
            'Back',
            hovercolor='white'
        )
        self.b_back.label.set_fontsize(14)
        self.b_back.on_clicked(self.__back)

    def __initDrawButton(self):
        self.draw_axes = self.fig.add_axes([0.74, 0.05, 0.1, 0.05])
        self.b_draw = Button(
            self.draw_axes,
            'Fill',
            hovercolor='white'
        )
        self.b_draw.label.set_fontsize(14)
        self.b_draw.on_clicked(self.__draw)

    def __initClearButton(self):
        self.clear_axes = self.fig.add_axes([0.86, 0.05, 0.1, 0.05])
        self.b_clear = Button(
            self.clear_axes,
            'Clear',
            hovercolor='white'
        )
        self.b_clear.label.set_fontsize(14)
        self.b_clear.on_clicked(self.__clear)


    def run(self):
        self.__drawPolygon()
        plt.show()

    def __drawPolygon(self):
        self.ax.clear()
        self.__initAxes()

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

    def __setX(self, text):
        self.point[0] = float(text)

    def __setY(self, text):
        self.point[1] = float(text)

    def __addPoint(self, event):
        self.polygon_coords = np.append(
            self.polygon_coords,
            [self.point],
            axis=0
        )
        self.__drawPolygon()

    def __back(self, event):
        self.polygon_coords = np.delete(
            self.polygon_coords,
            len(self.polygon_coords) - 1,
            0
        )
        self.__drawPolygon()

    def __clear(self, event):
        self.polygon_coords = np.empty(shape=[0, 2])
        self.ax.clear()
        self.__initAxes()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __draw(self, event):
        self.max_x, self.min_x = self.polygon_coords[0][0], self.polygon_coords[0][0]
        self.max_y, self.min_y = self.polygon_coords[0][1], self.polygon_coords[0][1]

        for point in self.polygon_coords:
            if point[0] > self.max_x:
                self.max_x = point[0]
            if point[1] > self.max_y:
                self.max_y = point[1]
            if point[0] < self.min_x:
                self.min_x = point[0]
            if point[1] < self.min_y:
                self.min_y = point[1]
        coords = np.copy(self.polygon_coords)
        flag = False
        for i in range(len(coords)):
            if flag:
                flag = False
            elif coords[i - 1][1] >= coords[i][1] and \
               coords[i + 1][1] <= coords[i][1] or \
               coords[i - 1][1] <= coords[i][1] and \
               coords[i + 1][1] >= coords[i][1]:
                coords = np.insert(coords, i, [coords[i][0], coords[i][1]], axis=0)
                flag = True
        if coords[len(coords) - 2][1] >= coords[len(coords) - 1][1] and \
           coords[0][1] <= coords[len(coords) - 1][1] or \
           coords[len(coords) - 2][1] <= coords[len(coords) - 1][1] and \
           coords[0][1] >= coords[len(coords) - 1][1]:
            coords = np.insert(
                coords, 
                len(coords) - 1, 
                [coords[len(coords) - 1][0], coords[len(coords) - 1][1]],
                axis=0
            )
        self.border = np.empty((0, 2))

        self.area = np.empty((100, 100))
        for x in range(100):
            for y in range(100):
                self.area[x][y] = False

        self.__rasterize(coords)
        self.__invertLineArea()
        points = np.array(list(map(lambda x: x[:2], self.polygon_coords)))
        polygon = Polygon(
            points,
            fc='none',
            ec='black',
            closed=True,
            lw=10
        )
        self.ax.add_patch(polygon)
        # for point in self.border:
        #     self.ax.scatter(point[0], point[1], s=100, marker='o', c='green')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __rasterize(self, coords):
        for i in range(len(coords) - 1):
            temp = self.bresenham_line(
                coords[i][0],
                coords[i][1],
                coords[i + 1][0],
                coords[i + 1][1]
            )
            # for point in temp:
            #     self.ax.scatter(point[0], point[1], s=100, marker='o', c='green')
            self.border = np.append(
                self.border,
                temp,
                axis=0
            )

        # uniq, index = np.unique(self.border, return_index=True, axis=0)
        # self.border = uniq[index.argsort()]
        temp = self.bresenham_line(
            coords[-1][0],
            coords[-1][1],
            coords[0][0],
            coords[0][1]
        )
        # for point in temp:
        #     self.ax.scatter(point[0], point[1], s=100, marker='o', c='green')
        self.border = np.append(
            self.border,
            temp,
            axis=0
        )

        # for i in range(len(coords)):
        #     dx = coords[i + 1 if i < len(coords) - 1 else 0][0] - coords[i][0]
        #     dy = coords[i + 1 if i < len(coords) - 1 else 0][1] - coords[i][1]

        #     if dx >= dy and dx >= 0 and dy >= 0:
        #         x = coords[i][0]
        #         y = coords[i][1]
        #         self.border = np.append(self.border, [[x, y]], axis=0)

        #         # self.ax.scatter(x, y, s=100, marker='o', c='green')
        #         # self.fig.canvas.draw()
        #         # self.fig.canvas.flush_events()

        #         self.area[int(x)][int(y)] = True
        #         self.__RightUp(x, y, dx, dy)
        #     elif dy >= dx and dx >= 0 and dy >= 0:
        #         x = coords[i][0]
        #         y = coords[i][1]
        #         self.border = np.append(self.border, [[x, y]], axis=0)

        #         # self.ax.scatter(x, y, s=100, marker='o', c='green')
        #         # self.fig.canvas.draw()
        #         # self.fig.canvas.flush_events()


        #         self.area[int(x)][int(y)] = True
        #         self.__RightUpper(x, y, dx, dy)
        #     elif dx >= np.abs(dy) and dx >= 0 and dy <= 0:
        #         x = coords[i][0]
        #         y = coords[i][1]
        #         dy = np.abs(dy)
        #         self.border = np.append(self.border, [[x, y]], axis=0)

        #         # self.ax.scatter(x, y, s=100, marker='o', c='green')
        #         # self.fig.canvas.draw()
        #         # self.fig.canvas.flush_events()


        #         self.area[int(x)][int(y)] = True
        #         self.__RightDown(x, y, dx, dy)
        #     elif np.abs(dy) >= dx and dx >= 0 and dy <= 0:
        #         x = coords[i][0]
        #         y = coords[i][1]
        #         dy = np.abs(dy)
        #         self.border = np.append(self.border, [[x, y]], axis=0)

        #         # self.ax.scatter(x, y, s=100, marker='o', c='green')
        #         # self.fig.canvas.draw()
        #         # self.fig.canvas.flush_events()


        #         self.area[int(x)][int(y)] = True
        #         self.__RightDowner(x, y, dx, dy)
        #     elif np.abs(dx) >= np.abs(dy) and dx <= 0 and dy <= 0:
        #         x = coords[i + 1 if i < len(coords) - 1 else 0][0]
        #         y = coords[i + 1 if i < len(coords) - 1 else 0][1]
        #         dx = np.abs(dx)
        #         dy = np.abs(dy)
        #         self.border = np.append(self.border, [[x, y]], axis=0)

        #         # self.ax.scatter(x, y, s=100, marker='o', c='green')
        #         # self.fig.canvas.draw()
        #         # self.fig.canvas.flush_events()


        #         self.area[int(x)][int(y)] = True
        #         self.__RightUp(x, y, dx, dy)
        #     elif np.abs(dy) >= np.abs(dx) and dx <= 0 and dy <= 0:
        #         x = coords[i + 1 if i < len(coords) - 1 else 0][0]
        #         y = coords[i + 1 if i < len(coords) - 1 else 0][1]
        #         dx = np.abs(dx)
        #         dy = np.abs(dy)
        #         self.border = np.append(self.border, [[x, y]], axis=0)

        #         # self.ax.scatter(x, y, s=100, marker='o', c='green')
        #         # self.fig.canvas.draw()
        #         # self.fig.canvas.flush_events()


        #         self.area[int(x)][int(y)] = 1
        #         self.__RightUpper(x, y, dx, dy)
        #     elif np.abs(dx) >= dy and dx <= 0 and dy >= 0:
        #         x = coords[i + 1 if i < len(coords) - 1 else 0][0]
        #         y = coords[i + 1 if i < len(coords) - 1 else 0][1]
        #         dx = np.abs(dx)
        #         self.border = np.append(self.border, [[x, y]], axis=0)

        #         # self.ax.scatter(x, y, s=100, marker='o', c='green')
        #         # self.fig.canvas.draw()
        #         # self.fig.canvas.flush_events()


        #         self.area[int(x)][int(y)] = True
        #         self.__RightDown(x, y, dx, dy)
        #     elif dy >= np.abs(dx) and dx <= 0 and dy >= 0:
        #         x = coords[i + 1 if i < len(coords) - 1 else 0][0]
        #         y = coords[i + 1 if i < len(coords) - 1 else 0][1]
        #         dx = np.abs(dx)
        #         self.border = np.append(self.border, [[x, y]], axis=0)

        #         # self.ax.scatter(x, y, s=100, marker='o', c='green')
        #         # self.fig.canvas.draw()
        #         # self.fig.canvas.flush_events()


        #         self.area[int(x)][int(y)] = True
        #         self.__RightDowner(x, y, dx, dy)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # uniq, index = np.unique(self.border, return_index=True, axis=0)
        # self.border = uniq[index.argsort()]

    def bresenham_line(self, x0, y0, x1, y1) -> list:
        pixels = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        slope = dy > dx
        if slope:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = abs(y1 - y0)
        error = int(dx / 2.0)
        ystep = 1 if y0 < y1 else -1
        y = y0
        for x in range(int(x0), int(x1 + 1)):
            coord = [y, x] if slope else [x, y]
            if not pixels or coord[1] != pixels[len(pixels) - 1][1]:
                pixels.append(coord)
            error -= dy
            if error < 0:
                y += ystep
                error += dx
        return pixels

    def __invertLineArea(self):
        for i in range(len(self.border)):
            y = int(self.border[i][1])
            if (self.border[i][0] < (self.min_x + self.max_x) / 2):
                for x in range(int(self.border[i][0]), int((self.min_x + self.max_x) / 2)):
                    self.area[x][y] = not self.area[x][y]
                    if self.area[x][y]:
                        self.ax.scatter(x, y, s=49, marker='o', c='red')
                    else:
                        self.ax.scatter(x, y, s=50, marker='o', c='white')

            else:
                for x in range(int((self.min_x + self.max_x) / 2), int(self.border[i][0]) + 1):
                    self.area[x][y] = not self.area[x][y]
                    if self.area[x][y]:
                        self.ax.scatter(x, y, s=49, marker='o', c='red')
                    else:
                        self.ax.scatter(x, y, s=50, marker='o', c='white')
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    def __RightUp(self, x, y, dx, dy):
        delta = 2 * dy - dx
        increment_horizontal = 2 * dy
        increment_diagonal = 2 * (dy - dx)
        for i in range(int(dx)):
            if delta > 0:
                y += 1
                x += 1
                self.border = np.append(self.border, [[x, y]], axis=0)

                # self.ax.scatter(x, y, s=100, marker='o', c='green')
                # self.fig.canvas.draw()
                # self.fig.canvas.flush_events()


                self.area[int(x)][int(y)] = True
                delta += increment_diagonal
            else:
                delta += increment_horizontal
                x += 1

    def __RightUpper(self, x, y, dx, dy):
        delta = 2 * dx - dy
        increment_vertical = 2 * dx
        increment_diagonal = 2 * (dx - dy)
        for i in range(int(dy)):
            if delta > 0:
                x += 1
                delta += increment_diagonal
            else:
                delta += increment_vertical
            y += 1
            self.border = np.append(self.border, [[x, y]], axis=0)

            # self.ax.scatter(x, y, s=100, marker='o', c='green')
            # self.fig.canvas.draw()
            # self.fig.canvas.flush_events()


            self.area[int(x)][int(y)] = True

    def __RightDown(self, x, y, dx, dy):
        delta = 2 * dy - dx
        increment_horizontal = 2 * dy
        increment_diagonal = 2 * (dy - dx)
        for i in range(int(dx)):
            if delta > 0:
                y -= 1
                x += 1
                self.border = np.append(self.border, [[x, y]], axis=0)

                # self.ax.scatter(x, y, s=100, marker='o', c='green')
                # self.fig.canvas.draw()
                # self.fig.canvas.flush_events()


                self.area[int(x)][int(y)] = True
                delta += increment_diagonal
            else:
                x += 1
                delta += increment_horizontal

    def __RightDowner(self, x, y, dx, dy):
        delta = 2 * dx - dy
        increment_vertical = 2 * dx
        increment_diagonal = 2 * (dx - dy)
        for i in range(int(dy)):
            if delta > 0:
                x += 1
                delta += increment_diagonal
            else:
                delta += increment_vertical
            y -= 1
            self.border = np.append(self.border, [[x, y]], axis=0)

            # self.ax.scatter(x, y, s=100, marker='o', c='green')
            # self.fig.canvas.draw()
            # self.fig.canvas.flush_events()


            self.area[int(x)][int(y)] = True


app = Filling()
app.run()
