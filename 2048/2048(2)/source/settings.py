from random import randint
from collections import namedtuple

from pyglet.resource import image
import pyglet


class Settings:
    pyglet.resource.path.append("../res")
    pyglet.resource.reindex()

    ROWS = 8
    COLUMNS = 8
    GRID_SIZE = 80

    WIDTH = 888
    HEIGHT = 888

    MID_X = WIDTH / 2
    MID_Y = HEIGHT / 2

    ORIGIN = namedtuple("ORIGIN", "x y")(WIDTH / 2 - COLUMNS / 2 * GRID_SIZE, HEIGHT / 2 - ROWS / 2 * GRID_SIZE)

    different_grid_color = [(52, 44, 37, 255), (52, 44, 27, 255),
                            (242, 177, 121, 255), (245, 149, 99, 255),
                            (218, 110, 84, 255), (210, 80, 50, 255),
                            (204, 178, 98, 255), (237, 204, 97, 255)]

    fade_time = 0.2
