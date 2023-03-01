from random import randint

import pygame

from settings import Settings
from stats import stats
from color import *


class Grid(object):
    def __init__(self, surface, x, y, color):
        self.screen = surface
        self.x, self.y = x, y
        self.color = color
        self.size = Settings.levels[stats.level]["grid_size"]

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.size, self.size))


class Mine(Grid):
    def __init__(self, surface, x, y):
        super().__init__(surface, x, y, (255, 0, 0, 255))


class Flag(Grid):
    def __init__(self, surface, x, y):
        super().__init__(surface, x, y, (0, 255, 0, 255))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))


class Space(Grid):
    colors = [BLUE, GREEN, RED, DARK_BLUE]

    def __init__(self, surface, x, y, num=None):
        super().__init__(surface, x, y, (255, 255, 255, 255))

        self.num = num
        self.font = pygame.font.SysFont("Arial", self.size)

        if num <= 4:
            self.font_color = self.colors[num - 1]
        else:
            self.font_color = (randint(0, 255), randint(0, 255), randint(0, 255), 255)
        w, h = self.font.size(str(self.num))  # txt being whatever str you're rendering
        self.font_x = self.x + (self.size - w) // 2
        self.font_y = self.y + (self.size - h) // 2

    def draw(self):
        super().draw()

        # 更新数字
        if self.num > 0:
            self.screen.blit(self.font.render(f"{self.num}", True, self.font_color), (self.font_x, self.font_y))


class BlinkGrid(Grid):
    def __init__(self, surface, x, y):
        super().__init__(surface, x, y, (255, 255, 255, 255))

        self.is_blink = False
        self.elapse = 0
        self.threshold = 7

    def update(self):
        if self.is_blink:
            self.elapse += 1
            if self.elapse > self.threshold:
                self.elapse = 0
                self.is_blink = False

    def draw(self):
        if self.is_blink:
            super().draw()

    def blink(self):
        self.is_blink = True
