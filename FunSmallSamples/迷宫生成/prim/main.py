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

    matrix = [[0] * Settings.COLUMNS for _ in range(Settings.ROWS)]
    for i in range(1, Settings.ROWS, 2):
        for j in range(1, Settings.COLUMNS, 2):
            matrix[i][j] = 1

    visited = set()  # 标记访问过的
    visited.add(Settings.START_POS)
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
