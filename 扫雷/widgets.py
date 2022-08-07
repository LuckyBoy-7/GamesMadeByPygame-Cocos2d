from time import time
from collections import namedtuple

from cocos.text import Label
from cocos.rect import Rect

from settings import Settings
from color import *


class Hint(object):
    """both Timer & Left Mines & game_over & succeed"""

    start_time: float

    def __init__(self, game_layer):
        self.game_layer = game_layer
        self.is_start = False

        self.mine_nums = Settings.mine_nums
        self.mines_hint = self.create_label(f"Mines left: {Settings.mine_nums}", (0, Settings.HEIGHT))
        self.time_hint = self.create_label(f"Time counting: 0", (0, Settings.HEIGHT - 50))

    def create_label(self, text, pos, anchor_x="left"):
        label = Label(text=text,
                      position=pos,
                      font_size=30,
                      color=BLACK,
                      anchor_x=anchor_x,
                      anchor_y="top")
        self.game_layer.add(label)
        return label

    def start(self):
        if not self.is_start:
            self.start_time = time()
            self.is_start = True

    def get_time(self):
        if self.is_start:
            return time() - self.start_time

    def update_time(self):
        if self.is_start:
            self.mines_hint.element.text = f"Mines left: {self.mine_nums}"
            self.time_hint.element.text = f"Time counting: {round(self.get_time(), 1)}"

    def game_over(self):
        self.create_label("LOSE", Settings.WINDOW_SIZE, "right")
        self.game_layer.show_all_mines()
        self.game_layer.stop_work()

    def succeed(self):
        self.create_label("YOU WIN!", Settings.WINDOW_SIZE, "right")
        self.game_layer.stop_work()


class Button(object):
    def __init__(self, game_layer):
        self.game_layer = game_layer

        self.low_level_rect = self.create_label("初级", (Settings.WIDTH - 20, 0))
        self.mid_level_rect = self.create_label("中级", (Settings.WIDTH - 120, 0))
        self.high_level_rect = self.create_label("高级", (Settings.WIDTH - 220, 0))

    def create_label(self, text, pos):
        label = Label(text=text,
                      position=pos,
                      font_name="Fira code",
                      font_size=30,
                      color=BLACK,
                      anchor_x="right",
                      anchor_y="bottom")
        self.game_layer.add(label)

        return Rect(label.x - label.element.content_width,
                    label.y,
                    label.element.content_width,
                    label.element.content_height)

    def check_button(self, x, y):
        if self.low_level_rect.contains(x, y):
            Settings.grid_size = 40
            Settings.mine_nums = 10
            Settings.rows = 9
            Settings.columns = 9
            Settings.origin = namedtuple("ORIGIN", "x y")(
                int(Settings.WIDTH / 2 - Settings.columns / 2 * Settings.grid_size),
                int(Settings.HEIGHT / 2 - Settings.rows / 2 * Settings.grid_size))
            self.game_layer.restart()
        elif self.mid_level_rect.contains(x, y):
            Settings.grid_size = 35
            Settings.mine_nums = 40
            Settings.rows = 16
            Settings.columns = 16
            Settings.origin = namedtuple("ORIGIN", "x y")(
                int(Settings.WIDTH / 2 - Settings.columns / 2 * Settings.grid_size),
                int(Settings.HEIGHT / 2 - Settings.rows / 2 * Settings.grid_size))
            self.game_layer.restart()
        elif self.high_level_rect.contains(x, y):
            Settings.grid_size = 30
            Settings.mine_nums = 99
            Settings.rows = 16
            Settings.columns = 30
            Settings.origin = namedtuple("ORIGIN", "x y")(
                int(Settings.WIDTH / 2 - Settings.columns / 2 * Settings.grid_size),
                int(Settings.HEIGHT / 2 - Settings.rows / 2 * Settings.grid_size))
            self.game_layer.restart()


def all_permutations(lst):
    for i in lst:
        for j in lst:
            yield i, j
