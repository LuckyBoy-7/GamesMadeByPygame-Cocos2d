"""
1. 刚开始不管点左右键, 都会开始游戏

原版: 1. 有self.grids, up_masks(灰色), down_masks(白色), flags, 创建的时候都是整个对象内存开销大
     2. 原理:
             1. 是up_mask和down_mask遮住nums&Mines, 点击取出两个mask
             2. 闪烁是暂时隐藏up_mask, 白色的down_mask漏出来, 实现blink
             3. flags是方便查找
改进: 1. 只有self.grids是整个的, up_masks, flags, 刚开始都是空{}, 去除了down_masks(perfect)
     2. 原理:
             1. 背景层(灰色)一整块挡在下面, nums&Mines隐藏
             2. 点击加入mask(白色), nums&Mines出现在他的上方
             3. blink可以动态的添加和删除
             4. adjust要做吐了
"""

from random import sample, randint

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.draw import Line
from cocos.text import Label
from cocos.actions import Blink, Hide, Show

from settings import Settings
from color import *
from grid_objs import Mine, Flag, Mask
from position import Pos
from widgets import Hint, all_permutations, Button


class GameScene(Scene):
    def __init__(self):
        super().__init__()

        self.restart()

    def restart(self):
        for _, child in self.children:
            self.remove(child)

        self.add(ColorLayer(*WHITE), z=0)  # 背景层
        color_layer = ColorLayer(*GREY,
                                 width=Settings.columns * Settings.grid_size,
                                 height=Settings.rows * Settings.grid_size)
        color_layer.position = Settings.origin
        self.add(color_layer, z=1)  # grid背景层
        self.add(GameLayer(), z=2)  # 游戏层


