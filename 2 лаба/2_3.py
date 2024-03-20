import tkinter as tk
import random


def move_snowflakes():
    for flake in snowflakes:
        canvas.move(flake['id'], 0, flake['speed'])

        # Если снежинка достигла нижней границы экрана, сбрасываем ее на верх
        if canvas.coords(flake['id'])[1] > height:
            canvas.move(flake['id'], random.randint(0, width), -height)

    window.after(50, move_snowflakes)


window = tk.Tk()
window.title("SnowFall")

width = 1920
height = 1080
canvas = tk.Canvas(window, width=width, height=height, bg='blue')
canvas.pack()

snowflakes = []
for _ in range(100):
    x = random.randint(0, width)
    y = random.randint(0, height)
    snowflake = canvas.create_text(x, y, text='❄', font=('Arial', 20), fill='white')
    snowflakes.append({'id': snowflake, 'speed': random.randint(1, 3)})

move_snowflakes()

window.mainloop()
