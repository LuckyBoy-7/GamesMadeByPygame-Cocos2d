import pygame
import sys


class Bird():
    def __init__(self, screen_size):
        self.image1 = pygame.image.load("images/bird1.png")
        self.image2 = pygame.image.load("images/bird2.png")
        self.status = [self.image1, self.image2]

        self.y = 200
        self.x = 50
        self.rect = self.image1.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        

        
        
        self.jump = False
        self.jumpspeed = 5
        self.gravity = 8
        self.dead = False


    def reset(self):
        self.rect.y = 200
        self.dead = False

    def update(self):
        if self.jump == True:
            self.rect.y -= self.jumpspeed
            self.jumpspeed -= 0.3

        else:
            self.rect[1] += self.gravity
            
            
        
