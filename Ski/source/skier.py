import pygame.mask
from pygame.sprite import Sprite
import pygame

from .settings import Settings
from .images import Images
from .moving_objs import MovingObj


class Skier(Sprite):
    def __init__(self):
        super().__init__()

        self.image_key = 0

        self.images = Images.skier
        self.masks = {key: pygame.mask.from_surface(img) for key, img in self.images.items()}

        self.mask = self.masks[self.image_key]
        self.image = self.images[self.image_key]
        self.rect = self.image.get_rect()
        self.rect.midtop = Settings.SCREEN_MID_X, 100

        self.speed_x = 0

        pivot = MovingObj.SPEED  # 物体的移速, 相当于自己的移速
        self.obj_speed = {0: pivot, 1: pivot - 1, 2: pivot - 2}

        self.slip_elapse = 0
        self.is_slipped = False

    def update_(self):
        self.image = self.images[self.image_key]
        MovingObj.SPEED = self.obj_speed[abs(self.image_key)]
        self.speed_x = self.image_key
        self.mask = self.masks[self.image_key]
        self.is_slipped = False

    def update(self):
        # 更新水平方向速度, 并且不出界
        if self.speed_x > 0:
            self.rect.x = min(self.rect.x + self.speed_x, Settings.SCREEN_WIDTH - self.image.get_width())
        elif self.speed_x < 0:
            self.rect.x = max(self.rect.x + self.speed_x, 0)
        self.rect.x += self.speed_x  # 补偿: 水平方向更丝滑

        if self.is_slipped:
            # pygame.time.delay(1000)  # 骚操作
            self.image = Images.skier_slipped
            MovingObj.SPEED = 0
            self.speed_x = 0

            self.slip_elapse += 1
            if self.slip_elapse == 30:
                self.slip_elapse = 0

                self.update_()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def turn(self, direct):
        if self.is_slipped:
            return

        if direct > 0:
            self.image_key = min(2, self.image_key + direct)
        else:
            self.image_key = max(-2, self.image_key + direct)
        self.update_()

    def slipped(self):
        self.is_slipped = True
