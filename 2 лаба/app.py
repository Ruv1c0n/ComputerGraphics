from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import (
    Button,
    RadioButtons,
    TextBox
)


from changes import *


class App:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 10))
        self.fig.canvas.manager.set_window_title('Звезда и шестиугольник')
        self.ax = self.fig.add_subplot()
        self.__init_axes()
        self.fig.subplots_adjust(bottom=0.2)
        self.__init_ui()

    def __init_axes(self):
        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('center')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set(xlim=(-10, 10), ylim=(-10, 10))
        self.ax.grid(True)

    def __init_ui(self):
        self.__init_reflection_type_changer_block()
        self.__init_transformations_values_input_block()
        self.__init_buttons_block()
        self.__init_figure()

    def __init_reflection_type_changer_block(self):
        # reflection_types = [r_type.value for r_type in ReflectionType]
        reflection_types = ['X', 'Y', 'X = Y']

        self.reflection_type_axes = self.fig.add_axes(
            [0.01, 0.07, 0.08, 0.1], facecolor='#d9d9d9')
        self.rbs_reflection_type = RadioButtons(
            self.reflection_type_axes,
            reflection_types,
            radio_props={'s': [64, 64, 64]},
            activecolor='black'
        )
        self.rbs_reflection_type.on_clicked(self._reflect_type_changed)

        self.current_reflect_type = reflection_types[0]

    def __init_transformations_values_input_block(self):
        self.input_x_axes = self.fig.add_axes([0.15, 0.12, 0.1, 0.05])
        self.input_x = TextBox(
            self.input_x_axes, ' X ', initial='0.0')
        self.input_x.on_submit(self._set_x)

        self.input_y_axes = self.fig.add_axes([0.15, 0.065, 0.1, 0.05])
        self.input_y = TextBox(
            self.input_y_axes, ' Y ', initial='0.0')
        self.input_y.on_submit(self._set_y)

        self.angle_axes = self.fig.add_axes([0.15, 0.01, 0.1, 0.05])
        self.angle_entry = TextBox(
            self.angle_axes, ' Angle ', initial='0'
        )
        self.angle_entry.on_submit(self._set_angle)

        self.current_coords = np.array([
            float(self.input_x.text),
            float(self.input_y.text),
        ])
        self.current_angle = float(self.angle_entry.text)

    def __init_buttons_block(self):
        self.reflection_run_axes = self.fig.add_axes([0.01, 0.01, 0.08, 0.05])
        self.b_reflection = Button(
            self.reflection_run_axes, 'Отразить', hovercolor='white')
        self.b_reflection.on_clicked(lambda x: self._reflect())

        self.shift_axes = self.fig.add_axes([0.26, 0.12, 0.15, 0.05])
        self.b_shift = Button(
            self.shift_axes, 'Переместить', hovercolor='white')
        self.b_shift.on_clicked(self._shift)

        self.scale_axes = self.fig.add_axes([0.26, 0.065, 0.15, 0.05])
        self.b_scale = Button(
            self.scale_axes, 'Масштабировать', hovercolor='white')
        self.b_scale.on_clicked(self._scale)

        self.rotate_axes = self.fig.add_axes([0.26, 0.01, 0.15, 0.05])
        self.b_rotate = Button(
            self.rotate_axes, 'Повернуть', hovercolor='white')
        self.b_rotate.on_clicked(self._rotate)

        self.reset_axes = self.fig.add_axes([0.45, 0.065, 0.15, 0.05])
        self.reset_button = Button(
            self.reset_axes, 'Восстановить', hovercolor='green')
        self.reset_button.on_clicked(self._reset)

    def __init_figure(self):
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
            [-1, 0.9, 1],
            [0, 4, 1],
            [0, 4, 1]
        ])
        self.coords = np.copy(self.const_coords)

    def run(self):
        self._draw()
        plt.show()

    def _draw(self):
        self.ax.clear()
        self.__init_axes()
        points = np.array(list(map(lambda x: x[:2], self.coords)))
        polygon = Polygon(points, fc='none', ec='black', closed=False)
        self.ax.add_patch(polygon)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def _reflect_type_changed(self, label_name):
        if label_name == 'X':
                self.current_reflect_type = 'X'
        elif label_name == 'Y':
                self.current_reflect_type = 'Y'
        elif label_name == 'X = Y':
                self.current_reflect_type = 'X = Y'

    def _reflect(self):
        if self.current_reflect_type == 'X':
                self.coords = scale_figure(self.coords, 1, -1)
        elif self.current_reflect_type == 'Y':
                self.coords = scale_figure(self.coords, -1, 1)
        elif self.current_reflect_type == 'X = Y':
                self.coords = xy_reflection(self.coords)
        self._draw()

    def _set_x(self, text):
        self.current_coords[0] = float(text)

    def _set_y(self, text):
        self.current_coords[1] = float(text)

    def _set_angle(self, text):
        self.current_angle = float(text)

    def _shift(self, event):
        self.coords = shift_figure(
            self.coords, self.current_coords[0], self.current_coords[1])
        self._draw()

    def _scale(self, event):
        self.coords = scale_figure(
            self.coords, self.current_coords[0], self.current_coords[1])
        self._draw()

    def _rotate(self, event):
        self.coords = rotate_figure(
            self.coords, self.current_coords[0], self.current_coords[1], self.current_angle)
        self._draw()

    def _reset(self, event):
        self.coords = np.copy(self.const_coords)
        self._draw()


app = App()
app.run()
