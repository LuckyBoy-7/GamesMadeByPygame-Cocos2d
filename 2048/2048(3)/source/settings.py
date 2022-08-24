import os
from atexit import register
from collections import namedtuple

import pyglet


class Settings:
    pyglet.resource.path.append("../res")
    pyglet.resource.reindex()

    ROWS = 5
    COLUMNS = 5
    GRID_SIZE = 80

    WIDTH = 888
    HEIGHT = 888
    WINDOW_SIZE = WIDTH, HEIGHT

    MID_X = WIDTH / 2
    MID_Y = HEIGHT / 2

    ORIGIN = namedtuple("ORIGIN", "x y")(WIDTH / 2 - COLUMNS / 2 * GRID_SIZE, HEIGHT / 2 - ROWS / 2 * GRID_SIZE)

    different_grid_color = [(52, 44, 37, 255), (52, 44, 27, 255),
                            (242, 177, 121, 255), (245, 149, 99, 255),
                            (218, 110, 84, 255), (210, 80, 50, 255),
                            (204, 178, 98, 255), (237, 204, 97, 255)]

    fade_time = 0.2
    move_time = 0.4

    score = 0
    if not os.path.exists("score.txt"):
        with open("score.txt", "w", encoding="UTF-8") as f:
            f.write("0")
        best_score = 0
    else:
        with open("score.txt", "r+", encoding="UTF-8") as f:
            txt = f.read()
            if txt.isdigit():
                best_score = int(txt)
            else:
                if any(letter.isdigit() for letter in txt):
                    best_score = int("".join([num for num in txt if num.isdigit()]))
                else:
                    best_score = 0


@register
def exit_write_score():
    with open("score.txt", "w", encoding="UTF-8") as f:
        f.write(f"{Settings.best_score}")
