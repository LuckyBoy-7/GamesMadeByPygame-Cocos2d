"""
former bug: 1. if fast_pos != Pos(col, slow - 1):
                   # 不知道为什么去掉会有bug
                   # 因为每次只更新了grid的position, 而没有改变pos
                   # 淦, 这个bug找了我好久
"""

from random import sample, choice, randint

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.sprite import Sprite
from pyglet.window import key

from settings import Settings
from image import Image
from grid import Grid
from position import Pos


class GameScene(Scene):
    def __init__(self):
        super(GameScene, self).__init__()

        self.add(ColorLayer(255, 255, 255, 255), z=1)  # 背景涂白
        self.add(Sprite(Image.background, position=(Settings.MID_X, Settings.MID_Y)), z=2)  # 游戏网格背景
        self.add(GameLayer(), z=3)


class GameLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()

        self.grids = {Pos(col, row): None
                      for col in range(Settings.COLUMNS)
                      for row in range(Settings.ROWS)}
        self.grid_init()

    def on_key_press(self, k, *_):
        if k == key.UP or k == key.W:
            self.move_grid_up()
        # elif k == key.DOWN or k == key.S:
        #     self.move_grid_down()
        # elif k == key.LEFT or k == key.A:
        #     self.move_grid_left()
        # elif k == key.RIGHT or k == key.D:
        #     self.move_grid_right()

    def _move(self, ):
        eval(
            f"""
            for col in range(Settings.COLUMNS):
                slow = Settings.ROWS - 1
                for fast in range(slow - 1, -1, -1):
                    fast_pos = Pos(col, fast)
                    slow_pos = Pos(col, slow)  # 都要不断更新
                    if self.grids[fast_pos]:  # fast处是grid
                        if self.grids[slow_pos]:
                            if self.grids[fast_pos].power == self.grids[slow_pos].power:
                                self.del_grid(fast_pos)
                                self.double_grid(slow_pos)
                            else:
                                if not fast_pos == Pos(col, slow - 1):
                                    self.grids[fast_pos].move_to(Pos(col, slow - 1), self)
                            slow -= 1
                        else:
                            self.grids[fast_pos].move_to(slow_pos, self)  # 如果slow处没东西, 就把fast处的移过去
    
            self.random_grid()
            """
        )

    def move_grid_up(self):
        for col in range(Settings.COLUMNS):
            slow = Settings.ROWS - 1
            for fast in range(slow - 1, -1, -1):
                fast_pos = Pos(col, fast)
                slow_pos = Pos(col, slow)  # 都要不断更新
                if self.grids[fast_pos]:  # fast处是grid
                    # print(fast_pos.pos, self.grids[fast_pos].pos.pos)
                    if self.grids[slow_pos]:
                        if self.grids[fast_pos].power == self.grids[slow_pos].power:  # grid_num相同
                            self.del_grid(fast_pos)
                            self.double_grid(slow_pos)
                        else:  # grid_num不同
                            self.grids[fast_pos].move_to(Pos(col, slow - 1), self)
                        slow -= 1
                    else:
                        self.grids[fast_pos].move_to(slow_pos, self)  # 如果slow处没东西, 就把fast处的移过去
        self.random_grid()

    def grid_init(self):
        for pos in sample(list(self.grids), 16):
            self.set_grid(power=1, pos=pos)

    def set_grid(self, power, pos):
        temp = Grid(power=power, pos=pos)
        self.grids[pos] = temp
        self.add(temp, z=10)

    def del_grid(self, pos):
        self.remove(self.grids[pos])
        self.grids[pos] = None

    def double_grid(self, pos):
        old_pow = self.grids[pos].power
        self.del_grid(pos)
        self.set_grid(power=old_pow + 1, pos=pos)

    def random_grid(self):
        chosen = [pos for pos in self.grids if self.grids[pos] is None]
        if chosen:
            pos = choice(chosen)
            if pos:
                if randint(1, 10) <= 8:  # 80%出2
                    self.set_grid(1, pos)
                else:  # 20%出4
                    self.set_grid(2, pos)
        else:  # 不是game_over
            print("sdkjf")
