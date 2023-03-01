class Settings:
    GRID_SIZE = 24
    ROWS = 21
    COLUMNS = 21

    WIDTH, HEIGHT = 1400,  800
    ORIGIN = WIDTH / 2 - COLUMNS / 2 * GRID_SIZE, HEIGHT - ROWS * GRID_SIZE - 10

    typing_start = WIDTH / 2, HEIGHT / 2 - 200
    grid_start, grid_end = (5, 5), (COLUMNS - 6, ROWS - 6)

