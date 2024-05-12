from tkinter import *
import random


class Snowflake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = None
        self.x = random.randint(1, self.canvas.winfo_reqwidth() - 1)
        self.y = random.randint(-1, self.canvas.winfo_reqheight() - 1)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(10, 20)
        self.draw()

    def draw(self):
        points = [(1, 1), (1, 0.5), (1.3, 0.5), (0.7, 0.5), (1, 0.5), (1, 0.2), (1.2, 0.2), (0.8, 0.2), (1, 0.2), (1, 0),
                  (1, 1), (1.4, 0.6), (1.6, 0.8), (1.2, 0.4), (1.4, 0.6), (1.6, 0.4), (1.7, 0.5), (1.5, 0.3), (1.6, 0.4), (1.7, 0.3),
                  (1, 1), (1.5, 1), (1.5, 1.3), (1.5, 0.7), (1.5, 1), (1.8, 1), (1.8, 1.2), (1.8, 0.8), (1.8, 1), (2, 1),
                  (1, 1), (1.4, 1.4), (1.2, 1.6), (1.6, 1.2), (1.4, 1.4), (1.6, 1.6), (1.5, 1.7), (1.7, 1.5), (1.6, 1.6), (1.7, 1.7),
                  (1, 1), (1, 1.5), (1.3, 1.5), (0.7, 1.5), (1, 1.5), (1, 1.8), (1.2, 1.8), (0.8, 1.8), (1, 1.8), (1, 2),
                  (1, 1), (0.6, 1.4), (0.8, 1.6), (0.4, 1.2), (0.6, 1.4), (0.4, 1.6), (0.5, 1.7), (0.3, 1.5), (0.4, 1.6), (0.3, 1.7),
                  (1, 1), (0.5, 1), (0.5, 1.3), (0.5, 0.7), (0.5, 1), (0.2, 1), (0.2, 1.2), (0.2, 0.8), (0.2, 1), (0, 1),
                  (1, 1), (0.6, 0.6), (0.4, 0.8), (0.8, 0.4), (0.6, 0.6), (0.4, 0.4), (0.3, 0.5), (0.5, 0.3), (0.4, 0.4), (0.3, 0.3)]
        scaled_points = [(x * self.size + self.x, y * self.size + self.y)
                         for x, y in points]
        self.id = self.canvas.create_polygon(scaled_points, outline='white')

    def move(self):
        rand_x = self.speed * 0.5 * (random.randrange(-1, 1))
        self.canvas.move(self.id, rand_x, self.speed)
        self.y += self.speed
        self.x += rand_x


def create_snowflakes(canvas, snowflakes_count):
    snowflakes = []
    for _ in range(snowflakes_count):
        snowflake = Snowflake(canvas)
        snowflakes.append(snowflake)
    return snowflakes


def motion():
    for flake in snowflakes:
        flake.move()
        if flake.y > 1080:
            flake.y = -1
            flake.x = random.randint(1, 1919)
            flake.speed = random.uniform(1, 3)
            flake.canvas.delete(flake.id)
            flake.draw()
    root.after(30, motion)


root = Tk()
root.title("SnowFall")
width = 1920
height = 1080
canvas = Canvas(root, width=width, height=height, bg='#a3b4d6')
canvas.pack()
snowflakes_count = 150
snowflakes = create_snowflakes(canvas, snowflakes_count)
motion()

root.mainloop()
