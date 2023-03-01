from random import *
from collections import deque

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.draw import Line
from cocos.text import Label
from cocos.actions import Delay, Hide, Show


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
    def check_valid(x, y, bound_lb, bound_rt):
        if bound_lb[0] <= x <= bound_rt[0] and bound_lb[1] <= y <= bound_rt[1] and (x, y) not in visited:
            return True
        return False


    matrix = [[0] * COLUMNS for _ in range(ROWS)]
    for i in range(1, ROWS, 2):
        for j in range(1, COLUMNS, 2):
            matrix[i][j] = 1
    flag = set()
    visited = set()

    direct = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    visited.add(start)  # 否则可能被反向搜索造成缺角的情况

    def dfs(x, y, dest, bound_lb, bound_rt):
        shuffle(direct)
        for delta_x, delta_y in list(direct):
            if check_valid(x + delta_x, y + delta_y, bound_lb, bound_rt):
                visited.add((x + delta_x, y + delta_y))
                flag.add((x + delta_x // 2, y + delta_y // 2))
                if (x + delta_x, y + delta_y) == dest:
                    return True
                if dfs(x + delta_x, y + delta_y, dest, bound_lb, bound_rt):
                    return True
                else:
                    flag.remove((x + delta_x // 2, y + delta_y // 2))
                    visited.remove((x + delta_x, y + delta_y))

    dfs(*start, end, (0, start[1]), (end[0], ROWS - 1))
    visited.remove(start)
    dfs(*end, start, (0, 0), (ROWS - 1, COLUMNS - 1))

    matrix = [[0] * COLUMNS for _ in range(ROWS)]
    for x, y in flag:
        matrix[x][y] = 1
    for x, y in visited:
        matrix[x][y] = 1
    return matrix


if __name__ == '__main__':
    director.init(width=1400, height=800)

    GRID_SIZE = 32
    ROWS = 21  # 都要是奇数
    COLUMNS = 21
    show_num = False  # 是否展现路径先后顺序
    start, end = (5, 5), (COLUMNS - 6, ROWS - 6)
    matrix = build_maze()

    width, height = director.get_window_size()
    ORIGIN = width / 2 - COLUMNS / 2 * GRID_SIZE, height / 2 - ROWS / 2 * GRID_SIZE

    director.run(DemoScene())
