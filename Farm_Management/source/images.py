import pygame
from pygame import image

from .settings import Settings


class Images(object):
    pygame.display.set_mode(Settings.SCREEN_SIZE)

    arrow = image.load("./resources/images/arrow.png").convert_alpha()
    selected = image.load("./resources/images/selected.png").convert_alpha()
    valid_selected = image.load("./resources/images/valid_selected.png").convert_alpha()

    mud_left = image.load("./resources/images/mud_left.png").convert_alpha()
    mud_right = image.load("./resources/images/mud_right.png").convert_alpha()
    grass0 = image.load("./resources/images/grass0.png").convert_alpha()
    grass1 = image.load("./resources/images/grass1.png").convert_alpha()
    grass2 = image.load("./resources/images/grass2.png").convert_alpha()
    grass3 = image.load("./resources/images/grass3.png").convert_alpha()
    grass4 = image.load("./resources/images/grass4.png").convert_alpha()

    auto_reapers = [image.load(f"./resources/images/auto_reaper/auto_reaper{i}.png").convert_alpha()
                    for i in range(9)]

    auto_seeders = [image.load(f"./resources/images/auto_seeder/auto_seeder{i}.png").convert_alpha()
                    for i in range(9)]

    white_rect = image.load("./resources/images/white_rect.png").convert_alpha()
