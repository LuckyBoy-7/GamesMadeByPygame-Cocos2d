from random import *

from cocos.layer import Layer, ColorLayer

from settings import Settings


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
        return self.x * Settings.GRID_SIZE + Settings.ORIGIN[0], \
               self.y * Settings.GRID_SIZE + Settings.ORIGIN[1]

    @classmethod
    def position_to_pos(cls, x, y):
        return cls((x - Settings.ORIGIN[0]) // Settings.GRID_SIZE, (y - Settings.ORIGIN[1]) // Settings.GRID_SIZE)

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
    def __init__(self, color, pos=None, route=None):
        super().__init__(*color, Settings.GRID_SIZE - 1, Settings.GRID_SIZE - 1)

        self.pos = pos
        self.position = pos.pos_to_position()
        self.route = route


class Background(Grid):
    def __init__(self, pos):
        super().__init__((0, 0, 0, 255), pos=pos)


class Player(Grid):
    START_IDX = 0

    def __init__(self, route):
        super().__init__((0, 255, 0, 255), pos=Pos(*route[Player.START_IDX]), route=route)
        self.idx = Player.START_IDX
        self.direct = 1

    def draw(self):
        super().draw()

        self.pos = Pos(*self.route[self.idx])
        self.position = self.pos.pos_to_position()


class Enemy(Grid):
    START_IDX = 5

    def __init__(self, route):
        super().__init__((255, 0, 0, 255), pos=Pos(*route[Enemy.START_IDX]), route=route)
        self.idx = Enemy.START_IDX
        self.direct = 1

    def draw(self):
        super().draw()

        self.pos = Pos(*self.route[self.idx])
        self.position = self.pos.pos_to_position()

    def adjust_direct(self, player: Grid):
        tmp = self.idx
        for _ in range(5):
            tmp = (tmp + self.direct * 1) % len(self.route)
            if tmp == player.idx:
                self.direct = -1 if self.direct == 1 else 1
                player.direct = -1 if player.direct == 1 else 1

    def move(self, player: Grid):
        self.adjust_direct(player)
        self.idx = (self.idx + self.direct * 1) % len(self.route)


def build_maze():
    def check_valid(x, y, bound_lb, bound_rt):
        if bound_lb[0] <= x <= bound_rt[0] and bound_lb[1] <= y <= bound_rt[1] and (x, y) not in visited:
            return True
        return False

    matrix = [[0] * Settings.COLUMNS for _ in range(Settings.ROWS)]
    for i in range(1, Settings.ROWS, 2):
        for j in range(1, Settings.COLUMNS, 2):
            matrix[i][j] = 1
    flag = set()
    visited = []

    direct = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    visited.append(Settings.grid_start)  # 否则可能被反向搜索造成缺角的情况

    def dfs(x, y, dest, bound_lb, bound_rt):
        shuffle(direct)
        for delta_x, delta_y in list(direct):
            if check_valid(x + delta_x, y + delta_y, bound_lb, bound_rt):
                visited.append((x + delta_x // 2, y + delta_y // 2))
                visited.append((x + delta_x, y + delta_y))
                flag.add((x + delta_x // 2, y + delta_y // 2))
                if (x + delta_x, y + delta_y) == dest:
                    return True
                if dfs(x + delta_x, y + delta_y, dest, bound_lb, bound_rt):
                    return True
                else:
                    flag.remove((x + delta_x // 2, y + delta_y // 2))
                    visited.pop()
                    visited.pop()

    dfs(*Settings.grid_start, Settings.grid_end, (Settings.grid_start[0], Settings.grid_start[1]),
        (Settings.grid_end[0], Settings.grid_end[1]))
    visited.pop(0)
    dfs(*Settings.grid_end, Settings.grid_start, (0, 0), (Settings.ROWS - 1, Settings.COLUMNS - 1))

    matrix = [[0] * Settings.COLUMNS for _ in range(Settings.ROWS)]
    for x, y in flag:
        matrix[x][y] = 1
    for x, y in visited:
        matrix[x][y] = 1
    return matrix, [(x, y) for y, x in visited]
