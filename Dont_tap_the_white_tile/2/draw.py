from itertools import chain, accumulate
from collections import namedtuple, deque
from random import randint

import pygame

from settings import Settings
from stats import stats

Pos = namedtuple("Pos", ["x", "y"])

BLACK = 0, 0, 0, 255
TAPED_COLOR = 127, 127, 127, 255


def lock(refer, condition, execute_time):
    def wrapper(func):
        is_execute = False
        on_enter = True
        execute_time_backup = execute_time

        def inner():
            nonlocal condition, execute_time, is_execute, on_enter
            if getattr(refer, condition) or is_execute:
                is_execute = True
                # 是否执行on_enter回调函数
                if on_enter and hasattr(refer, "on_enter"):
                    getattr(refer, "on_enter")()
                    on_enter = False

                if execute_time > 0:
                    execute_time -= 1
                    func()
                if execute_time == 0:
                    is_execute = False
                    on_enter = True
                    execute_time = execute_time_backup
                    # 是否执行on_exit回调函数
                    if hasattr(refer, "on_exit"):
                        getattr(refer, "on_exit")()

        return inner

    return wrapper


class Line(object):
    def __init__(self, surface, start, end, color=(0, 0, 0, 255), stroke_width=1):
        self.screen_surface = surface
        self.start = Pos(*start)
        self.end = Pos(*end)
        self.color = color
        self.stroke_width = stroke_width

        self.is_move = False  # 什么时候可以开始移动
        # 这里上了个锁, 本质上就是装饰器, 根据is_move状态来决定是否执行, 而update是一直被调用的
        self.update = lock(self, condition="is_move",
                           execute_time=Settings.GRID_HEIGHT // Settings.MOVE_SPEED)(self.update)

    def update(self) -> None:
        self.start = Pos(self.start.x, self.start.y + Settings.MOVE_SPEED)
        self.end = Pos(self.end.x, self.end.y + Settings.MOVE_SPEED)
        if self.start.y >= Settings.HEIGHT:
            self.start = Pos(self.start.x, self.start.y - Settings.TABLE_HEIGHT)
            self.end = Pos(self.end.x, self.end.y - Settings.TABLE_HEIGHT)

    def draw(self) -> None:
        pygame.draw.line(self.screen_surface,
                         start_pos=self.start,
                         end_pos=self.end,
                         color=self.color,
                         width=self.stroke_width)

    def on_exit(self):
        self.is_move -= 1


class Lines(object):
    def __init__(self, surface):
        self.screen_surface = surface
        self.horizontal_lines = []
        self.vertical_lines = []
        self.init()

    def move(self) -> None:
        for line in self.horizontal_lines:
            line.is_move = True

    def update(self) -> None:
        for line in self.horizontal_lines:
            line.update()

    def draw(self) -> None:
        for line in chain(self.horizontal_lines, self.vertical_lines):
            line.draw()

    def init(self) -> None:
        start_x, start_y = Settings.START
        for x in range(Settings.COLUMNS + 1):
            self.vertical_lines.append(Line(surface=self.screen_surface,
                                            start=(start_x + Settings.GRID_WIDTH * x, start_y),
                                            end=(start_x + Settings.GRID_WIDTH * x, 0),
                                            color=(0, 0, 0, 255),
                                            stroke_width=1))

        for y in range(Settings.ROWS + 1):
            self.horizontal_lines.append(Line(surface=self.screen_surface,
                                              start=(start_x, start_y - Settings.GRID_HEIGHT * y),
                                              end=(start_x + Settings.TABLE_WIDTH, start_y - Settings.GRID_HEIGHT * y),
                                              color=(0, 0, 0, 255),
                                              stroke_width=1))


class Grid(object):
    width = Settings.GRID_WIDTH  # 补偿线条的宽度
    height = Settings.GRID_HEIGHT

    def __init__(self, surface, x, y, col):
        self.screen_surface = surface
        self.x = x
        self.y = y
        self.col = col

        self.move_event_cnt = 0  # >0时可以开始移动
        self.update = lock(self, condition="move_event_cnt",
                           execute_time=Settings.GRID_HEIGHT // Settings.MOVE_SPEED)(self.update)

    def get_rect(self) -> tuple:
        return Settings.START.x + Settings.GRID_WIDTH * self.col, self.y, self.width, self.height

    def update(self) -> None:  # 打过补丁了
        self.y += Settings.MOVE_SPEED
        if self.y >= Settings.HEIGHT:  # 向下移动
            self.y -= Settings.TABLE_HEIGHT + Settings.GRID_HEIGHT
            self.reset()

    def reset(self) -> None:  # 新的一轮
        self.col = randint(0, 3)  # 随机位置
        self.color = self.color_backup  # 复原颜色

    def draw(self) -> None:
        pygame.draw.rect(self.screen_surface, color=self.color, rect=self.get_rect())

    def on_exit(self):
        self.move_event_cnt -= 1


class BlackGrid(Grid):
    def __init__(self, surface, x, y, col):
        super().__init__(surface, x, y, col)

        self.color_backup = self.color = 0, 0, 0, 255


class RedGrid(Grid):
    poses = set()

    def __init__(self, surface, x, y, col):
        super().__init__(surface, x, y, col)

        self.color_backup = self.color = 255, 0, 0, 255
        self.is_show = False
        self.col = col

    def show(self, col):
        if col not in self.poses:
            self.y = Settings.GRID_HEIGHT * (Settings.ROWS - 1)
            self.is_show = True
            self.col = col
            self.poses.add(self.col)

    def update(self) -> None:
        if self.is_show:
            super().update()

    def on_exit(self):  # 移动结束后
        super().on_exit()
        self.is_show = False
        self.poses.clear()


class Grids(object):
    match = {key: num for key, num in zip(("d", "f", "j", "k"), range(4))}

    current_grid_idx = -1

    def __init__(self, surface):
        self.screen_surface = surface
        self.grids = deque()
        self.wrong_grids = [self.create_red_grid(0) for _ in range(Settings.COLUMNS - 1)]
        self.create_grids()

    def is_move(self) -> bool:
        return bool(self.grids[0].move_event_cnt)

    def _create_grid(self, cls, col, row) -> Grid:
        start_x, start_y = Settings.START
        return cls(self.screen_surface,
                   x=start_x + Settings.GRID_WIDTH * col,
                   y=Settings.GRID_HEIGHT * row,
                   col=col)

    def create_red_grid(self, col, row=Settings.ROWS):
        return self._create_grid(RedGrid, col, row)

    def create_black_grid(self, col, row=Settings.ROWS - 1):
        return self._create_grid(BlackGrid, col, row)

    def create_grids(self) -> None:
        pos = [randint(0, 3) for _ in range(Settings.ROWS + 1)]
        for row, col in enumerate(pos, -1):
            self.grids.append(self.create_black_grid(col=col, row=row))

    def draw(self) -> None:
        for grid in chain(self.grids, self.wrong_grids):
            grid.draw()

    def update(self) -> None:
        for grid in chain(self.grids, self.wrong_grids):
            grid.update()  # 不断调用

    def move(self) -> None:
        self.grids[self.current_grid_idx].color = TAPED_COLOR
        self.current_grid_idx = (self.current_grid_idx - 1) % len(self.grids)
        for grid in self.grids:
            grid.move_event_cnt += 1
        for grid in self.wrong_grids:
            if grid.is_show:
                grid.move_event_cnt += 1

    def show_wrong_grid(self, key):
        if key in self.match:
            for grid in self.wrong_grids:
                if not grid.is_show:
                    grid.show(col=self.match[key])
                    break


class Prompts(object):
    def __init__(self, surface, music):
        self.screen_surface = surface
        self.font = pygame.font.SysFont("Arial", 25)
        self.music = music

    def update(self) -> None:
        # render不接受keyword args, why?  parameters: text, is_antialias, color
        self.txt_right = self.font.render(f"altogether {stats.right_tap} right taps", True, BLACK)
        self.txt_wrong = self.font.render(f"altogether {stats.wrong_tap} wrong taps", True, BLACK)
        self.music_time_remaining = self.font.render(f"music time remains {self.music.elapsed // Settings.TICK}s", True,
                                                     BLACK)
        self.txt_combo = self.font.render(f"combo {stats.combo} times!!!", True, BLACK)

    def draw(self) -> None:
        texts = [self.txt_right,
                 self.txt_wrong,
                 self.music_time_remaining,
                 self.txt_combo]
        for txt, height in zip(texts, accumulate(txt.get_height() for txt in texts)):
            self.screen_surface.blit(txt, (0, height - texts[0].get_height()))
