import sys

import pygame
from pygame.locals import *

from settings import Settings
from draw import Lines, Grids, Prompts
from stats import stats
from music import Music


class Game(object):
    """
    D F J K对应四个键
    """

    def __init__(self):
        super(Game, self).__init__()

        pygame.init()  # pygame实例化

        self.surface = pygame.display.set_mode(Settings.SIZE)  # 生成windows(窗口)对象
        pygame.display.set_caption("Don't Tap The White Tile")  # 设置标题

        self.lines = Lines(self.surface)  # 创建线条
        self.grids = Grids(self.surface)  # 创建黑块
        self.music = Music()  # 控制音乐
        self.score_prompt = Prompts(self.surface, self.music)  # 创建计分板

        self.clock = pygame.time.Clock()  # 设置帧率

    def run(self) -> None:
        while True:
            # 处理时间队列
            self.handle_events()

            # 处理更新
            self.lines.update()
            self.grids.update()
            self.score_prompt.update()
            self.music.elapse()

            # 处理绘制
            self.update_screen()

            self.clock.tick(Settings.TICK)

    def update_screen(self) -> None:
        self.surface.fill((200, 200, 200, 255))  # 一定要先涂背景色

        self.lines.draw()  # 绘制
        self.grids.draw()
        self.score_prompt.draw()

        pygame.display.flip()  # 更新

    @staticmethod
    def handle_exit() -> None:  # 清理工作
        pygame.quit()
        sys.exit()

    def key_match(self, key) -> bool:  # 这个按键对应的col是否与黑块的匹配
        if key in self.grids.match and self.grids.match[key] == self.grids.grids[self.grids.current_grid_idx].col:
            return True
        return False

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.handle_exit()
            if event.type == KEYDOWN:
                self.handle_key_down(event)

    def handle_key_down(self, event: pygame.event.Event) -> None:
        if event.key == K_ESCAPE:
            self.handle_exit()

        if self.key_match(pygame.key.name(event.key)):
            stats.right_tap += 1
            stats.combo = stats.combo + 1
            self.lines.move()
            self.grids.move()
            self.music.compensate_elapse()
        else:
            stats.wrong_tap += 1
            stats.combo = 0
            self.music.elapse(more_punish=True)
            self.grids.show_wrong_grid(pygame.key.name(event.key))

