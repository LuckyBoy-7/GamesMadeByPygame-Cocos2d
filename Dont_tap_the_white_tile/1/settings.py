from collections import namedtuple


Pos = namedtuple("Pos", ["x", "y"])


class Settings(object):
    COLUMNS = 4
    ROWS = 5

    ratio = 10
    GRID_WIDTH = 8 * ratio
    GRID_HEIGHT = 11 * ratio
    TABLE_WIDTH = GRID_WIDTH * COLUMNS
    TABLE_HEIGHT = GRID_HEIGHT * ROWS

    WIDTH = 1200
    HEIGHT = 800

    START = Pos((WIDTH - GRID_WIDTH * COLUMNS) // 2, (HEIGHT - GRID_HEIGHT * ROWS) // 2)
