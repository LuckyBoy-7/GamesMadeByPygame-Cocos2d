from typing import List

import pygame

from .fonts import Fonts
from .stats import stats
from .settings import Settings
from .sounds import Sounds
from .timer import Timer


class ButtonItem(object):
    # 备份不会被修改, 拿来改别的
    bg_color = bg_color_backup = 127, 127, 127  # 背景色
    invalid_color = invalid_color_backup = 80, 80, 80  # 无法购买的背景色
    blink_color = blink_color_backup = 180, 180, 180  # 点击的闪烁色

    text_color = text_color_backup = 255, 255, 255

    edge_color = edge_color_backup = 0, 0, 0
    hovering_color = hovering_color_backup = 255, 255, 255

    item_len = 30  # 一个button bar(按钮条)的长度
    gap = 7  # 按钮之间的距离
    pivot_backup = pivot = gap  # 开始的y

    def __init__(self, outer: "Buttons", msg: str, costs: List[int], callback):
        self.font = Fonts.my_font(20)

        self.outer = outer  # 对buttons群组的引用
        self.msg = msg  # 按钮文本
        self.costs = costs  # 每次执行函数需花费的点数
        self.callback = callback  # 回调func

        self.cost_idx = 0

        self.text = self.get_text()
        self.rect = self.text.get_rect()
        self.width, self.height = self.text.get_size()
        self.rect.topleft = self.x, self.y = Settings.SCREEN_WIDTH - self.width, self.pivot
        self.__class__.pivot += self.height + self.gap

        self.is_blink = False
        self.blink_timer = Timer(time=5)

    def get_text(self):
        return self.font.render(f" {self.msg: <{self.item_len - 6}}{self.cost: >6}", False, self.text_color)

    @property
    def cost(self):
        return self.costs[self.cost_idx]

    def update_blink(self):
        if self.is_blink:
            self.bg_color = self.blink_color_backup
            if self.blink_timer.on_time():
                self.bg_color = self.bg_color_backup
                self.is_blink = False

    def blink(self):
        self.is_blink = True

    def kill(self):
        self.outer.items.remove(self)
        self.outer.update_pos()

    def update_click(self, pos):
        if self.rect.collidepoint(pos) and stats.harvest >= self.cost:
            self.callback()
            stats.harvest -= self.cost
            self.cost_idx += 1
            if self.cost_idx < len(self.costs):  # 还有新文本要显示
                self.text = self.get_text()
            else:
                self.kill()  # 移除此按钮

            Sounds.sound_button.play()
            self.blink()

    def update(self, pos):
        self.rect.topleft = self.x, self.y
        if self.rect.collidepoint(pos) and stats.harvest > self.cost:
            self.edge_color = self.hovering_color_backup
        else:
            self.edge_color = self.edge_color_backup
        self.bg_color = self.bg_color_backup if stats.harvest >= self.cost else self.invalid_color_backup
        self.update_blink()

    def draw(self, surface):
        # 按钮背景
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))
        # 按钮文本
        surface.blit(self.text, (self.x, self.y))
        # 按钮边框
        pygame.draw.line(surface, self.edge_color, start_pos=(self.x, self.y), end_pos=(self.x + self.width, self.y))
        pygame.draw.line(surface, self.edge_color, start_pos=(self.x, self.y), end_pos=(self.x, self.y + self.height))
        pygame.draw.line(surface, self.edge_color, start_pos=(self.x, self.y + self.height),
                         end_pos=(self.x + self.width, self.y + self.height))


class Buttons(object):
    def __init__(self, game):
        self.game = game

        self.items = [
            ButtonItem(self, "Expand Field", [5, 16, 32, 80], callback=self.expand_field),
            ButtonItem(self, "Auto Reaper", [25], callback=self.auto_reaper),
            ButtonItem(self, "Auto Seeder", [30], callback=self.auto_seeder),
            ButtonItem(self, "Better yield", [25, 60, 100, 150], callback=self.better_yield),
            ButtonItem(self, "Faster Plant Growth", [50, 100, 150, 200], callback=self.faster_plant_growth),
            ButtonItem(self, "???", [1200], callback=self.game_over)
        ]

        self.items.sort(key=lambda button: button.cost)

    def expand_field(self):
        self.game.grasslands.expand_field()  # grassland_cls
        self.game.auto_seeder.update_grasslands()
        self.game.auto_reaper.update_grasslands()
        Sounds.sound_expand.play()

    def auto_reaper(self):
        # 因为原bar已被删除, 所以这里sort没有关系
        self.game.auto_reaper.work()
        self.items.append(ButtonItem(self, "Faster Auto Reaper", [25, 50, 80], callback=self.faster_auto_reaper))
        self.items.sort(key=lambda button: button.cost)

    def auto_seeder(self):
        self.game.auto_seeder.work()
        self.items.append(ButtonItem(self, "Faster Auto Seeder", [30, 50, 80], callback=self.faster_auto_seeder))
        self.items.sort(key=lambda button: button.cost)

    def faster_auto_reaper(self):
        self.game.auto_reaper.work_timer.time -= Settings.FPS

    def faster_auto_seeder(self):
        self.game.auto_seeder.work_timer.time -= Settings.FPS

    def better_yield(self):
        self.game.grasslands[0].__class__.yield_ += 1

    def faster_plant_growth(self):
        cls = self.game.grasslands[0].__class__
        cls.t1, cls.t2 = cls.t1 - 1, cls.t2 - 1

    def game_over(self):  # 不想做结束画面了
        print("game_over!!!")

    def update_pos(self):
        pivot = ButtonItem.pivot_backup
        for item in self.items:
            item.y = pivot
            pivot += item.height + ButtonItem.gap

    def update(self, pos):  # 管理显示的
        for item in self.items:
            item.update(pos)

    def update_click(self, pos):  # 管理点击的
        for item in self.items:
            item.update_click(pos)

    def draw(self, surface):
        for item in self.items:
            item.draw(surface)


class Hint(object):
    def __init__(self):
        self.font = Fonts.my_font(50)

    def draw(self, surface):
        surface.blit(self.font.render(f"Harvest: {stats.harvest}", False, (255, 255, 255)), (0, 0))
