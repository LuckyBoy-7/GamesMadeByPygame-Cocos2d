import sys
from collections import namedtuple
from random import shuffle, randint
from itertools import chain

import pygame
from pygame.locals import *

from settings import Settings
from stats import stats
from grid_objs import Mine, Flag, Space, BlinkGrid
from color import *


class MineSweeper(object):
    MINE, SPACE, FLAG, VISITED = range(4)

    def __init__(self):
        pygame.init()
        # 初始化窗口
        self.surface = pygame.display.set_mode(Settings.WINDOW_SIZE)

        # 读取数据
        self.read_datas()
        # 初始化网格(含炸弹)
        self.grids_init()
        self.grid_objs = set()
        self.left_grid = self.columns * self.rows

        # 初始化帧率
        self.clock = pygame.time.Clock()

    def read_datas(self):
        self.columns = Settings.levels[stats.level]["columns"]
        self.rows = Settings.levels[stats.level]["rows"]
        self.grid_size = Settings.levels[stats.level]["grid_size"]
        self.mine_nums = Settings.levels[stats.level]["mine_nums"]
        self.grids_width = self.grid_size * self.columns
        self.grids_height = self.grid_size * self.rows
        self.start_coord = namedtuple("START_COORD", "x y")(int(Settings.WIDTH / 2 - self.columns / 2 * self.grid_size),
                                                            int(Settings.HEIGHT / 2 - self.rows / 2 * self.grid_size))

    def grids_init(self) -> None:
        self.grids = [self.MINE] * self.mine_nums + [self.SPACE] * (self.columns * self.rows - self.mine_nums)
        shuffle(self.grids)
        self.grids = [
            [
                [pos] for pos in self.grids[row * self.columns:(row + 1) * self.columns]
            ] for row in range(len(self.grids) // self.columns)
        ]
        self.blink_grids = [BlinkGrid(self.surface, 0, 0) for _ in range(8)]

    def draw_grid_lines(self) -> None:
        for x in range(self.columns + 1):
            pygame.draw.line(surface=self.surface,
                             color=BLACK,
                             start_pos=(self.start_coord[0] + x * self.grid_size, self.start_coord[1]),
                             end_pos=(self.start_coord[0] + x * self.grid_size,
                                      self.start_coord[1] + self.rows * self.grid_size))
            for y in range(self.rows + 1):
                pygame.draw.line(surface=self.surface, color=BLACK,
                                 start_pos=(self.start_coord[0], self.start_coord[1] + y * self.grid_size),
                                 end_pos=(self.start_coord[0] + self.columns * self.grid_size,
                                          self.start_coord[1] + y * self.grid_size))

    def run(self) -> None:
        while True:
            self.handle_events()

            # 更新blink_grids
            for grid in self.blink_grids:
                grid.update()

            # 处理绘制
            self.update_screen()
            self.clock.tick(Settings.TICK)

    @staticmethod
    def exit_():
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.exit_()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exit_()
            elif event.type == MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event.pos, event.button)

    def handle_mouse_button_down(self, pos, button):
        if not self.mouse_in_grids(pos):
            return

        x, y = self.get_coord(pos)
        if stats.running:
            if button == 1:  # 点左键
                self.handle_first_click(x, y)
                if self.grids[x][y][-1] == self.MINE:
                    self.handle_mine_clicked()
                elif self.grids[x][y][-1] == self.SPACE:
                    self.handle_space_clicked(x, y)
                elif self.grids[x][y][-1] == self.VISITED:
                    self.handle_visited_clicked(x, y)
                elif self.grids[x][y][-1] == self.FLAG:
                    self.handle_flag_clicked(x, y)
            elif button == 3:  # 点右键
                self.handle_right_button_clicked(x, y)

    def handle_first_click(self, x, y):
        if not stats.first_click:
            return

        stats.first_click = False
        while self.mine_nums_in_nine_grids(x, y) != 0:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    pos_x, pos_y = x + i, y + j
                    if self.check_valid(pos_x, pos_y):
                        while self.grids[pos_x][pos_y][-1] == self.MINE:
                            new_x, new_y = randint(0, len(self.grids) - 1), randint(0, len(self.grids[0]) - 1)
                            self.grids[pos_x][pos_y], self.grids[new_x][new_y] = self.grids[new_x][new_y], \
                                                                                     self.grids[pos_x][pos_y]

    def remove_obj(self, x, y, cls) -> None:
        position = self.get_position(x, y)
        self.grid_objs.remove(cls(self.surface, *position))
        self.grids[x][y].pop()

    def create_obj(self, x, y, cls, token) -> None:
        position = self.get_position(x, y)
        self.grid_objs.add(cls(self.surface, *position))
        self.grids[x][y].append(token)

    def get_unvisited_around(self, x, y):
        lst = []
        flag_num = 0
        mine_num = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_x, new_y = x + i, y + j
                if (new_x, new_y) != (x, y) and self.check_valid(new_x, new_y):
                    if self.MINE in self.grids[new_x][new_y]:
                        mine_num += 1
                    if self.grids[new_x][new_y][-1] in [self.SPACE, self.MINE]:
                        lst.append((new_x, new_y))
                    if self.grids[new_x][new_y][-1] == self.FLAG:
                        flag_num += 1
        return lst, flag_num, mine_num

    def handle_visited_clicked(self, x, y):
        poses, flag_num, mine_num = self.get_unvisited_around(x, y)

        if mine_num <= flag_num:
            for pos in poses:
                self.handle_mouse_button_down(self.get_position(*pos), 1)
        else:
            for pos, blink_grid in zip(poses, self.blink_grids):
                blink_grid.x, blink_grid.y = self.get_position(*pos)
                blink_grid.blink()

    def handle_flag_clicked(self, x, y):
        self.remove_obj(x, y, Flag)

    def handle_right_button_clicked(self, x, y):
        if self.grids[x][y][-1] not in [self.VISITED, self.FLAG]:
            self.create_obj(x, y, cls=Flag, token=self.FLAG)
        elif self.grids[x][y][-1] == self.FLAG:
            self.remove_obj(x, y, cls=Flag)

    def handle_mine_clicked(self):
        self.mine_poses = [(x, y) for x in range(len(self.grids)) for y in range(len(self.grids[0]))
                           if self.grids[x][y][-1] == self.MINE]
        for pos in self.mine_poses:
            self.grid_objs.add(Mine(self.surface, *self.get_position(*pos)))
        stats.running = False

    def handle_space_clicked(self, x, y):
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if self.grids[x][y][-1] == self.SPACE:
                position = self.get_position(x, y)

                mine_cnt = self.search_mines_around(x, y)
                if mine_cnt == 0:  # 没有炸弹, 继续递归扩展, 若有, 则是数字, 无需扩展
                    stack.extend(self.get_poses_around(x, y))
                self.grid_objs.add(Space(self.surface, *position, num=mine_cnt))

                self.grids[x][y].append(self.VISITED)
                self.left_grid -= 1
                if self.left_grid == self.mine_nums:
                    print("win")

    def check_valid(self, x, y):
        return 0 <= x < len(self.grids) and 0 <= y < len(self.grids[0])

    def get_poses_around(self, x, y) -> list:
        lst = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_x, new_y = x + i, y + j
                if (new_x, new_y) != (x, y) and self.check_valid(new_x, new_y):
                    lst.append((new_x, new_y))
        return lst

    def mine_nums_in_nine_grids(self, x, y) -> int:
        cnt = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_x, new_y = x + i, y + j
                if self.check_valid(new_x, new_y):
                    if self.grids[new_x][new_y][-1] == self.MINE:
                        cnt += 1

        return cnt

    def search_mines_around(self, x, y) -> int:
        cnt = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_x, new_y = x + i, y + j
                if (new_x, new_y) != (x, y) and self.check_valid(new_x, new_y):
                    if self.MINE in self.grids[new_x][new_y]:
                        cnt += 1
        return cnt

    def get_position(self, x, y):
        x = self.start_coord.x + x * self.grid_size
        y = self.start_coord.y + y * self.grid_size
        return x, y

    def get_coord(self, pos):
        x = (pos[0] - self.start_coord.x) // self.grid_size
        y = (pos[1] - self.start_coord.y) // self.grid_size
        return x, y

    def mouse_in_grids(self, pos):
        x, y = self.start_coord
        if x <= pos[0] <= x + self.grids_width and y <= pos[1] <= y + self.grids_height:
            return True
        return False

    def update_screen(self) -> None:
        self.surface.fill(WHITE)

        # 绘制棋盘背景
        pygame.draw.rect(self.surface, BACKGROUND_COLOR,
                         (*self.start_coord, self.grid_size * self.columns, self.grid_size * self.rows))

        # 绘制obj对象
        for grid in chain(self.grid_objs, self.blink_grids):
            grid.draw()

        # 绘制棋盘线条
        self.draw_grid_lines()

        # 更新
        pygame.display.flip()
