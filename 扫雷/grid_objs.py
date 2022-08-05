from cocos.layer import ColorLayer

from settings import Settings


class GridObject(ColorLayer):
    def __init__(self, pos, color):
        super().__init__(*color)

        self.position = pos.pos_to_position()
        self.width = Settings.GRID_SIZE - 1
        self.height = Settings.GRID_SIZE - 1


class Mine(GridObject):
    def __init__(self, pos):
        super().__init__(pos, color=(255, 0, 0, 255))


class Flag(GridObject):
    def __init__(self, pos):
        super().__init__(pos, color=(0, 120, 0, 255))
