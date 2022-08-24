from random import randint
from math import log

from cocos.layer import ColorLayer
from cocos.text import Label
from cocos.actions import MoveTo

from settings import Settings
from position import Pos


class Grid(ColorLayer):
    def __init__(self, power, pos):
        self.power = power
        if self.power > len(Settings.different_grid_color):
            Settings.different_grid_color.append((randint(0, 255), randint(0, 255), randint(0, 255), 255))

        super().__init__(*Settings.different_grid_color[self.power - 1], Settings.GRID_SIZE - 1, Settings.GRID_SIZE - 1)

        self.pos = pos
        self.anchor = self.width / 2, self.height / 2
        self.position = pos.pos_to_mid_position()
        self.create_label(2 ** power)

    def move_to(self, pos, game_layer):
        if pos != self.pos:
            game_layer.grids[self.pos] = None
            self.update_pos(pos)
            game_layer.grids[pos] = self

    def update_pos(self, pos):
        self.do(MoveTo(pos.pos_to_mid_position(), 0.4))
        self.pos = pos

    def create_label(self, num):
        if num <= 4:
            color = 160, 151, 141, 255
        else:
            color = 249, 246, 242, 255
        label = Label(text=f"{num}",
                      font_size=100,
                      color=color,
                      anchor_x="center",
                      anchor_y="center")
        label.position = self.width / 2, self.width / 2 + 5
        while label.element.content_width > self.width or label.element.content_height > self.height:
            label.element.font_size -= 5

        self.add(label, z=1)
        return label
