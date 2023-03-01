import pygame

from settings import Settings
from stats import stats


class HpPrompt(object):
    DOT_COLOR = 255, 0, 0, 255
    DOT_RADIUS = 10
    DOT_DIAMETER = DOT_RADIUS * 2

    def __init__(self, surface, camp: str):
        self.screen = surface
        self.camp = camp
        self.direct = 1 if self.camp == "left" else -1
        self.update()
        self.x, self.y = self.get_position()

    def get_position(self):
        y = self.DOT_RADIUS
        if self.camp == "left":
            x = self.DOT_RADIUS
        else:
            x = Settings.WIDTH - self.DOT_RADIUS

        return x, y

    def update(self):
        self.hp = stats.left_hp if self.camp == "left" else stats.right_hp

    def draw(self):
        for i in range(self.hp):
            pygame.draw.circle(self.screen, self.DOT_COLOR, (self.x + self.direct * (2 + self.DOT_DIAMETER) * i, self.y),
                               self.DOT_RADIUS)
