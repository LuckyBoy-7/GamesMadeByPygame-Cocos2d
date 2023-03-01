from random import randint, sample

import pygame.transform
from .images import Images
from pygame.sprite import Sprite

from .settings import Settings
from .stats import stats
from .sounds import Sounds
from .particle import WhiteExplode
from .timer import Timer


def tuple_add(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1]


class Zoom(Sprite):
    def __init__(self, img, size, **kwargs):
        super().__init__()

        self.size = size[0] * 4, size[1] * 4

        self.image = pygame.transform.scale(img, (size[0] * 4, size[1] * 4))
        self.rect = self.image.get_rect(**kwargs)
        # self.width, self.height = self.rect.size
        # self.hf_w, self.hf_h = self.width / 2, self.height / 2  # 一半


class Grass(Zoom):
    # 32 * 16
    # (32 * 16) * 4 == 128, 64
    def __init__(self, img, position):
        if img != Images.grass0:
            super().__init__(img, size=(32, 32), midleft=position)
        else:
            super().__init__(img, size=(32, 16), topleft=position)


class MudLeft(Zoom):
    # 16 * 16
    # (16 * 16) * 4 == 64, 64
    def __init__(self, position):
        super().__init__(Images.mud_left, size=(16, 32), bottomleft=position)


class MudRight(Zoom):
    def __init__(self, position):
        super().__init__(Images.mud_right, size=(16, 32), bottomleft=position)


class Selected(Zoom):
    # 32 * 16
    # (32 * 16) * 4 == 128, 64
    def __init__(self, position):
        super().__init__(Images.selected, size=(32, 16), bottomleft=position)


class ValidSelected(Zoom):
    # 32 * 16
    # (32 * 16) * 4 == 128, 64
    def __init__(self, position):
        super().__init__(Images.valid_selected, size=(32, 16), bottomleft=position)


class GrassLand(object):
    yield_ = 1
    empty, born, start_grow, taller, mature = range(5)
    t1, t2 = 8, 16

    def __init__(self, position):
        super().__init__()
        self.state = 4
        self.grasses = {n: Grass(eval(f"Images.grass{n}"), position)
                        for n in range(5)}  # grass是本体, mud是装饰
        self.mask = pygame.mask.from_surface(self.grasses[0].image)
        self.rect = self.grasses[0].rect
        self.position_backup = self.rect.topleft
        self.width, self.height = self.rect.size
        self.hf_w, self.hf_h = self.width / 2, self.height / 2  # 一半

        # 把mud拼上去
        x, y = self.rect.bottomleft
        self.mud_left = MudLeft((x, y + self.hf_h))
        self.mud_right = MudRight((x + self.hf_w, y + self.hf_h))

        # 把选中光圈拼上去
        self.selected_hint = Selected((x, y))
        self.valid_selected_hint = ValidSelected((x, y))
        self.is_selected = False

        self.time = randint(self.t1 * Settings.FPS, self.t2 * Settings.FPS)
        self.growth_timer = Timer(time=self.time, )  # growth timer

        self.occupied = False  # 被自动对象占用时, 鼠标无法点击他们

        self.reaped_animation_items = set()  # 存放粒子效果
        self.reaped_animation_items_removed = set()

    def selected(self):
        self.is_selected = True

    def unselected(self):
        self.is_selected = False

    def draw(self, surface):
        surface.blit(self.mud_left.image, self.mud_left.rect)
        surface.blit(self.mud_right.image, self.mud_right.rect)
        # 初始empty草皮要一直显示, 其他根据状态再画
        surface.blit(self.grasses[0].image, self.rect)

    def draw_later(self, surface):
        if self.is_selected:
            if self.state in (self.empty, self.mature):
                surface.blit(self.valid_selected_hint.image, self.valid_selected_hint.rect)
            else:
                surface.blit(self.selected_hint.image, self.selected_hint.rect)

        if self.state != self.empty:
            surface.blit(self.grasses[self.state].image, self.grasses[self.state].rect)

        if self.reaped_animation_items:
            for effect in self.reaped_animation_items:
                effect.draw(surface)

    def update_reaped_animation(self):
        for effect in self.reaped_animation_items:
            effect.update()
        for effect in self.reaped_animation_items_removed:
            self.reaped_animation_items.remove(effect)
        self.reaped_animation_items_removed.clear()

    def update_position(self):
        # O(grassland_part * grasslands_num * frames) -> O(grassland_part * grasslands_num * gen_grasslands_times)
        if self.position_backup != self.rect.topleft:
            self.mud_left.rect.midleft = self.rect.move((0, self.hf_h)).topleft
            self.mud_right.rect.midleft = self.rect.move((self.hf_w, self.hf_h)).topleft
            self.selected_hint.rect.bottomleft = self.rect.bottomleft
            self.valid_selected_hint.rect.bottomleft = self.rect.bottomleft
            for g in self.grasses.values():
                g.rect.bottomleft = self.rect.bottomleft
        self.position_backup = self.rect.topleft

    def update(self):
        # 自己本应该不断更新自己, 不要拿别人更新自己, 不为效率改变, 易读性(或可在函数里优化)
        self.update_position()
        self.update_reaped_animation()
        if self.growth_timer.on_time():
            self.handle_growth()

    def handle_growth(self):
        if self.state not in (self.empty, self.mature):
            self.grow()

    def grow(self):
        self.state += 1

    def reap(self):
        self.state = 0
        stats.harvest += self.yield_
        self.reset()

        Sounds.sound_reap.play()
        self.reaped_animation_items.add(WhiteExplode(self.rect.center, self))

    def seed(self):
        self.state = 1

        Sounds.sound_seed.play()

    def reset_speed(self):
        self.time = randint(self.t1 * Settings.FPS, self.t2 * Settings.FPS)

    def reset(self):
        self.occupied = False


