from collections import namedtuple

import pyglet


class Settings:
    pyglet.resource.path.append("../res")
    pyglet.resource.reindex()

    ROWS = 6
    COLUMNS = 6
    GRID_SIZE = 80

    WIDTH = 888
    HEIGHT = 888
    WINDOW_SIZE = WIDTH, HEIGHT

    MID_X = WIDTH / 2
    MID_Y = HEIGHT / 2

    # 网格left-bottom坐标
    ORIGIN = namedtuple("ORIGIN", "x y")(WIDTH / 2 - COLUMNS / 2 * GRID_SIZE, HEIGHT / 2 - ROWS / 2 * GRID_SIZE)

    different_grid_color = {-1: (100, 100, 100, 255),
                            1: (52, 44, 37, 255), 2: (52, 44, 27, 255),
                            3: (242, 177, 121, 255), 4: (245, 149, 99, 255),
                            5: (218, 110, 84, 255), 6: (210, 80, 50, 255),
                            7: (204, 178, 98, 255), 8: (237, 204, 97, 255),
                            }

    fade_time = 0.2
    move_time = 0.4
