from turtle import *


def draw_rectangle(x, y, width, height, color_fill):
    up()
    goto(x, y)
    color(color_fill, color_fill)
    down()
    begin_fill()
    for _ in range(2):
        forward(width)
        right(90)
        forward(height)
        right(90)
    end_fill()
    up()   


def draw_trident(color_line, line_width):
    width(line_width)
    color(color_line)
    trident_coords = [
        (0, 210), (45, 120), (10, -60), (45, -120), (60, -90),
        (135, -60), (75, -30), (90, 60), (135, 120), (135, -120),
        (45, -120), (0, -180),
        (0, 210), (-45, 120), (-10, -60), (-45, -120), (-60, -90),
        (-135, -60), (-75, -30), (-90, 60), (-135, 120), (-135, -120),
        (-45, -120), (0, -180)
    ]
    up()
    goto(trident_coords[0])
    down()
    for coord in trident_coords[1:]:
        goto(coord)
    up()
def draw_text(text, x, y, font_size=20):
    up()
    goto(x, y)
    down()
    color('black')
    write(text, align='center', font=("Times New Roman", font_size, 'bold'))


setup(600, 480)
speed(0)
hideturtle()


draw_rectangle(-300, 240, 600, 240, 'blue')
draw_rectangle(-300, 0, 600, 240, 'yellow')


draw_trident('white', 30)
draw_trident('blue', 15)


draw_text("Слава Україні! Перемога за нами!", 0, -225)


done()
