import pygame
from pygame.sprite import Sprite

from image import Image


class Bullet(Sprite):
    def __init__(self, hero_rect):
        super().__init__()
        self.image = Image.bullet
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.midtop = hero_rect.midtop

    def update(self):
        self.rect.top = -12

        if self.rect.bottom <= 0:
            self.kill()
