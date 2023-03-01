from random import randint

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.draw import Line
from cocos.text import Label
from cocos.rect import Rect
from cocos.actions import FadeIn, Delay, Hide, Show, MoveTo


class DemoScene(Scene):
    def __init__(self):
        super(DemoScene, self).__init__()

        self.add(ColorLayer(255, 255, 255, 200), z=1)  # 背景涂白
        self.add(DemoLayer(), z=2)


class DemoLayer(Layer):
    def __init__(self):
        super().__init__()

        self.nums = [randint(1, 100) for _ in range(COLUMNS)]
        self.nums_map = [Bar] * COLUMNS  # 通过索引同时访问Bar对象和数字
        for idx, num in enumerate(self.nums):
            tmp = Bar(idx, num * 3)
            self.nums_map[idx] = tmp
            self.add(tmp, z=1)
        self.elapsed = 1
        self.i = 0
        self.j = len(self.nums) - 1

        self.schedule(self.update)

    def update(self, dt):
        self.elapsed += 1
        if self.elapsed > 2:
            self.elapsed = 1  # tick

            if self.j > self.i:
                if self.nums[self.j] < self.nums[self.j - 1]:
                    [self.nums_map[self.j].position,
                     self.nums_map[self.j - 1].position] = [self.nums_map[self.j - 1].position,  # 更新坐标
                                                            self.nums_map[self.j].position]
                    self.nums_map[self.j], self.nums_map[self.j - 1] = self.nums_map[self.j - 1], self.nums_map[self.j]
                    self.nums[self.j], self.nums[self.j - 1] = self.nums[self.j - 1], self.nums[self.j]  # 更新map
                self.j -= 1
            else:
                if self.i < len(self.nums) - 1:
                    self.i += 1
                    self.j = len(self.nums) - 1
                else:
                    self.unschedule(self.update)


class Bar(ColorLayer):
    def __init__(self, idx, height):
        super().__init__(127, 127, 127, 255, BAR_WIDTH, height)

        self.position = idx * BAR_WIDTH, 0
        self.add(Line(start=(0, 0),
                      end=(0, self.height),
                      color=(0, 0, 0, 255),
                      stroke_width=2), z=10)
        self.add(Line(start=(0, self.height),
                      end=(self.width, self.height),
                      color=(0, 0, 0, 255),
                      stroke_width=2), z=10)
        self.add(Line(start=(self.width, 0),
                      end=(self.width, self.height),
                      color=(0, 0, 0, 255),
                      stroke_width=2), z=10)


if __name__ == '__main__':
    director.init(width=1200, height=700)
    width, height = director.get_window_size()

    BAR_WIDTH = 60  # 最好被width整除
    COLUMNS = width // BAR_WIDTH

    director.run(DemoScene())
