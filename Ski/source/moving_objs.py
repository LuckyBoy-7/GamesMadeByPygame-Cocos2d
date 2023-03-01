from random import randint

from pygame.sprite import Sprite

from .images import Images
from .settings import Settings


class MovingObj(Sprite):
    SPEED = 6

    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.reset_pos()

    def reset_pos(self):
        self.rect.x = randint(0, Settings.SCREEN_WIDTH - self.image.get_width())
        self.rect.y = randint(Settings.SCREEN_HEIGHT, Settings.SCREEN_HEIGHT * 3)

    def move(self):
        self.rect.centery -= self.SPEED
        if self.rect.bottom < 0:
            self.reset_pos()

    def update(self):
        self.move()


class Tree(MovingObj):
    def __init__(self):
        super().__init__(Images.tree)

        self.is_crashed = False

    def reset_pos(self):
        super().reset_pos()
        self.is_crashed = False


class Flag(MovingObj):
    def __init__(self):
        super().__init__(Images.flag)
