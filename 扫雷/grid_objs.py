from cocos.layer import ColorLayer

from settings import Settings
from color import *


class GridObject(ColorLayer):
    def __init__(self, pos, color):
        super().__init__(*color)

        self.position = pos.pos_to_position()
        self.width = Settings.grid_size - 1
        self.height = Settings.grid_size - 1


class Mine(GridObject):
    def __init__(self, pos):
        super().__init__(pos, color=RED)


class Flag(GridObject):
    def __init__(self, pos):
        super().__init__(pos, color=PALE_GREEN)

class Mask(GridObject):
    def __init__(self, pos):
        super().__init__(pos, color=WHITE)

