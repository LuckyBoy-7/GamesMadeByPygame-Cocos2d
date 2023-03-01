from random import randint

import pygame.transform
from .images import Images
from .timer import Timer


class WhiteRect(object):
    def __init__(self, pos, speed, size=(10, 10), frame=20):
        self.pos = pos[0] + randint(-5, 5), pos[1] + randint(-5, 5)  # 对应位置加上x,y方向上的扰动(即偏移)
        self.speed = speed

        self.image = pygame.transform.scale(Images.white_rect, size)
        self.rect = self.image.get_rect(topleft=self.pos)

        self.opacity = 255
        self.opacity_delta = self.opacity / frame  # 每一帧透明度的减少量

    def update(self):
        self.image.set_alpha(self.opacity)
        self.rect.move_ip(*self.speed)  # 飞溅
        self.opacity -= self.opacity_delta

class WhiteExplode(object):
    particle_num = 8  # 粒子数量
    active_frame = 23  # 存活时间

    def __init__(self, pos, outer):
        self.pos = pos
        self.outer = outer  # kill自己用
        self.particles = [WhiteRect(self.pos, (randint(-1, 1), randint(-2, 1)), frame=self.active_frame)
                          for _ in range(self.particle_num)]

        self.dead_timer = Timer(time=self.active_frame)  # 死亡倒计时

    def update(self):
        for p in self.particles:
            p.update()

        if self.dead_timer.on_time():
            self.outer.reaped_animation_items_removed.add(self)

    def draw(self, surface):
        for p in self.particles:
            surface.blit(p.image, p.rect)