class GameLayer(Layer):
    up_masks: dict
    grids: dict
    is_first_click: bool
    start_time: float
    time_hint: Label
    mines_hint: Label
    blink_grids: set
    changed_num_poses: set
    rest_grids: set

    is_event_handler = True

    def __init__(self):
        super().__init__()

        self.is_over = False

        # 绘制棋盘
        self.draw_grids()
        # 设置各种先隐藏再显示的信息
        self.flags = {}
        self.nums = {}
        self.mines = {}
        self.up_masks = {}
        self.set_blink_grids()  # 设置八个隐藏的闪烁砖块, 需要的时候拿出来用
        self.grids = {Pos(x, y): 0
                      for x in range(Settings.columns)
                      for y in range(Settings.rows)}  # 棋盘, 但好像也就只是存int
        self.is_first_click = True
        # 布置雷(mine)和设置数字 [之后再调整, 不然第一次点击会有卡顿感]
        self.place_mines()
        self.set_nums()
        # 炸弹数量和时间的提醒类, 和更换关卡类
        self.hint = Hint(self)
        self.button = Button(self)

        self.schedule(self.update)

    def on_mouse_press(self, x, y, button, _):
        self.handle_button_logical(x, y)
        if not self.is_over:
            pos = Pos.position_to_pos(x, y)
            if pos in self.grids:  # 在网格内操作
                self.hint.start()
                if button == 1:  # 点击左键
                    if not self.has_been_clicked(pos):  # 点到棋盘内未点击区
                        if pos in self.flags:
                            self.remove_flag(pos)
                        else:
                            if self.is_first_click:  # 第一次保证点到空白部分
                                self.first_click(pos)
                            elif pos not in self.nums and pos not in self.mines:  # 点到空白
                                self.recursively_expand(pos)

                            if pos in self.nums:  # 点到数字
                                self.nums[pos].do(Show())
                            self.set_mask(pos)
                            self.judge_success(pos)
                    elif pos in self.nums:
                        if pos.count_flags(self.flags) >= self.grids[pos]:
                            pos.auto_remove(self.flags, self)
                            self.judge_success(pos)
                        else:
                            self.grid_blink(pos)

                elif button == 4:  # 点击右键
                    if not self.has_been_clicked(pos):  # 只能在未点击的地方点
                        if pos not in self.flags:
                            self.set_flag(pos)
                            self.hint.mine_nums -= 1
                        else:
                            self.remove_flag(pos)
        else:
            if button == 1:
                self.restart()

    def first_click(self, pos):
        # 调整雷和数字
        self.adjust_mines(pos)
        self.adjust_nums()
        # 点到空白地方扩展开来
        self.recursively_expand(pos)

        self.is_first_click = False

    def update(self, _):
        self.hint.update_time()

    def handle_button_logical(self, x, y):
        self.button.check_button(x, y)

    def adjust_mines(self, pos: Pos):
        around_mines = set()
        forbidden_poses = set()  # 防止mine又抽到pos那一圈
        self.changed_num_poses = set()  # 记录要被调整的num(被移除的mine的旁边&新的mine的旁边)

        # p是pos旁边的position, pp是p旁边的position
        for p in all_permutations([-1, 0, 1]):  # 周围找一圈
            p = p + pos
            forbidden_poses.add(p)
            if p in self.mines:
                for pp in all_permutations([-1, 0, 1]):  # 周围找一圈
                    pp = pp + p
                    if Pos.check_valid(*pp):
                        self.grids[pp] -= 1  # 改mine周围的num
                        self.changed_num_poses.add(pp)
                self.remove(self.mines[p])
                self.mines.pop(p)
                self.grids[p] = p.search_mines(self.mines)  # 改mine上的num
                around_mines.add(p)

        chosen_poses = {pos for pos in self.rest_grids if pos not in forbidden_poses}
        new_pos = sample(chosen_poses, len(around_mines))

        pos: Pos
        for pos in new_pos:
            for p in all_permutations([-1, 0, 1]):  # 周围找一圈
                p = p + pos
                if Pos.check_valid(*p):
                    self.grids[p] += 1
                    self.changed_num_poses.add(p)
                if p in self.nums:
                    self.remove(self.nums[p])
                    self.nums.pop(p)
            self._place_mines(pos)

    def adjust_nums(self):
        pos: Pos
        for pos in self.changed_num_poses:
            mines = self.grids[pos]
            if mines > 0:
                if pos not in self.mines:
                    self.create_num_label(pos, mines)
                    self.grids[pos] = mines
            else:
                if pos in self.nums:
                    self.remove(self.nums[pos])
                    self.nums.pop(pos)

    def set_mask(self, pos):
        if pos in self.flags:
            self.remove_flag(pos)
        if pos in self.nums:
            self.nums[pos].do(Show())
        up_mask = Mask(pos)
        up_mask.position = pos.pos_to_position()
        self.add(up_mask, z=2)
        self.up_masks[pos] = up_mask

    def set_flag(self, pos):
        flag = Flag(pos)
        self.add(flag, z=2)
        self.flags[pos] = flag

    def set_nums(self):
        for pos in self.grids:
            if pos not in self.mines:
                mines = pos.search_mines(self.mines)
                if mines:
                    self.create_num_label(pos, mines)
                    self.grids[pos] = mines

    def place_mines(self):
        mine_poses = sample(list(self.grids), Settings.mine_nums)
        for pos in mine_poses:
            self._place_mines(pos)
        self.rest_grids = {pos for pos in self.grids if pos not in self.mines}

    def _place_mines(self, pos):
        mine = Mine(pos)
        mine.do(Hide())
        self.mines[pos] = mine
        self.add(mine, z=3)

    def has_been_clicked(self, pos):
        return pos in self.up_masks

    def has_been_inserted(self, pos):
        return pos in self.flags

    def set_blink_grids(self):
        self.blink_grids = set()
        for i in range(8):
            grid = ColorLayer(255, 255, 255, 255, width=Settings.grid_size - 1,
                              height=Settings.grid_size - 1)
            grid.do(Hide())
            self.blink_grids.add(grid)
            self.add(grid, z=10)

    def grid_blink(self, pos):
        poses = pos.get_grids_nearby(self.up_masks, self.flags)
        for grid, pos_ in zip(self.blink_grids, poses):
            grid.do(Show() + Blink(1, 0.15) + Hide())
            grid.position = pos_.pos_to_position()

    def judge_success(self, pos):
        # 若剩余格子与炸弹数相同, 则成功(前提是最后一个点到的不是mine, 因为这也会增加一个mask)
        if pos in self.mines:
            self.hint.game_over()
        elif len(self.grids) - len(self.up_masks) == Settings.mine_nums:
            self.hint.succeed()

    def stop_work(self):
        self.is_over = True
        # director.window.remove_handlers(self)
        self.unschedule(self.update)

    def show_all_mines(self):
        for mine in self.mines.values():
            mine.do(Show())

    def recursively_expand(self, pos):
        if Pos.check_valid(*pos) and not self.has_been_clicked(pos):
            if (self.is_first_click and self.has_been_inserted(pos)) or \
                    not self.has_been_inserted(pos):

                self.set_mask(pos)
                if pos in self.nums:
                    return
                self.recursively_expand(pos.up_pos)
                self.recursively_expand(pos.down_pos)
                self.recursively_expand(pos.left_pos)
                self.recursively_expand(pos.right_pos)

    def remove_flag(self, pos):
        self.hint.mine_nums += 1
        self.remove(self.flags[pos])
        self.flags.pop(pos)

    def draw_grids(self):
        for x in range(Settings.columns + 1):
            self.add(Line(start=(Settings.origin[0] + x * Settings.grid_size, Settings.origin[1]),
                          end=(Settings.origin[0] + x * Settings.grid_size,
                               Settings.origin[1] + Settings.rows * Settings.grid_size),
                          color=BLACK))
        for y in range(Settings.rows + 1):
            self.add(Line(start=(Settings.origin[0], Settings.origin[1] + y * Settings.grid_size),
                          end=(Settings.origin[0] + Settings.columns * Settings.grid_size,
                               Settings.origin[1] + y * Settings.grid_size),
                          color=BLACK))

    def create_num_label(self, pos: Pos, num):
        color = [BLUE, GREEN, RED, DARK_BLUE]
        if num <= 4:
            chosen_color = color[num - 1]
        else:
            chosen_color = (randint(0, 255), randint(0, 255), randint(0, 255), 255)
        label = Label(
            text=f"{num}",
            position=pos.pos_to_mid_position(),
            font_size=Settings.grid_size - 5,
            color=chosen_color,
            anchor_x="center",
            anchor_y="center"
        )
        label.do(Hide())
        self.nums[pos] = label
        self.add(label, z=3)

    def restart(self):
        self.parent.restart()
        # self.parent.remove(self)
        # self.parent.add(GameLayer(), z=2)