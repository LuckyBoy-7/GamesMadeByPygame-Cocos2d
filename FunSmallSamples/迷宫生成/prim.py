"""
Prim遍历墙的算法
来自<httos://www.ianshu.com/p/c93615186a05>
一开始，所有网格的所有墙都保留；
随机选择一个网格，将这个网格加入到遍历过的网格列表里；然后将这个网格的四面墙，添加到候选墙的列表中；
当候选的墙的列表不为空时，进行下面的循环：
（1）在候选墙的列表中随机选择一面墙。根据这面墙的标识（网格编号和方向）可以得到被这面墙分割的2个网格，例如C1和02；
（2）下面对这2个网格进行汇断：如果这2个网格仅有1个网格（假设D2）在遍历过的网格列表里，那就移除这面墙（字典中的值变为1)，同时在候选墙列表中也移除。同时
把另一个网格（也就是C1)添加到遍历过的网格列表中，同时把这个网格（C1）的周围的墙添加到候选墙的列表中，注意只添加字典中的值为0的墙，也就是没有处理过的
墙。
（3）如果这2个网格都在遍历过的网格列表里，说明这面墙需要保留。直接在候选墙的列表中删除即可。因为这面墙虽然字典的值为0，但是分割的2个网格都已经遍历
过，所以不可能在被选进候选墙中。

这里把墙看细好理解一点
"""
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
        # self.dfs(*start)

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
        if 0 < x < len(matrix) - 1 and 1 <= y < len(matrix[0]) - 1 and (x, y) not in visited:
            return True
        return False

    def get_valid_wall_around(x, y):
        retval = []
        for delta_x, delta_y, axis in [(1, 0, 1), (-1, 0, 1), (0, 1, 0), (0, -1, 0)]:
            new_x, new_y = x + delta_x, y + delta_y
            if check_valid(new_x, new_y):
                if matrix[new_x][new_y] == 0:
                    print(12903)
                    retval.append((new_x, new_y, axis))
        return retval

    matrix = [[0] * COLUMNS for _ in range(ROWS)]
    for i in range(1, ROWS, 2):
        for j in range(1, COLUMNS, 2):
            matrix[i][j] = 1

    visited = set()  # 标记访问过的
    visited.add(start)
    walls = [(2, 1, 1), (1, 2, 0)]  # 表示墙
    while walls:
        idx = randint(0, len(walls) - 1)
        *pos, axis = walls.pop(idx)
        pos = tuple(pos)
        if check_valid(*pos):
            visited.add(pos)

            if axis == 0:
                if (pos[0], pos[1] - 1) in visited and (pos[0], pos[1] + 1) in visited:
                    continue
                elif (pos[0], pos[1] - 1) not in visited:
                    visited.add((pos[0], pos[1] - 1))
                    walls.extend(get_valid_wall_around(pos[0], pos[1] - 1))
                else:
                    visited.add((pos[0], pos[1] + 1))
                    walls.extend(get_valid_wall_around(pos[0], pos[1] + 1))
            if axis == 1:
                if (pos[0] - 1, pos[1]) in visited and (pos[0] + 1, pos[1]) in visited:
                    continue
                elif (pos[0] - 1, pos[1]) not in visited:
                    visited.add((pos[0] - 1, pos[1]))
                    walls.extend(get_valid_wall_around(pos[0] - 1, pos[1]))
                else:
                    visited.add((pos[0] + 1, pos[1]))
                    walls.extend(get_valid_wall_around(pos[0] + 1, pos[1]))
            matrix[pos[0]][pos[1]] = 1

        # for i, j in [[0, 1], [0, -1]]:  # 横向
        #     if check_valid(pos[0] + i, pos[1] + j):
        #         walls.append((pos[0] + i, pos[1] + j, 0))
        # for i, j in [[1, 0], [-1, 0]]:  # 纵向
        #     if check_valid(pos[0] + i, pos[1] + j):
        #         walls.append((pos[0] + i, pos[1] + j, 1))

    return matrix


if __name__ == '__main__':
    director.init(width=1400, height=800)

    GRID_SIZE = 24
    ROWS = 31  # 都要是奇数
    COLUMNS = 31
    show_num = False  # 是否展现路径先后顺序
    start = 1, 1  # x, y, axis
    end = ROWS - 2, COLUMNS - 2
    matrix = build_maze()

    width, height = director.get_window_size()
    ORIGIN = width / 2 - COLUMNS / 2 * GRID_SIZE, height / 2 - ROWS / 2 * GRID_SIZE

    director.run(DemoScene())
