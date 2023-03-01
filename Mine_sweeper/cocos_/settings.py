from collections import namedtuple


class Settings(object):
    grid_size = 40
    mine_nums = 10
    rows = 9
    columns = 9

    WIDTH = 1000
    HEIGHT = 800
    WINDOW_SIZE = WIDTH, HEIGHT

    origin = namedtuple("ORIGIN", "x y")(int(WIDTH / 2 - columns / 2 * grid_size),
                                         int(HEIGHT / 2 - rows / 2 * grid_size))
