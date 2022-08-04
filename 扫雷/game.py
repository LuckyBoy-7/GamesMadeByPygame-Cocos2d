"""
todo: 1. 数字颜色
      2. 遮盖
"""

from random import sample, randint

from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.draw import Line
from cocos.text import Label


class GameScene(Scene):
    def __init__(self):
        super().__init__()

        self.add(ColorLayer(255, 255, 255, 255), z=0)
        self.add(GameLayer(), z=1)


class _GameConfigure(object):
    GRID_SIZE = 40

    def __init__(self):
        self.rows = 8
        self.columns = 8

        self.origin = (int(director.get_window_size()[0] / 2 - self.columns / 2 * _GameConfigure.GRID_SIZE),
                       int(director.get_window_size()[1] / 2 - self.rows / 2 * _GameConfigure.GRID_SIZE))


class GameLayer(Layer):
    masks: dict

    is_event_handler = True

    def __init__(self):
        super().__init__()

        # 棋盘基本信息
        self.config = _GameConfigure()
        # 绘制棋盘
        self.grids = {Pos((x, y), self.config): None
                      for x in range(self.config.columns)
                      for y in range(self.config.rows)}
        self.draw_grids()
        # 布置雷(mine)
        self.place_mines(num=10)
        # 设置数字
        self.set_nums()
        # 设置遮盖
        self.set_masks()

    def on_mouse_press(self, x, y, button, _):
        pos = Pos.position_to_pos(x, y, self.config)
        if button == 1:  # 点击左键
            if pos in self.masks:
                if isinstance(self.masks[pos], ColorLayer):
                    self.remove(self.masks[pos])
                    self.masks[pos] = -1
                    if self.grids[pos] is Mine:
                        print("Game Over")

    def set_masks(self):
        self.masks = {Pos((x, y), self.config): None
                      for x in range(self.config.columns)
                      for y in range(self.config.rows)}
        for x in range(self.config.columns):
            for y in range(self.config.rows):
                mask = ColorLayer(127, 127, 127, 255, width=self.config.GRID_SIZE - 1, height=self.config.GRID_SIZE - 1)
                mask.position = Pos((x, y), self.config).pos_to_position()
                self.add(mask)
                self.masks[(x, y)] = mask

    def draw_grids(self):
        for x in range(self.config.columns + 1):
            self.add(Line(start=(self.config.origin[0] + x * self.config.GRID_SIZE, self.config.origin[1]),
                          end=(self.config.origin[0] + x * self.config.GRID_SIZE,
                               self.config.origin[1] + self.config.rows * self.config.GRID_SIZE),
                          color=(0, 0, 0, 255)))
        for y in range(self.config.rows + 1):
            self.add(Line(start=(self.config.origin[0], self.config.origin[1] + y * self.config.GRID_SIZE),
                          end=(self.config.origin[0] + self.config.columns * self.config.GRID_SIZE,
                               self.config.origin[1] + y * self.config.GRID_SIZE),
                          color=(0, 0, 0, 255)))

    def place_mines(self, num=10):
        mine_poses = sample(list(self.grids), num)

        for pos in mine_poses:
            self.grids[pos] = Mine
            self.add(Mine(pos))

    def set_nums(self):
        for pos in self.grids:
            if self.grids[pos] is not Mine:
                mines = pos.search_mines(self.grids)
                if mines:
                    self.create_label(pos, mines)

    def create_label(self, pos, num):
        color = [(0, 0, 255, 255),
                 (0, 255, 0, 255),
                 (255, 0, 0, 255),
                 (0, 0, 104, 255)]
        if num <= 4:
            chosen_color = color[num - 1]
        else:
            chosen_color = (randint(0, 255), randint(0, 255), randint(0, 255), 255)
        label = Label(
            text=f"{num}",
            position=pos.pos_to_mid_position(),
            font_size=30,
            color=chosen_color,
            anchor_x="center",
            anchor_y="center"
        )
        self.add(label)


class Pos(object):
    def __init__(self, pos, config):
        self.pos = pos
        self.config = config

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def pos_to_position(self):
        return self.pos[0] * self.config.GRID_SIZE + self.config.origin[0], \
               self.pos[1] * self.config.GRID_SIZE + self.config.origin[1]

    def pos_to_mid_position(self):
        return (self.pos[0] + 0.5) * self.config.GRID_SIZE + self.config.origin[0], \
               (self.pos[1] + 0.5) * self.config.GRID_SIZE + self.config.origin[1]

    @staticmethod
    def position_to_pos(x, y, config):
        return (x - config.origin[0]) // config.GRID_SIZE, (y - config.origin[1]) // config.GRID_SIZE

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        if isinstance(other, tuple):
            if self.pos == other:
                return True
        if isinstance(other, Pos):
            if self.pos == other.pos:
                return True
        return False

    def search_mines(self, grids):
        mines_count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if self.check_valid(self.x + i, self.y + j) and not (self.x + i, self.y + j) == self.pos:
                    if grids[(self.x + i, self.y + j)] is Mine:
                        mines_count += 1
        return mines_count

    def check_valid(self, x, y):
        if x < 0 or x >= self.config.rows or y < 0 or y >= self.config.columns:
            return False
        return True


class Mine(ColorLayer):
    def __init__(self, pos: Pos):
        super().__init__(255, 0, 0, 255)

        self.position = pos.pos_to_position()
        self.width = pos.config.GRID_SIZE - 1
        self.height = pos.config.GRID_SIZE - 1
