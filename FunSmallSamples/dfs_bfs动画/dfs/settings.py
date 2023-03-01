class Settings:
    GRID_SIZE = 24
    ROWS = 31  # 都要是奇数
    COLUMNS = 31

    THRESHOLD = 1  # 阈值

    show_num = False  # 是否展现路径先后顺序

    START_POS = 1, 1  # x, y, axis
    END_POS = ROWS - 2, COLUMNS - 2

    WIDTH, HEIGHT = 1400, 800
    ORIGIN = WIDTH / 2 - COLUMNS / 2 * GRID_SIZE, HEIGHT / 2 - ROWS / 2 * GRID_SIZE