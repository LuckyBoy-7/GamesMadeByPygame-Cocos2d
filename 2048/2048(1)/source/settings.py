from random import randint
from collections import namedtuple

from pyglet.resource import image
import pyglet


class Settings:
    pyglet.resource.path.append("../res")
    pyglet.resource.reindex()

    ROWS = 4
    COLUMNS = 4
    GRID_SIZE = 135

    WIDTH = 888
    HEIGHT = 888

    MID_X = WIDTH / 2
    MID_Y = HEIGHT / 2

    offset = 18
    img = image("background.png")
    ORIGIN = namedtuple("ORIGIN", "x y")(MID_X - img.width / 2 + offset, MID_Y - img.height / 2 + offset)

    different_grid_color = [(52, 44, 37, 255), (52, 44, 27, 255),
                            (242, 177, 121, 255), (245, 149, 99, 255),
                            (218, 110, 84, 255), (210, 80, 50, 255),
                            (204, 178, 98, 255), (237, 204, 97, 255)]
