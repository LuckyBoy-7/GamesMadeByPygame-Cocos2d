class Settings(object):
    GRID_SIZE = 40
    MINE_NUMS = 15

    ROWS = 10
    COLUMNS = 10

    WIDTH = 1000
    HEIGHT = 800

    ORIGIN = (int(WIDTH / 2 - COLUMNS / 2 * GRID_SIZE),
              int(HEIGHT / 2 - ROWS / 2 * GRID_SIZE))
