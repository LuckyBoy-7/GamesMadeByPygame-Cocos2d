import pygame
from pygame import image

from .settings import Settings


class Images(object):
    pygame.display.set_mode(Settings.SCREEN_SIZE)

    # 旗杆
    flag = image.load("./resources/images/flag.png").convert_alpha()
    # 树
    tree = image.load("./resources/images/tree.png").convert_alpha()
    # 人
    skier_forward = image.load("./resources/images/skier_forward.png").convert_alpha()
    skier_slipped = image.load("./resources/images/skier_slipped.png").convert_alpha()
    skier_left1 = image.load("./resources/images/skier_left1.png").convert_alpha()
    skier_left2 = image.load("./resources/images/skier_left2.png").convert_alpha()
    skier_right1 = image.load("./resources/images/skier_right1.png").convert_alpha()
    skier_right2 = image.load("./resources/images/skier_right2.png").convert_alpha()
    skier = {i: img for i, img in
             zip(range(-2, 3), [skier_left2, skier_left1,
                                skier_forward,
                                skier_right1, skier_right2])}
