from collections import namedtuple

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.draw import Line
from cocos.sprite import BatchableNode

from settings import Settings


class GameScene(Scene):
    def __init__(self):
        super(GameScene, self).__init__()

        self.add(ColorLayer(127, 127, 127, 255), z=1)  # 背景层
        self.add(GameLayer(), z=2)  # 游戏层


Pos = namedtuple("Pos", ["x", "y"])


class GameLayer(Layer):
    def __init__(self):
        super(GameLayer, self).__init__()

        self.add(TableLayer())


class TableLayer(Layer):
    def __init__(self):
        super(TableLayer, self).__init__()

        self.draw_grid_lines()

        self.schedule(self.move_down)

    def move_down(self, dt):
        gap = 1
        for line in self.row_lines:
            line.start = line.start[0], line.start[1] - gap
            line.end = line.end[0], line.end[1] - gap
            if line.start[1] <= Settings.START.y:
                line.start = line.start[0], Settings.START.y + Settings.TABLE_HEIGHT
                line.end = line.end[0], Settings.START.y + Settings.TABLE_HEIGHT


    def draw_grid_lines(self):  # 以0点为基准
        self.row_lines = []
        start_x, start_y = Settings.START
        for x in range(Settings.COLUMNS + 1):
            self.add(Line(start=(start_x + Settings.GRID_WIDTH * x, start_y),
                          end=(start_x + Settings.GRID_WIDTH * x, start_y + Settings.GRID_HEIGHT * Settings.ROWS),
                          color=(0, 0, 0, 255),
                          stroke_width=2))
        self.add(Line(start=(start_x, start_y),
                      end=(start_x + Settings.TABLE_WIDTH, start_y),
                      color=(0, 0, 0, 255),
                      stroke_width=2))
        self.add(Line(start=(start_x, start_y + Settings.TABLE_HEIGHT),
                      end=(start_x + Settings.TABLE_WIDTH, start_y + Settings.TABLE_HEIGHT),
                      color=(0, 0, 0, 255),
                      stroke_width=2))
        for y in range(Settings.ROWS):
            tmp = Line(start=(start_x, start_y + Settings.GRID_HEIGHT * y),
                       end=(start_x + Settings.GRID_WIDTH * Settings.COLUMNS, start_y + Settings.GRID_HEIGHT * y),
                       color=(0, 0, 0, 255),
                       stroke_width=2)
            self.add(tmp)
            self.row_lines.append(tmp)
