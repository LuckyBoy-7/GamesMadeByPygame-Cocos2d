from random import randint

from cocos.layer import ColorLayer
from cocos.text import Label
from cocos.actions import MoveTo

from settings import Settings
from stats import stats
from grid_id import *


class Grid(ColorLayer):
    def __init__(self, power, pos):
        self.power = power
        if self.power not in Settings.different_grid_color:
            Settings.different_grid_color[self.power] = (randint(0, 255), randint(0, 255), randint(0, 255), 255)

        super().__init__(*Settings.different_grid_color[self.power], Settings.GRID_SIZE - 1, Settings.GRID_SIZE - 1)

        self.applied_grids = set()  # 适用对象
        self.pos = pos
        self.anchor = self.width / 2, self.height / 2
        self.position = pos.pos_to_mid_position()
        self.label = self.create_label(2 ** power)

    def move_to(self, pos, game_layer):
        if pos != self.pos:
            game_layer.grids[self.pos] = None
            new_pos = pos
            self.update_pos(new_pos)
            game_layer.grids[new_pos] = self

    def update_pos(self, pos):
        self.do(MoveTo(pos.pos_to_mid_position(), Settings.move_time))
        self.pos = pos

    def update_score(self):
        stats.score += int(2 ** self.power)
        if stats.score > stats.best_score:
            stats.best_score = stats.score

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
        self.adjust_label(label)
        self.add(label, z=1)
        return label

    def adjust_label(self, label):
        while label.element.content_width > self.width or label.element.content_height > self.height:
            label.element.font_size -= 5


class NumGrid(Grid):
    def __init__(self, power, pos):
        super().__init__(power=power, pos=pos)

        self.applied_grids = {NumGrid, ReduceGrid, UniversalGrid}

    def exec(self, other, game_layer, pos):
        if type(other) in self.applied_grids:
            if isinstance(other, NumGrid):
                if other.power == self.power:
                    game_layer.double_grid(self.pos)
                    game_layer.del_grid(other.pos)
                else:
                    other.move_to(pos, game_layer)
            elif isinstance(other, ReduceGrid):
                if self.power > 1:
                    game_layer.reduce_grid(self.pos)
                    game_layer.del_grid(other.pos)
                else:
                    other.move_to(pos, game_layer)
            elif isinstance(other, UniversalGrid):
                game_layer.double_grid(self.pos)
                game_layer.del_grid(other.pos)
        else:  # 保证黑色方块不移动
            other.move_to(pos, game_layer)


class ReduceGrid(Grid):  # 1/2grid
    def __init__(self, power, pos):
        super().__init__(power=ReduceGrid_ID, pos=pos)  # 这里power随便反正用不到

        self.applied_grids = {NumGrid}

    def exec(self, other, game_layer, pos):
        if type(other) in self.applied_grids:
            if isinstance(other, NumGrid):
                if other.power > 1:
                    game_layer.del_grid(self.pos)
                    other.move_to(self.pos, game_layer)
                    game_layer.reduce_grid(self.pos)
                    # game_layer.del_grid(self.pos)
                    # game_layer.reduce_grid(other.pos)  # 隐性逻辑错误, reduce后找不到other了
                    # other.move_to(self.pos, game_layer)  # bug

                else:
                    other.move_to(pos, game_layer)
        else:
            other.move_to(pos, game_layer)


class UniversalGrid(Grid):  # 万能方块
    def __init__(self, power, pos):
        super().__init__(power=UniversalGrid_ID, pos=pos)
        self.label.element.text = "*2"
        self.adjust_label(self.label)

        self.applied_grids = {NumGrid}

    def exec(self, other, game_layer, pos):
        if type(other) in self.applied_grids:
            if isinstance(other, NumGrid):
                if other.power > 1:
                    game_layer.del_grid(self.pos)
                    other.move_to(self.pos, game_layer)
                    game_layer.double_grid(self.pos)

                else:
                    other.move_to(pos, game_layer)
        else:
            other.move_to(pos, game_layer)


class BlockGrid(Grid):  # 阻塞方块
    def __init__(self, power, pos):
        super().__init__(power=BlockGrid_ID, pos=pos)

        self.applied_grids = set()

    def exec(self, other, game_layer, pos):
        other.move_to(pos, game_layer)


class BoomGrid(Grid):  # 爆炸方块
    def __init__(self, power, pos):
        super().__init__(power=BoomGrid_ID, pos=pos)

        self.applied_grids = set()

    def exec(self, other, game_layer, pos):
        other.move_to(pos, game_layer)

# 失败的尝试
# class Grid(ColorLayer):
#     def not_blocked_pos(self, dest, grids):
#     delta = dest - self.pos
#     if delta.y > 0:  # up
#         for j in range(self.pos.y, dest.y + 1):
#             if isinstance(grids[Pos(self.pos.x, j)], BlockGrid):
#                 return Pos(self.pos.x, j - 1)
#     elif delta.y < 0:  # down
#         for j in range(dest.y, self.pos.y + 1):
#             if isinstance(grids[Pos(self.pos.x, j)], BlockGrid):
#                 return Pos(self.pos.x, j + 1)
#     elif delta.x > 0:  # right
#         for i in range(self.pos.x, dest.x + 1):
#             if isinstance(grids[Pos(i, self.pos.y)], BlockGrid):
#                 return Pos(i - 1, self.pos.y)
#     elif delta.x < 0:  # left
#         for i in range(dest.x, self.pos.x + 1):
#             if isinstance(grids[Pos(i, self.pos.y)], BlockGrid):
#                 return Pos(i + 1, self.pos.y)
#     return dest
