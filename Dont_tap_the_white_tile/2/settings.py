from collections import namedtuple

Pos = namedtuple("Pos", ["x", "y"])


class Settings(object):
    COLUMNS = 4
    ROWS = 6

    ratio = 10
    GRID_WIDTH = 8 * ratio
    GRID_HEIGHT = 12 * ratio
    TABLE_WIDTH = GRID_WIDTH * COLUMNS
    TABLE_HEIGHT = GRID_HEIGHT * ROWS

    MOVE_SPEED = 20  # 必须被GRID_HEIGHT整除, 用来控制方块和线条的移动速度

    WIDTH = 1200
    HEIGHT = GRID_HEIGHT * ROWS
    SIZE = WIDTH, HEIGHT

    START = Pos((WIDTH - GRID_WIDTH * COLUMNS) // 2, HEIGHT)

    TICK = 120
