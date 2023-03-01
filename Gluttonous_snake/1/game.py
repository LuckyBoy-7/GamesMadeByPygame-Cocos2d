"""
我在想self.prop_spawn_places到底是用dict还是list管理呢
dict: 增删改查snake_body是O(1)的, 但是每抽取一次spawn_place都要list()整个个对象, 开销大
list: 可以做到完美抽取, 但增删改查snake_body是O(n)的

考虑到apple被吃才会刷新, 而snake_body需要不断增删改查, 所以我选择dict
我每次都沉湎于效率, 以至于code没有效率
todo: 1. restart col = 2, row = 2
      2. higher level col += 1, row += 1
      3. auto_move
"""

from collections import namedtuple
from random import choice

from cocos.director import director
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.draw import Line
from cocos.text import Label
from cocos.actions import FadeIn
from pyglet.window import key

from snake import Snake, SnakeBody, SnakeHead, AppleProp, Pos


class _GameConfigue(object):
    """采用笛卡尔直角坐标系Origin(0, 0)"""
    GRID_SIZE = 40

    def __init__(self):
        self.rows = 2
        self.columns = 2

        width, height = director.get_window_size()
        self.ORIGIN = namedtuple("Origin", "x y")(width / 2 - self.rows / 2 * self.GRID_SIZE,
                                                  height / 2 - self.columns / 2 * self.GRID_SIZE)

    def upgrade_level(self):
        self.rows += 1
        self.columns += 1
        width, height = director.get_window_size()
        self.ORIGIN = namedtuple("Origin", "x y")(width / 2 - self.rows / 2 * self.GRID_SIZE,
                                                  height / 2 - self.columns / 2 * self.GRID_SIZE)


class GameScene(Scene):
    def __init__(self):
        super().__init__()

        # 背景层(白色)
        self.add(ColorLayer(127, 127, 127, 255), z=0)
        # 游戏层
        self.add(GameLayer(), z=1)


class GameLayer(Layer):
    snake: Snake
    move_elapsed: int
    prop_spawn_places: dict
    grids: dict
    is_win: bool
    is_game_over: bool
    
    is_event_handler = True
    
    def __init__(self):
        super().__init__()

        # 基本信息
        self.config = _GameConfigue()

        self.init()
        self.schedule(self.update)

    def init(self):
        self.is_game_over = False
        self.is_win = False
        # 画网格
        self.draw_grid_line()
        # 初始化snake_body和网格信息
        self.grids = {(x, y): None for x in range(self.config.columns) for y in range(self.config.rows)}
        self.snake = Snake(self)
        # 可放置apple的地方
        self.prop_spawn_places = {pos: 1 for pos in self.grids if self.grids[pos] is None}
        # move
        self.move_elapsed = 0

        self.spawn_prop()

    def update(self, _):
        self.move_snake()

    def move_snake(self):
        self.move_elapsed += 1
        if self.move_elapsed > 50:
            self.move_elapsed = 0
            self.snake.move()

    def draw_grid_line(self):
        for x in range(self.config.columns + 1):
            self.add(Line(start=(self.config.ORIGIN.x + x * self.config.GRID_SIZE, self.config.ORIGIN.y),
                          end=(self.config.ORIGIN.x + x * self.config.GRID_SIZE,
                               self.config.ORIGIN.y + self.config.rows * self.config.GRID_SIZE),
                          color=(0, 0, 0, 255)))
        for y in range(self.config.rows + 1):
            self.add(Line(start=(self.config.ORIGIN.x, self.config.ORIGIN.y + y * self.config.GRID_SIZE),
                          end=(self.config.ORIGIN.x + self.config.columns * self.config.GRID_SIZE,
                               self.config.ORIGIN.y + y * self.config.GRID_SIZE),
                          color=(0, 0, 0, 255)))

    def on_key_press(self, key_, *_):
        # 规定不能倒着转向, 不然导致误触死亡
        if key_ == key.UP:
            if not self.snake.direction == "down":
                self.snake.direction = "up"
        elif key_ == key.DOWN:
            if not self.snake.direction == "up":
                self.snake.direction = "down"
        elif key_ == key.LEFT:
            if not self.snake.direction == "right":
                self.snake.direction = "left"
        elif key_ == key.RIGHT:
            if not self.snake.direction == "left":
                self.snake.direction = "right"

        if not self.is_game_over:
            if self.is_win:
                if key_ == key.U:
                    self.upgrade_level()
        else:
            if key_ == key.R:
                self.restart()

    def spawn_prop(self):
        pos = choice(list(self.prop_spawn_places))
        apple = AppleProp(Pos(pos, None), self.config)
        self.add(apple)
        self.grids[pos] = apple

    def game_over(self):
        self.unschedule(self.update)
        self.is_game_over = True
        self.create_label(text="Game Over~",
                          pos=(director.get_window_size()[0] / 2, director.get_window_size()[1] / 2),
                          size=100,
                          color=(0, 0, 0, 255))
        self.create_label(text="Press 'r' to restart",
                          pos=(director.get_window_size()[0] / 2, director.get_window_size()[1] / 2 - 120),
                          size=50)

    def succeed(self):
        self.unschedule(self.update)
        self.is_win = True
        self.create_label(text="You win!",
                          pos=(director.get_window_size()[0] / 2, director.get_window_size()[1] / 2),
                          size=70,
                          color=(0, 0, 0, 255))
        self.create_label(text="Press 'u' to a higher level",
                          pos=(director.get_window_size()[0] / 2, director.get_window_size()[1] / 2 - 120),
                          size=50)

    def create_label(self, text, pos, size, color=(255, 255, 255, 255)):
        label = Label(
            text=text,
            position=pos,
            font_size=size,
            color=color,
            anchor_x="center",
            anchor_y="center"
        )
        label.do(FadeIn(2))
        self.add(label, z=1000)

    def restart(self):
        for _, child in self.children:
            if isinstance(child, (Line, SnakeBody, SnakeHead, Label, AppleProp)):
                self.remove(child)
        self.init()
        self.schedule(self.update)

    def upgrade_level(self):
        self.config.upgrade_level()
        self.restart()
