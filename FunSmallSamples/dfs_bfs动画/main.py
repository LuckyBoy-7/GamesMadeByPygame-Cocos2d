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
    def __init__(self, color, time=0, pos=None):
        super().__init__(*color, GRID_SIZE - 1, GRID_SIZE - 1)

        self.pos = pos
        if self.pos:
            self.position = self.pos.pos_to_position()
        self.anchor = self.width / 2, self.height / 2
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
        self.helper = GridSetHelper(self)

        self.exec_time = 1
        self.running = False
        self.is_start = False
        self.grids = {Pos(col, row): None
                      for col in range(COLUMNS)
                      for row in range(ROWS)}

        self.schedule(self.update)

    def update(self, dt):
        if self.is_start:
            self.is_start = False
            self.running = True
            self.grids[self.helper.start.pos] = None

            # dfs
            # self.dfs(*self.helper.start.pos)

            # bfs
            self.d = deque()
            self.d.append(self.helper.start.pos)
            self.bfs()

    def dfs(self, x, y):
        pos = Pos(x, y)
        if pos in self.grids and self.running:
            if isinstance(self.grids[pos], End):
                self.running = False
                return
            elif not isinstance(self.grids[pos], Grid):
                grid = Grid((255, 0, 0, 255), time=self.exec_time, pos=pos)
                grid.do(Hide() + Delay(self.exec_time * 0.1) + Show() + FadeIn(0.5))
                self.add(grid)
                self.grids[pos] = grid
                self.exec_time += 1
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
                    grid = Grid((255, 0, 0, 255), time=self.exec_time, pos=pos)
                    grid.do(Hide() + Delay(self.exec_time * 0.1) + Show() + FadeIn(0.5))
                    self.add(grid)
                    self.grids[pos] = grid
                    self.exec_time += 1
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
                    if self.helper.end:
                        self.del_grid(self.helper.end)
                    self.helper.end = self._set_grid(pos, End)
                elif type_ == "start":
                    if self.helper.start:
                        self.del_grid(self.helper.start)
                    self.helper.start = self._set_grid(pos, Start)
                elif type_ == "block":
                    self._set_grid(pos, Block)
            elif isinstance(self.grids[pos], Block):
                self.del_grid(self.grids[pos])

    def del_grid(self, grid):
        self.grids[grid.pos] = None
        self.remove(grid)

    def on_mouse_press(self, x, y, button, modifier):
        if button == 1:
            self.helper.update(x, y)
            self.set_grid(Pos.position_to_pos(x, y), self.helper.current_grid)
        elif button == 4:
            if self.helper.start:
                self.is_start = True

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


class GridSetHelper(object):
    def __init__(self, layer):
        self.layer = layer
        self.current_grid = "end"
        self.start = None
        self.end = None
        self.set_hints()
        self.get_rects()

    def update(self, x, y):
        if self.start_rect.contains(x, y):
            self.change_current_grid("start")
        elif self.end_rect.contains(x, y):
            self.change_current_grid("end")
        elif self.block_rect.contains(x, y):
            self.change_current_grid("block")

    def set_hints(self):
        self.current_hint = Grid((0, 255, 0, 255))
        self.current_hint.position = 0, 0
        self.layer.add(self.current_hint)

        self.set_hint("start")
        self.set_hint("end")
        self.set_hint("block")

    def get_rects(self):
        self.start_rect = Rect(*self.start_hint.position, GRID_SIZE, GRID_SIZE)
        self.end_rect = Rect(*self.end_hint.position, GRID_SIZE, GRID_SIZE)
        self.block_rect = Rect(*self.block_hint.position, GRID_SIZE, GRID_SIZE)

    def change_current_grid(self, type_):
        if type_ == "start":
            color = 255, 0, 0
        elif type_ == "end":
            color = 0, 255, 0
        elif type_ == "block":
            color = 0, 0, 0
        self.current_grid = type_
        self.current_hint.color = color

    def set_hint(self, type_):
        if type_ == "start":
            self.start_hint = Grid((255, 0, 0, 255))
            self.start_hint.position = 0, height - GRID_SIZE * 1
            self.layer.add(self.start_hint)
        elif type_ == "end":
            self.end_hint = Grid((0, 255, 0, 255))
            self.end_hint.position = 0, height - GRID_SIZE * 2
            self.layer.add(self.end_hint)
        elif type_ == "block":
            self.block_hint = Grid((0, 0, 0, 255))
            self.block_hint.position = 0, height - GRID_SIZE * 3
            self.layer.add(self.block_hint)


if __name__ == '__main__':
    director.init(width=1100, height=700)

    GRID_SIZE = 60
    ROWS = 10
    COLUMNS = 10

    width, height = director.get_window_size()
    ORIGIN = width / 2 - COLUMNS / 2 * GRID_SIZE, height / 2 - ROWS / 2 * GRID_SIZE

    director.run(DemoScene())