class GrassLandGroup(object):
    def __init__(self):
        self.grassland_num = 6
        self.grasslands = []
        self.gen_grasslands()

    @property
    def start_pos(self):
        return (Settings.SCREEN_WIDTH - 128 * self.grassland_num) // 2, \
               (Settings.SCREEN_HEIGHT - 64 * self.grassland_num) // 2

    def expand_field(self):
        self.grassland_num += 1
        self.gen_grasslands()

    def gen_grasslands(self):
        width, height = Grass(Images.grass0, (0, 0)).size
        hf_w, hf_h = width / 2, height / 2  # 一半

        n = self.grassland_num
        while len(self.grasslands) < n ** 2:
            self.grasslands.append(GrassLand((0, 0)))
        start = tuple_add(((n - 1) * hf_w, 0), self.start_pos)

        idx = 0
        for i in range(n):
            pivot = start[0] - i * hf_w, start[1] + i * hf_h
            for j in range(i + 1):
                x, y = pivot[0] + j * width, pivot[1]
                self.grasslands[idx].rect.topleft = x, y
                idx += 1

        start = tuple_add(((n - 1) * hf_w, (n - 1) * height), self.start_pos)
        for i in range(n - 2, -1, -1):  # [0, n - 2] 共 n - 1 个
            pivot = start[0] - i * hf_w, start[1] - i * hf_h
            for j in range(i + 1):
                x, y = pivot[0] + j * width, pivot[1]
                self.grasslands[idx].rect.topleft = x, y
                idx += 1

    def update(self):
        for grassland in self.grasslands:
            grassland.update()

    def draw(self, surface):
        for grassland in self.grasslands:
            grassland.draw(surface)

    def draw_later(self, surface):
        for grassland in self.grasslands:
            grassland.draw_later(surface)

    def __iter__(self):
        return iter(self.grasslands)

    def __len__(self):
        return len(self.grasslands)

    def __getitem__(self, item):
        return self.grasslands[item]


class Auto(object):
    def __init__(self, images, grasslands, target_attr: int, callback: str, position=(-1000, -1000)):
        self.images = images
        for i, img in enumerate(self.images):
            self.images[i] = pygame.transform.scale(img, (32 * 4, 16 * 4))

        self.img_idx = 0  # 更新动画
        self.image = self.images[self.img_idx]
        self.rect = self.image.get_rect(topleft=position)

        self.orig_grasslands = grasslands
        self.grasslands = sample(list(grasslands), len(grasslands))  # 让收割(播种)对象更加随机, 同时在扩张时更新

        self.target_attr = target_attr
        self.callback = callback

        self.animation_timer = Timer(time=10)

        self.is_work = False  # 是否要工作
        self.is_working = False  # 是否正在工作
        self.work_timer = Timer(time=4 * Settings.FPS)  # 工作时间(管速度)
        self.target = None

    def update(self):
        if not self.is_work:
            return

        self.update_animation()
        if not self.is_working:
            for grassland in self.grasslands:
                if grassland.state == self.target_attr:
                    grassland.occupied = True
                    self.rect.bottomleft = grassland.rect.bottomleft
                    self.is_working = True
                    self.target = grassland
                    break
        elif self.work_timer.on_time():
            eval(f"self.target.{self.callback}()")
            self.is_working = False
            self.rect.bottomleft = -1000, -1000

    def update_grasslands(self):
        self.grasslands = sample(list(self.orig_grasslands), len(self.orig_grasslands))

    def update_animation(self):
        if self.animation_timer.on_time():
            self.img_idx = (self.img_idx + 1) % len(self.images)
            self.image = self.images[self.img_idx]

    def work(self):
        self.is_work = True

    def draw(self, surface):
        if self.is_work:
            surface.blit(self.image, self.rect)


class AutoReaper(Auto):
    def __init__(self, grasslands):
        grassland = grasslands[0]
        super().__init__(Images.auto_reapers, grasslands, target_attr=grassland.mature, callback="reap")


class AutoSeeder(Auto):
    def __init__(self, grasslands):
        grassland = grasslands[0]
        super().__init__(Images.auto_seeders, grasslands, target_attr=grassland.empty, callback="seed")
