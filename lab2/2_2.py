from tkinter import *
import random


def motion():
    global ind_count
    canvas.move('tag1', 0, 1)
    canvas.move('tag2', 0, 1)
    canvas.move(ind, 0, 1)
    if canvas.coords(ind)[1] < height + 1:
        root.after(10, motion)
    else:
        canvas.move(ind, 0, -height - 5)
        root.after(10, motion)
        if ind_count == 0:
            canvas.delete('tag1')
            create_snow('tag1', 1)
            ind_count = 1
        else:
            canvas.delete('tag2')
            create_snow('tag2', 1)
            ind_count = 0


def create_snow(t, n):
    for _ in range(100):
        x = random.randint(1, width)
        y = random.randint(-height * n - 8, height * (1 - n))
        w = random.randint(3, 8)
        canvas.create_oval(x, y, x+w, y+w, fill='white', tag=t)


def main():
    global ind, ind_count
    ind = canvas.create_oval(-1, -1, 0, 0, fill='white')
    ind_count = 0
    create_snow('tag1', 0)
    create_snow('tag2', 1)
    motion()


root = Tk()
root.title('SnowFall')
width = 1920
height = 1080
root.resizable(0, 0)
canvas = Canvas(root, width=width, height=height, bg='#000000')
canvas.pack()
main()

root.mainloop()
