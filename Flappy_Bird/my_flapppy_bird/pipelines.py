import pygame
import sys
from random import *


class UpPipeline(pygame.sprite.Sprite):  
    def __init__(self, screen, y):
        super().__init__()
        self.image = pygame.image.load("images/pipeline.png").convert_alpha()
        self.screen_size = screen
        
        self.rect = self.image.get_rect()
        self.y = y
        self.x = self.screen_size[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.bottom = self.x, self.y


    def update(self):
            self.rect.x -= 6



class DownPipeline(pygame.sprite.Sprite):  
    def __init__(self, screen, y):
        super().__init__()
        self.image = pygame.image.load("images/pipeline.png").convert_alpha()
        self.screen_size = screen
        
        self.rect = self.image.get_rect()
        self.y = y
        self.x = self.screen_size[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y


    def update(self):
            self.rect.x -= 6
