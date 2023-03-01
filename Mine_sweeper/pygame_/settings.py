class Settings(object):
    WIDTH = 1000
    HEIGHT = 800
    WINDOW_SIZE = WIDTH, HEIGHT
    levels = {0: {"grid_size": 40,
                  "mine_nums": 10,
                  "rows": 9,
                  "columns": 9},
              1: {"grid_size": 35,
                  "mine_nums": 40,
                  "rows": 16,
                  "columns": 16},
              2: {"grid_size": 30,
                  "mine_nums": 99,
                  "rows": 16,
                  "columns": 30}}
    TICK = 90
