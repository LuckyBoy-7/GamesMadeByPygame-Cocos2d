import sys

import pygame
from pygame.locals import *

pygame.init()

from .settings import Settings
from .stats import stats
from .fonts import Fonts
from .sounds import *
from .skier import Skier
from .moving_objs import Tree, Flag


class SkiGame(object):
    def __init__(self):
        self.surface = pygame.display.set_mode(Settings.SCREEN_SIZE)

        # 初始化滑雪者
        self.skier = Skier()
        # 初始化障碍物(树)
        self.trees = pygame.sprite.Group([Tree() for _ in range(Settings.TREE_NUM)])
        self.flags = pygame.sprite.Group([Flag() for _ in range(Settings.FLAG_NUM)])

        self.clock = pygame.time.Clock()

    def draw_score(self):
        txt = Fonts.my_font(30).render(f"Score: {stats.score}", False, (0, 0, 0))
        self.surface.blit(txt, (0, 0))

    def draw_mid_txt(self, msg, font_size, color, delta_y):
        text = Fonts.my_font(font_size).render(msg, False, color)
        width, height = text.get_size()
        self.surface.blit(source=text,
                          dest=(Settings.SCREEN_MID_X - width // 2,
                                Settings.SCREEN_MID_Y - height // 2 + delta_y))

    def draw_welcome_text(self):
        self.draw_mid_txt("Welcome Player", 70, (255, 0, 0), -100)
        self.draw_mid_txt("This is a ski game", 40, (255, 0, 0), -30)
        self.draw_mid_txt("press any button to start!", 30, (0, 255, 0), 100)

    def update_screen(self):
        # 绘制屏幕
        self.surface.fill(Settings.BACKGROUND_COLOR)

        if stats.state == stats.WELCOME:
            self.draw_welcome_text()
        elif stats.state == stats.START:
            self.skier.draw(self.surface)
            self.flags.draw(self.surface)
            self.trees.draw(self.surface)
            self.draw_score()

        pygame.display.update()

    def update_collision(self):
        for tree in pygame.sprite.spritecollide(self.skier, self.trees, False, pygame.sprite.collide_mask):
            if not tree.is_crashed:
                tree.is_crashed = True
                self.skier.slipped()
                stats.score -= 5
        for flag in pygame.sprite.spritecollide(self.skier, self.flags, False, pygame.sprite.collide_mask):
            flag.reset_pos()
            stats.score += 2

    def update(self):
        if stats.state == stats.START:
            self.flags.update()
            self.trees.update()
            self.skier.update()
            self.update_collision()

    def handle_start_events(self, event):
        # 更新
        if stats.state == stats.START:
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.skier.turn(-1)
                elif event.key == K_RIGHT:
                    self.skier.turn(1)

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.quit()

            if stats.state == stats.WELCOME:
                # 处理欢迎事件
                if event.type == KEYDOWN:  # 按任意键开始
                    stats.state = stats.START
            elif stats.state == stats.START:
                # 处理游戏事件
                self.handle_start_events(event)

    def run(self):
        while True:
            self.handle_events()
            # update
            self.update()
            # draw
            self.update_screen()
            self.clock.tick(Settings.FPS)
