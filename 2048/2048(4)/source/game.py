from random import sample, choices

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from pyglet.window import key
from cocos.draw import Line
from cocos.actions import FadeOut, FadeIn, ScaleTo, Delay, Hide, Show

from settings import Settings
from grid import Grid, NumGrid, ReduceGrid, UniversalGrid
from position import Pos
from widgets import Hint
from stats import stats


class GameScene(Scene):
    def __init__(self):
        super(GameScene, self).__init__()

        self.add(ColorLayer(255, 255, 255, 255), z=1)  # 背景涂白
        self.add(GameLayer(), z=2)


class GameLayer(Layer):
    grids: dict

    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()

        self.draw_grid_lines()

        self.grids_init()
        self.hint = Hint(self)

        stats.is_start = True
        self.schedule(self.update)

    def update(self, _):
        self.hint.update_hint()

    def on_key_press(self, k, *_):
        if not stats.is_game_over:
            if k == key.UP or k == key.W:
                self.move_grid_up()
            elif k == key.DOWN or k == key.S:
                self.move_grid_down()
            elif k == key.LEFT or k == key.A:
                self.move_grid_left()
            elif k == key.RIGHT or k == key.D:
                self.move_grid_right()
        elif k == key.ENTER:
            print(123)
            self.restart()

    def _move(self, *args, sign):
        slow_pos, fast_pos, pos, slow, fast = args
        if self.grids[fast_pos]:  # fast处有东西
            if self.grids[slow_pos]:
                self.grids[slow_pos].exec(self.grids[fast_pos], self, pos)
                slow = eval(f"slow {sign} 1")
            else:
                self.grids[fast_pos].move_to(slow_pos, self)  # 如果slow处没东西, 就把fast处的移过去
        return slow

    def move_grid_up(self):
        for col in range(Settings.COLUMNS):
            slow = Settings.ROWS - 1
            fast = slow - 1
            while fast != -1:
                fast_pos = Pos(col, fast)
                slow_pos = Pos(col, slow)  # 都要不断更新
                args = slow_pos, fast_pos, Pos(col, slow - 1), slow, fast
                slow = self._move(*args, sign="-")
                fast -= 1

        self.random_grid()

    def move_grid_down(self):
        for col in range(Settings.COLUMNS):
            slow = 0
            fast = slow + 1
            while fast != Settings.ROWS:
                fast_pos = Pos(col, fast)
                slow_pos = Pos(col, slow)  # 都要不断更新
                args = slow_pos, fast_pos, Pos(col, slow + 1), slow, fast
                slow = self._move(*args, sign="+")
                fast += 1
        self.random_grid()

    def move_grid_left(self):
        for row in range(Settings.ROWS):
            slow = 0
            fast = slow + 1
            while fast != Settings.COLUMNS:
                fast_pos = Pos(fast, row)
                slow_pos = Pos(slow, row)  # 都要不断更新
                args = slow_pos, fast_pos, Pos(slow + 1, row), slow, fast
                slow = self._move(*args, sign="+")
                fast += 1
        self.random_grid()

    def move_grid_right(self):
        for row in range(Settings.ROWS):
            slow = Settings.COLUMNS - 1
            fast = slow - 1
            while fast != -1:
                fast_pos = Pos(fast, row)
                slow_pos = Pos(slow, row)  # 都要不断更新
                args = slow_pos, fast_pos, Pos(slow - 1, row), slow, fast
                slow = self._move(*args, sign="-")
                fast -= 1
        self.random_grid()

    def grids_init(self):
        """刚开始init的grids"""
        self.grids = {Pos(col, row): None
                      for col in range(Settings.COLUMNS)
                      for row in range(Settings.ROWS)}

        for pos in sample(list(self.grids), 5):
            self.set_grid(power=1, pos=pos)

    def set_grid(self, power, pos, is_inflate=False):
        if power == -1:  # reduce grid
            temp = ReduceGrid(pos=pos)
        elif power == 0:
            temp = UniversalGrid(pos=pos)
        else:
            temp = NumGrid(power=power, pos=pos)
        self.grids[pos] = temp
        self.add(temp, z=10)

        if stats.is_start:  # 刚开始生成的不能算作分数
            temp.update_score()

        if is_inflate:  # 2合1
            temp.do(ScaleTo(1.2, 0.05) + ScaleTo(0.8, 0.1) + ScaleTo(1, 0.05))
        else:  # 普通生成
            temp.do(Hide() + Delay(Settings.move_time - 0.2) + Show() + FadeIn(Settings.fade_time))

    def del_grid(self, pos):
        self.grids[pos].do(FadeOut(Settings.fade_time))
        self.remove(self.grids[pos])
        self.grids[pos] = None

    def double_grid(self, pos):
        old_pow = self.grids[pos].power
        self.del_grid(pos)
        self.set_grid(power=old_pow + 1, pos=pos, is_inflate=True)

    def reduce_grid(self, pos):
        old_pow = self.grids[pos].power
        self.del_grid(pos)
        self.set_grid(power=old_pow - 1, pos=pos, is_inflate=True)

    def random_grid(self):
        chosen = [pos for pos in self.grids if self.grids[pos] is None]
        threshold = 2
        if chosen:
            times = threshold if len(chosen) >= threshold else len(chosen)
            poses = sample(chosen, times)
            for pos in poses:
                if pos:
                    self.set_grid(power=choices(*zip( [-1, 100],
                                                     # [0, 100],
                                                     [1, 20],
                                                     [2, 80])
                                                )[0], pos=pos)

        if len(chosen) <= threshold:  # 抽完了在判断, 这样节省内存
            for pos in self.grids:
                for i, j in [(0, -1), (1, 0)]:
                    if Pos.check_valid(pos.x + i, pos.y + j):
                        if self.grids[Pos(pos.x + i, pos.y + j)].power == self.grids[pos].power:
                            return
            self.hint.game_over()

    def draw_grid_lines(self):
        for x in range(Settings.COLUMNS + 1):
            self.add(Line(start=(Settings.ORIGIN[0] + x * Settings.GRID_SIZE, Settings.ORIGIN[1]),
                          end=(Settings.ORIGIN[0] + x * Settings.GRID_SIZE,
                               Settings.ORIGIN[1] + Settings.ROWS * Settings.GRID_SIZE),
                          color=(0, 0, 0, 255)))
        for y in range(Settings.ROWS + 1):
            self.add(Line(start=(Settings.ORIGIN[0], Settings.ORIGIN[1] + y * Settings.GRID_SIZE),
                          end=(Settings.ORIGIN[0] + Settings.COLUMNS * Settings.GRID_SIZE,
                               Settings.ORIGIN[1] + y * Settings.GRID_SIZE),
                          color=(0, 0, 0, 255)))

    def restart(self):
        stats.restart()
        self.parent.remove(self)
        self.parent.add(GameLayer(), z=2)
