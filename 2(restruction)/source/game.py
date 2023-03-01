import sys

import pygame
from pygame.locals import *

pygame.init()

from .settings import Settings
from .grassland import GrassLandGroup, AutoReaper, AutoSeeder
from .images import Images
from .sounds import *
from .widget import Buttons, Hint


class FarmManagementGame(object):
    def __init__(self):
        self.surface = pygame.display.set_mode(Settings.SCREEN_SIZE)

        self.grasslands = GrassLandGroup()  # 草地组群
        self.arrow = self.get_arrow()  # 鼠标箭头, 主要记录位置进行检测碰撞, 因为除了mask我真不知道还有什么方法
        self.auto_reaper = AutoReaper(self.grasslands)  # 自动收割对象
        self.auto_seeder = AutoSeeder(self.grasslands)  # 自动种植对象
        self.buttons = Buttons(self)  # 按钮对象
        self.hint = Hint()  # 提示对象

        self.clock = pygame.time.Clock()  # 控制帧率

    @staticmethod
    def get_arrow():
        mouse = pygame.sprite.Sprite()
        mouse.image = Images.arrow
        mouse.rect = mouse.image.get_rect()
        mouse.mask = pygame.mask.from_surface(mouse.image)
        return mouse

    def update_screen(self):
        # 绘制屏幕
        self.surface.fill(Settings.BACKGROUND_COLOR)

        # draw
        self.grasslands.draw(self.surface)
        self.auto_reaper.draw(self.surface)
        self.auto_seeder.draw(self.surface)
        self.grasslands.draw_later(self.surface)
        self.buttons.draw(self.surface)
        self.hint.draw(self.surface)

        pygame.display.update()

    def update(self):
        # 更新
        self.auto_reaper.update()
        self.auto_seeder.update()
        self.grasslands.update()
        self.buttons.update(self.arrow.rect.topleft)

    def handle_mouse_button_down_event(self, event):
        self.buttons.update_click(event.pos)  # button的亮暗, 响应等要更新
        for grassland in self.grasslands:
            if not grassland.occupied and pygame.sprite.collide_mask(grassland, self.arrow):
                if grassland.state == grassland.empty:
                    grassland.seed()
                elif grassland.state == grassland.mature:
                    grassland.reap()

    def handle_key_down_event(self, event):
        if event.key == K_RETURN:
            for g in self.grasslands:
                g.handle_growth()
        elif event.key == K_a:
            self.auto_reaper.work()
        elif event.key == K_s:
            self.auto_seeder.work()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    def handle_mouse_move(self):
        self.arrow.rect.topleft = pygame.mouse.get_pos()
        for grassland in self.grasslands:
            if pygame.sprite.collide_mask(grassland, self.arrow):
                grassland.selected()
            else:
                grassland.unselected()

    def handle_events(self):
        self.handle_mouse_move()  # 鼠标的位置要一直更新
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # 退出
                self.quit()
            if event.type == KEYDOWN:  # 调试
                self.handle_key_down_event(event)
            elif event.type == MOUSEBUTTONDOWN:  # 点击
                self.handle_mouse_button_down_event(event)

    def run(self):
        while True:
            self.handle_events()

            # update
            self.update()
            # draw
            self.update_screen()

            self.clock.tick(Settings.FPS)
