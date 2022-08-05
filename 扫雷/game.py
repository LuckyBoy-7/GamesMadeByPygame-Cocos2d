from random import sample, randint

from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.draw import Line
from cocos.text import Label
from cocos.actions import Blink

from settings import Settings
from grid_objs import Mine, Flag
from position import Pos


class GameScene(Scene):
    def __init__(self):
        super().__init__()

        self.add(ColorLayer(255, 255, 255, 255), z=0)
        self.add(GameLayer(), z=1)


class GameLayer(Layer):
    up_masks: dict
    down_masks: dict
    grids: dict
    is_first_click: bool

    is_event_handler = True

    def __init__(self):
        super().__init__()

        # 绘制棋盘
        self.draw_grids()
        # 设置flag信息
        self.flags = {Pos((x, y)): None
                      for x in range(Settings.COLUMNS)
                      for y in range(Settings.ROWS)}

        self.grids = {Pos((x, y)): None
                      for x in range(Settings.COLUMNS)
                      for y in range(Settings.ROWS)}
        self.is_first_click = True
        # 设置遮盖
        self.set_masks()

    def on_mouse_press(self, x, y, button, _):
        pos = Pos.position_to_pos(x, y)
        if pos in self.grids:
            if button == 1:  # 点击左键
                if pos in self.up_masks and self.up_masks[pos] is not None:  # 点到棋盘内未点击区
                    if self.is_first_click:
                        # 布置雷(mine)
                        self.place_mines(Settings.MINE_NUMS, pos)
                        # 设置数字
                        self.set_nums()
                        self.recursively_expand(pos)
                    elif isinstance(self.up_masks[pos], ColorLayer):
                        if self.grids[pos] is Mine:
                            self.show_all_mines()
                        elif self.grids[pos] is None:
                            self.recursively_expand(pos)
                        self.remove_mask(pos)
                elif pos.get_mask_nearby(self.up_masks):
                    if self.grids[pos]:
                        if pos.count_flags(self.flags) >= self.grids[pos]:
                            pos.auto_remove(self.flags, self)
                        else:
                            self.grid_blink(pos)

            elif button == 4:  # 点击右键
                if self.up_masks[pos] is not None:  # 只能在未点击的地方点
                    if self.flags[pos] is None:
                        flag = Flag(pos)
                        self.add(flag, z=100)
                        self.flags[pos] = flag
                    else:
                        self.remove(self.flags[pos])
                        self.flags[pos] = None

    def clear(self):
        for _, child in self.children:
            if isinstance(child, (Mine, ColorLayer, Label)) and not isinstance(child, Flag):
                self.remove(child)

    def show_all_mines(self):
        for pos in self.grids:
            if self.grids[pos] is Mine:
                self.remove_mask(pos)
        director.window.remove_handlers(self)

    def grid_blink(self, pos):
        poses = pos.get_mask_nearby(self.up_masks)
        for pos_ in poses:
            self.up_masks[pos_].do(Blink(1, 0.15))

    def recursively_expand(self, pos):
        if pos.check_valid(*pos.pos) and self.up_masks[pos] is not None and self.flags[pos] is None:
            self.remove_mask(pos)
            if isinstance(self.grids[pos], int):
                return
            self.recursively_expand(pos.up_pos)
            self.recursively_expand(pos.down_pos)
            self.recursively_expand(pos.left_pos)
            self.recursively_expand(pos.right_pos)

    def remove_mask(self, pos):
        if self.up_masks[pos]:
            self.remove(self.up_masks[pos])
            self.up_masks[pos] = None
        if self.down_masks[pos]:
            self.remove(self.down_masks[pos])
            self.down_masks[pos] = None
        if self.flags[pos]:
            self.remove(self.flags[pos])
            self.flags[pos] = None

    def set_masks(self):
        self.up_masks = {Pos((x, y)): None
                         for x in range(Settings.COLUMNS)
                         for y in range(Settings.ROWS)}
        self.down_masks = {Pos((x, y)): None
                           for x in range(Settings.COLUMNS)
                           for y in range(Settings.ROWS)}
        for x in range(Settings.COLUMNS):
            for y in range(Settings.ROWS):
                up_mask = ColorLayer(127, 127, 127, 255, width=Settings.GRID_SIZE - 1,
                                     height=Settings.GRID_SIZE - 1)
                up_mask.position = Pos((x, y)).pos_to_position()
                self.add(up_mask, z=10)
                self.up_masks[(x, y)] = up_mask

                down_mask = ColorLayer(255, 255, 255, 255, width=Settings.GRID_SIZE - 1,
                                       height=Settings.GRID_SIZE - 1)
                down_mask.position = Pos((x, y)).pos_to_position()
                self.add(down_mask, z=5)
                self.down_masks[(x, y)] = down_mask

    def draw_grids(self):
        for x in range(Settings.COLUMNS + 1):
            self.add(Line(start=(Settings.ORIGIN[0] + x * Settings.GRID_SIZE, Settings.ORIGIN[1]),
                          end=(Settings.ORIGIN[0] + x * Settings.GRID_SIZE,
                               Settings.ORIGIN[1] + Settings.ROWS * Settings.GRID_SIZE),
                          color=(0, 0, 0, 255)))
        for y in range(Settings.ROWS + 1):
            self.add(Line(start=(Settings.ORIGIN[0], Settings.ORIGIN[1] + y * Settings.GRID_SIZE),
                          end=(Settings.ORIGIN[0] + Settings.COLUMNS * Settings.GRID_SIZE,
                               Settings.ORIGIN[1] + y * Settings.GRID_SIZE),
                          color=(0, 0, 0, 255)))

    def place_mines(self, num, pos_):
        mine_poses = sample(list(self.grids), num)

        def check_mines_around():
            for position in mine_poses:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        pos = pos_.x + i, pos_.y + j
                        if pos == position.pos:
                            return True
            return False

        while check_mines_around():
            mine_poses = sample(list(self.grids), num)
        self.is_first_click = False

        for pos in mine_poses:
            self.grids[pos] = Mine
            self.add(Mine(pos))

    def set_nums(self):
        for pos in self.grids:
            if self.grids[pos] is not Mine:
                mines = pos.search_mines(self.grids)
                if mines:
                    self.create_label(pos, mines)
                    self.grids[pos] = mines

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
            font_size=Settings.GRID_SIZE - 5,
            color=chosen_color,
            anchor_x="center",
            anchor_y="center"
        )
        self.add(label)
