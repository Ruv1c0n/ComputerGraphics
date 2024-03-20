import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox


STAR_POINTS = np.array([[0, 4], [1, 0.9], [4.1, 0.9], [1.6, -0.9], [2.5, -3.8],
                        [0, -2], [-1.6, -1.1], [-1.6, 0.6], [0, 1.4], [1.6, 0.6], [1.6, -1.1], [0, -2], [-2.5, -3.8], [-1.6, -0.9], [-4.1, 0.9], [-1, 0.9], [0, 4]])


class Controllers:
    def __init__(self):
        self.shift_step = 0.5

    def __update_figure(self):
        f.set_data(star_coords[:, 0], star_coords[:, 1])
        ax.draw_artist(f)
        fig.canvas.blit(ax.bbox)
        plt.pause(0.001)

    def reset(self):
        global star_coords
        star_coords = np.copy(STAR_POINTS)
        self.__update_figure()

    def __scale(self, direction, coef):
        global star_coords
        for coord in star_coords:
            coord[0 if direction == 'x' else 1] *= np.float64(coef)

    def scale_Ox(self, expression):
        self.__scale('x', expression)
        self.__update_figure()

    def scale_Oy(self, expression):
        self.__scale('y', expression)
        self.__update_figure()

    def reflection_Ox(self):
        self.__update_figure()

    def reflection_Oy(self):
        self.__update_figure()

    def reflection_xy(self):
        self.__update_figure()

    def __shift(self, oxy, direction):
        global star_coords
        for coord in star_coords:
            coord[0 if oxy == 'x' else 1] += self.shift_step * direction

    def shift_Ox(self, direction):
        self.__shift('x', direction)
        self.__update_figure()

    def shift_Oy(self, direction):
        self.__shift('y', direction)
        self.__update_figure()

    def rotate(self):
        self.__update_figure()

    def point_rotate(self):
        self.__update_figure()


fig, ax = plt.subplots(figsize=(9, 10))
fig.subplots_adjust(bottom=0.4)


star_coords = np.copy(STAR_POINTS)

f, = ax.plot(star_coords[:, 0], star_coords[:, 1])

cntrl = Controllers()
bs = fig.add_axes([0.11, 0.045, 0.03, 0.03])
bShiftXRight = Button(bs, '→')
bShiftXRight.on_clicked(lambda x: cntrl.shift_Ox(1))
bs = fig.add_axes([0.01, 0.045, 0.03, 0.03])
bShiftXLeft = Button(bs, '←')
bShiftXLeft.on_clicked(lambda x: cntrl.shift_Ox(-1))
bs = fig.add_axes([0.06, 0.08, 0.03, 0.03])
bShiftYUp = Button(bs, '↑')
bShiftYUp.on_clicked(lambda x: cntrl.shift_Oy(1))
bs = fig.add_axes([0.06, 0.01, 0.03, 0.03])
bShiftYDown = Button(bs, '↓')
bShiftYDown.on_clicked(lambda x: cntrl.shift_Oy(-1))

bs = fig.add_axes([0.045, 0.045, 0.06, 0.03])
bReset = Button(bs, 'reset')
bReset.on_clicked(lambda x: cntrl.reset())

bs = fig.add_axes([0.2, 0.07, 0.1, 0.03])
tbScaleX = TextBox(bs, "Scale x", textalignment="center")
tbScaleX.set_val(1)
tbScaleX.on_submit(cntrl.scale_Ox)
bs = fig.add_axes([0.2, 0.01, 0.1, 0.03])
tbScaleY = TextBox(bs, "Scale y", textalignment="center")
tbScaleY.set_val(1)
tbScaleY.on_submit(lambda x: cntrl.scale_Oy)

plt.xlim(-10, 10)
plt.ylim(-10, 10)
ax.grid(True)
plt.show()
