from random import choice, randint

import pygame

from settings import Settings
from stats import stats


class Ball(object):
    COLOR = 0, 0, 255, 255
    RADIUS = 5
    DIAMETER = RADIUS * 2

    def __init__(self, surface, baffles: list):
        self.screen = surface
        self.baffles = baffles
        self.x, self.y = Settings.WIDTH // 2, Settings.HEIGHT // 2
        self.speed_x, self.speed_y = randint(4, 7), randint(4, 6)
        self.backup_x, self.backup_y = self.x, self.y
        self.direct_x, self.direct_y = choice([-1, 1]), choice([-1, 1])

    def update(self):
        """baffle的update更为精细, 要妥善处理, 这里ball的update我就随便写了"""
        self.x += self.direct_x * self.speed_x
        self.y += self.direct_y * self.speed_y

        if self.y < 0 or self.y > Settings.HEIGHT:
            self.direct_y = -self.direct_y
        for baffle in self.baffles:
            if baffle.get_rect().colliderect(self.get_rect()):
                self.direct_x = -self.direct_x
                self.speed_x, self.speed_y = randint(5, 6), randint(5, 10)

        if self.x < 0:
            stats.left_hp -= 1
            stats.game_over = True
        elif self.x > Settings.WIDTH:
            stats.right_hp -= 1
            stats.game_over = True

    def get_rect(self):
        return pygame.rect.Rect(self.x - self.RADIUS, self.y - self.RADIUS, self.DIAMETER, self.DIAMETER)

    def draw(self):
        pygame.draw.circle(self.screen, self.COLOR, (self.x, self.y), self.RADIUS)

    def reset(self):
        self.x, self.y = self.backup_x, self.backup_y
        self.direct_x, self.direct_y = choice([-1, 1]), choice([-1, 1])
        self.speed_x, self.speed_y = randint(5, 6), randint(5, 10)
