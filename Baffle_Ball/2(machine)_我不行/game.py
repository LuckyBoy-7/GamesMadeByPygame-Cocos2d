import sys

import pygame
from pygame.locals import *

from settings import Settings
from baffle import Baffle
from stats import stats
from ball import Ball
from prompt import HpPrompt


class BaffleBall(object):
    def __init__(self):
        # 初始化pygame
        pygame.init()

        # 初始化屏幕
        self.surface = pygame.display.set_mode(Settings.SIZE)

        # 初始化板
        self.left_baffle = Baffle(surface=self.surface, camp="left", key_to_move_up=K_w, key_to_move_down=K_s)
        self.right_baffle = Baffle(surface=self.surface, camp="right", key_to_move_up=K_UP, key_to_move_down=K_DOWN)

        # 初始化球
        self.ball = Ball(surface=self.surface, baffles=[self.left_baffle, self.right_baffle])

        # 初始化生命条
        self.left_hp_prompt = HpPrompt(surface=self.surface, camp="left")
        self.right_hp_prompt = HpPrompt(surface=self.surface, camp="right")

        # 初始化帧率
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.key_down = pygame.key.get_pressed()
            # 处理事件队列:
            self.handle_events()

            # 处理更新(如果游戏开始的话[对有些来说])
            self.left_baffle.update(self.key_down)
            self.right_baffle.update(self.key_down)
            if stats.is_start:
                self.ball.update()
                self.left_hp_prompt.update()
                self.right_hp_prompt.update()
                self.handle_game_over()

            # 处理绘制
            self.update_screen()
            self.clock.tick(Settings.TICK)

    def draw_mid_line(self):
        pygame.draw.line(self.surface, (255, 255, 255),
                         start_pos=(Settings.WIDTH // 2, 0),
                         end_pos=(Settings.WIDTH // 2, Settings.HEIGHT))

    def handle_game_over(self):
        if stats.game_over:
            self.reset()

    def reset(self):
        self.left_baffle.reset()
        self.right_baffle.reset()
        self.ball.reset()
        stats.game_over = False
        stats.is_start = False

    @staticmethod
    def exit_():
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:  # 点叉叉时
                self.exit_()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exit_()

    def update_screen(self):
        # 绘制背景
        self.surface.fill((127, 127, 127, 255))

        self.draw_mid_line()
        # 绘制小球
        self.ball.draw()

        # 绘制挡板
        self.left_baffle.draw()
        self.right_baffle.draw()

        # 绘制生命条
        self.left_hp_prompt.draw()
        self.right_hp_prompt.draw()

        # 更新
        pygame.display.flip()
