from random import *

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.draw import Line
from cocos.text import Label
from cocos.actions import FadeIn, Delay, Hide, Show

from settings import Settings
from position import Pos
from grid import Start, End, Block, Grid


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

    matrix = [[1] * Settings.COLUMNS for _ in range(Settings.ROWS)]
    for y_ in range(Settings.COLUMNS):  # 边界(两条横线)
        matrix[0][y_] = 0
        matrix[Settings.ROWS - 1][y_] = 0
    for x_ in range(Settings.ROWS):  # 两条竖线
        matrix[x_][0] = 0
        matrix[x_][Settings.COLUMNS - 1] = 0

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

    split(1, 1, Settings.ROWS - 2, Settings.COLUMNS - 2)
    return matrix


class DemoScene(Scene):
    def __init__(self):
        super(DemoScene, self).__init__()

        self.add(ColorLayer(255, 255, 255, 255), z=1)  # 背景涂白
        self.add(GridLayer(), z=2)


class GridLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super(GridLayer, self).__init__()

        self.grids = self._grids_init()
        self._set_end()
        self._draw_grid_lines()

        self._draw_maze()

        self.route = self.get_dfs_route()
        self._handle_show_route()

    def _draw_maze(self):
        maze = build_maze()
        for i in range(Settings.ROWS):
            for j in range(Settings.COLUMNS):
                pos = Pos(j, i)
                if maze[i][j] == 0:
                    self.set_grid(pos, "block")

    def _set_end(self):
        self.set_grid(Pos(*Settings.END_POS), "end")

    def _handle_show_route(self):
        self.i = 0
        self.elapsed = 0
        self.schedule(self._show_route)

    def _show_route(self, dt):
        self.elapsed += 1
        if self.elapsed > Settings.THRESHOLD:
            self.elapsed = 0
            self.grids[self.route[self.i]].do(Show())
            self.i += 1
            if self.i == len(self.route):
                self.unschedule(self._show_route)

    def _grids_init(self) -> dict:
        return {Pos(col, row): None
                for col in range(Settings.COLUMNS)
                for row in range(Settings.ROWS)}

    def _draw_grid_lines(self) -> None:
        row, col, size, origin = Settings.ROWS, Settings.COLUMNS, Settings.GRID_SIZE, Settings.ORIGIN
        for x in range(col + 1):
            self.add(Line(start=(origin[0] + x * size, size),
                          end=(origin[0] + x * size,
                               origin[1] + row * size),
                          color=(0, 0, 0, 255)))
        for y in range(row + 1):
            self.add(Line(start=(origin[0], origin[1] + y * size),
                          end=(origin[0] + col * size,
                               origin[1] + y * size),
                          color=(0, 0, 0, 255)))

    def _set_grid(self, pos, cls, **kwargs):
        tmp = cls(pos, **kwargs)
        if isinstance(tmp, Start):
            tmp.do(Hide())
        self.grids[pos] = tmp
        self.add(tmp)
        return tmp

    def set_grid(self, pos, type_, **kwargs):
        if type_ == "end":
            self._set_grid(pos, End, **kwargs)
        elif type_ == "start":
            self._set_grid(pos, Start, **kwargs)
        elif type_ == "block":
            self._set_grid(pos, Block, **kwargs)

    def del_grid(self, grid):
        self.grids[grid.pos] = None
        self.remove(grid)

    def get_dfs_route(self) -> list:
        route = []
        running = True
        exec_time = 1

        def dfs(x, y):
            nonlocal exec_time, running  # 因为要修改exec_time的值所以要nonlocal, 否则会被当作局部变量
            pos = Pos(x, y)
            if pos in self.grids and running:
                if isinstance(self.grids[pos], End):
                    running = False
                    return
                elif not isinstance(self.grids[pos], Grid):
                    self.set_grid(pos, "start", exec_time=exec_time)
                    route.append(pos)
                    exec_time += 1

                    dfs(x + 1, y)
                    dfs(x - 1, y)
                    dfs(x, y + 1)
                    dfs(x, y - 1)

        dfs(*Settings.START_POS)
        return route


if __name__ == '__main__':
    director.init(width=Settings.WIDTH, height=Settings.HEIGHT)
    director.run(DemoScene())
