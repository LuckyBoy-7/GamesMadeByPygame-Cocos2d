from typing import Sequence

import pygame

from settings import Settings
from stats import stats


class Baffle(object):
    GAP_TO_BORDER = 30  # 板离边界的距离
    LENGTH = 100  # 板的长度
    THICKNESS = 5  # 板的厚度
    COLOR = 0, 255, 0, 255  # 板的颜色
    SPEED = 6  # 板的速度

    def __init__(self, surface, camp: str,
                 key_to_move_up: int = None,
                 key_to_move_down: int = None):
        self.screen = surface  # 在surface上绘制
        self.camp = camp  # 左 | 右
        self.x, self.y = self.get_position()  # 根据camp获取初始位置
        self.backup_x, self.backup_y = self.x, self.y  # 用于reset
        self.key_to_move_up = key_to_move_up  # 对应向上移动的响应按键
        self.key_to_move_down = key_to_move_down  # 对应向下移动的响应按键

    def get_position(self):
        y = Settings.HEIGHT // 2 - self.LENGTH
        if self.camp == "left":
            x = self.GAP_TO_BORDER
        elif self.camp == "right":
            x = Settings.WIDTH - (self.GAP_TO_BORDER + self.THICKNESS)
        else:
            raise TypeError("Unknown Camp")

        return x, y

    def update(self, keys: Sequence[bool]):
        if keys[self.key_to_move_up]:  # 向上移动且不会移出边界
            self.y = max(0, self.y - self.SPEED)
            stats.is_start = True
        elif keys[self.key_to_move_down]:  # 向下移动且不会移出边界
            self.y = min(Settings.HEIGHT - self.LENGTH, self.y + self.SPEED)
            stats.is_start = True

    def get_rect(self):
        return pygame.rect.Rect(self.x, self.y, self.THICKNESS, self.LENGTH)

    def draw(self):
        pygame.draw.rect(surface=self.screen, color=self.COLOR,
                         rect=self.get_rect(), width=0)

    def reset(self):
        self.x, self.y = self.backup_x, self.backup_y


class AI(Baffle):
    def __init__(self, surface):
        super().__init__(surface, "left")
        import math
