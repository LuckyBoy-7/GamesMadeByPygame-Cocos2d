import pygame
import sys
from random import *
pygame.init()
    
size = (900, 512)
screen = pygame.display.set_mode(size)
color = (0, 0, 0)


image = pygame.image.load("../../images/pipeline.png")
rect = image.get_rect()


y = randint(100, 400)
x = 660
rect = image.get_rect()
rect.x, rect.bottom = x, y
clock = pygame.time.Clock()
while True:
    screen.fill((0, 0, 0))
    rect.x -= 6
    screen.blit(image, rect)

    pygame.display.flip()
    clock.tick(60)
