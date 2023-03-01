from random import *
from collections import deque

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.draw import Line
from cocos.text import Label
from cocos.rect import Rect
from cocos.actions import FadeIn, Delay, Hide, Show


class DemoScene(Scene):
    def __init__(self):
        super(DemoScene, self).__init__()

        self.add(ColorLayer(255, 255, 255, 255), z=1)  # 背景涂白
        self.add(DemoLayer(), z=2)


class Pos(object):
    def __init__(self, x, y):
        self.pos = x, y

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def pos_to_position(self):
        return self.x * GRID_SIZE + ORIGIN[0], \
               self.y * GRID_SIZE + ORIGIN[1]

    @classmethod
    def position_to_pos(cls, x, y):
        return cls((x - ORIGIN[0]) // GRID_SIZE, (y - ORIGIN[1]) // GRID_SIZE)

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        if self.pos == other.pos:
            return True
        return False

    def __iter__(self):
        yield self.x
        yield self.y


class Grid(ColorLayer):
    exec_time = 1

    def __init__(self, color, time=0, pos=None):
        super().__init__(*color, GRID_SIZE - 1, GRID_SIZE - 1)

        self.pos = pos
        if self.pos:
            self.position = self.pos.pos_to_position()
        self.anchor = self.width / 2, self.height / 2
        if show_num:
            if time:
                label = Label(f"{time}", font_size=30, anchor_x="center", anchor_y="center")
                label.x, label.y = self.width / 2, self.height / 2
                self.add(label)

                while label.element.content_width > self.width or label.element.content_height > self.height:
                    label.element.font_size -= 5


class End(Grid):
    def __init__(self, pos):
        super().__init__((0, 255, 0, 255), pos=pos)


class Start(Grid):
    def __init__(self, pos, time=0):
        super().__init__((255, 0, 0, 255), time, pos=pos)


class Block(Grid):
    def __init__(self, pos):
        super().__init__((0, 0, 0, 255), pos=pos)


class DemoLayer(Layer):
    grids: dict

    is_event_handler = True

    def __init__(self):
        super(DemoLayer, self).__init__()

        self.draw_grid_lines()
        self.grids_init()

        self.running = True
        self.schedule(self.update)

    def grids_init(self):
        self.grids = {Pos(col, row): None
                      for col in range(COLUMNS)
                      for row in range(ROWS)}
        for i in range(COLUMNS):
            for j in range(ROWS):
                if matrix[j][i] == 0:
                    self.grids[Pos(i, j)] = self.set_grid(Pos(i, j), "block")
        self.set_grid(Pos(*start), "start")  # matrix是像素坐标系
        self.grids[Pos(*start)] = None
        self.set_grid(Pos(*end), "end")  # Pos是笛卡尔坐标系, 所以要反一下

    def update(self, dt):
        # dfs
        self.dfs(*start)

        # bfs
        self.d = deque()
        self.d.append(start)
        self.bfs()

    def dfs(self, x, y):
        pos = Pos(x, y)
        if pos in self.grids and self.running:
            if isinstance(self.grids[pos], End):
                self.running = False
                return
            elif not isinstance(self.grids[pos], Grid):
                grid = Grid((255, 0, 0, 255), time=Grid.exec_time, pos=pos)
                # grid.do(Hide() + Delay(Grid.exec_time * 0.01) + Show() + FadeIn(0.5))
                grid.do(Hide() + Delay(Grid.exec_time * 0.01) + Show())
                self.add(grid)
                self.grids[pos] = grid
                Grid.exec_time += 1
                self.dfs(x + 1, y)
                self.dfs(x - 1, y)
                self.dfs(x, y + 1)
                self.dfs(x, y - 1)

    def bfs(self):
        while self.d:
            x, y = self.d.popleft()
            pos = Pos(x, y)
            if pos in self.grids and self.running:
                if isinstance(self.grids[pos], End):
                    self.running = False
                    return
                elif not isinstance(self.grids[pos], Grid):
                    grid = Grid((255, 0, 0, 255), time=Grid.exec_time, pos=pos)
                    # grid.do(Hide() + Delay(Grid.exec_time * 0.01) + Show() + FadeIn(0.5))
                    grid.do(Hide() + Delay(Grid.exec_time * 0.01) + Show())
                    self.add(grid)
                    self.grids[pos] = grid
                    Grid.exec_time += 1
                    self.d.append((x + 1, y))
                    self.d.append((x - 1, y))
                    self.d.append((x, y + 1))
                    self.d.append((x, y - 1))

    def _set_grid(self, pos, cls):
        tmp = cls(pos=pos)
        self.grids[pos] = tmp
        self.add(tmp)
        return tmp

    def set_grid(self, pos, type_):
        if pos in self.grids:
            if self.grids[pos] is None:
                if type_ == "end":
                    return self._set_grid(pos, End)
                elif type_ == "start":
                    return self._set_grid(pos, Start)
                elif type_ == "block":
                    return self._set_grid(pos, Block)

    def del_grid(self, grid):
        self.grids[grid.pos] = None
        self.remove(grid)

    def draw_grid_lines(self):
        for x in range(COLUMNS + 1):
            self.add(Line(start=(ORIGIN[0] + x * GRID_SIZE, ORIGIN[1]),
                          end=(ORIGIN[0] + x * GRID_SIZE,
                               ORIGIN[1] + ROWS * GRID_SIZE),
                          color=(0, 0, 0, 255)))
        for y in range(ROWS + 1):
            self.add(Line(start=(ORIGIN[0], ORIGIN[1] + y * GRID_SIZE),
                          end=(ORIGIN[0] + COLUMNS * GRID_SIZE,
                               ORIGIN[1] + y * GRID_SIZE),
                          color=(0, 0, 0, 255)))


def build_maze():
    def check_valid(x, y):
        # 判断该位置是否能确保打通相邻两块区域,判断依据, 上下左右位置最多只有两面墙
        cnt = 0
        for i, j in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            if matrix[x + i][y + j] == 0:
                cnt += 1
                if cnt > 2:
                    return False
        return True

    matrix = [[1] * COLUMNS for _ in range(ROWS)]
    for y_ in range(COLUMNS):  # 边界(两条横线)
        matrix[0][y_] = 0
        matrix[ROWS - 1][y_] = 0
    for x_ in range(ROWS):  # 两条竖线
        matrix[x_][0] = 0
        matrix[x_][COLUMNS - 1] = 0

    def split(x, y, end_x, end_y):
        if end_x - x + 1 >= 3 and end_y - y + 1 >= 3:
            mid_x, mid_y = randint(x + 1, end_x - 1), randint(y + 1, end_y - 1)  # 随机取点
            for y_ in range(y, end_y + 1):  # 画两条线(这条是横线)
                matrix[mid_x][y_] = 0
            for x_ in range(x, end_x + 1):  # 竖线
                matrix[x_][mid_y] = 0
            # 我草, 先分割后破墙能少这么多bug!!! 还是后序稳健一点
            # 因为状态已经确定, 前序不知道未来会发生什么
            split(x, y, mid_x - 1, mid_y - 1)  # 左上(地图左下)
            split(x, mid_y + 1, mid_x - 1, end_y)  # 右上(地图右下)
            split(mid_x + 1, y, end_x, mid_y - 1)  # 左下(地图左上)
            split(mid_x + 1, mid_y + 1, end_x, end_y)  # 右下(地图右上)

            tmp1 = mid_x, randint(y, mid_y - 1)
            tmp2 = mid_x, randint(mid_y + 1, end_y)
            tmp3 = randint(x, mid_x - 1), mid_y
            tmp4 = randint(mid_x + 1, end_x), mid_y
            while not check_valid(*tmp1):
                tmp1 = mid_x, randint(y, mid_y - 1)
            while not check_valid(*tmp2):
                tmp2 = mid_x, randint(mid_y + 1, end_y)
            while not check_valid(*tmp3):
                tmp3 = randint(x, mid_x - 1), mid_y
            while not check_valid(*tmp4):
                tmp4 = randint(mid_x + 1, end_x), mid_y

            for tmp_x, tmp_y in sample([tmp1, tmp2, tmp3, tmp4], 3):
                matrix[tmp_x][tmp_y] = 1

    split(1, 1, ROWS - 2, COLUMNS - 2)
    return matrix


if __name__ == '__main__':
    director.init(width=1400, height=800)

    GRID_SIZE = 24
    ROWS = 31  # 都要是奇数
    COLUMNS = 37
    show_num = False  # 是否展现路径先后顺序
    start, end = (1, 1), (COLUMNS - 2, ROWS - 2)
    matrix = build_maze()

    width, height = director.get_window_size()
    ORIGIN = width / 2 - COLUMNS / 2 * GRID_SIZE, height / 2 - ROWS / 2 * GRID_SIZE

    director.run(DemoScene())
