import sys

import pygame
from pygame.locals import *
pygame.init()

from .settings import Settings


class Game(object):
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(Settings.SCREEN_SIZE)

        self.clock = pygame.time.Clock()

    def update_screen(self):
        # 绘制屏幕
        self.surface.fill(Settings.BACKGROUND_COLOR)

        # draw

        pygame.display.update()

    def update(self):
        # 更新
        pass

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.quit()

    def run(self):
        while True:
            self.handle_events()

            # update
            self.update()

            # draw
            self.update_screen()
            self.clock.tick(Settings.FPS)
