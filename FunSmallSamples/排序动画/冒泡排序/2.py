from random import randint

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.draw import Line


class DemoScene(Scene):
    def __init__(self):
        super(DemoScene, self).__init__()

        self.add(ColorLayer(255, 255, 255, 200), z=1)  # 背景涂白
        self.add(DemoLayer(), z=2)


class DemoLayer(Layer):
    def __init__(self):
        super().__init__()

        self.nums = [Bar(num=randint(10, 200)) for _ in range(COLUMNS)]
        for idx, bar in enumerate(self.nums):
            bar.position = idx * BAR_WIDTH, 0
            self.add(bar, z=1)

        self.elapsed = 1
        self.i = 0
        self.j = len(self.nums) - 1
        self.backup = self.nums[0]  # 默认值

        self.schedule(self.update)

    def update(self, dt):
        self.elapsed += 1
        self.backup.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        if self.elapsed > 2:
            self.elapsed = 1  # tick
            self.backup = self.nums[self.j]
            self.backup.color = 255, 0, 0

            if self.j > self.i:
                if self.nums[self.j] < self.nums[self.j - 1]:
                    [self.nums[self.j].position,
                     self.nums[self.j - 1].position] = [self.nums[self.j - 1].position,  # 更新坐标
                                                        self.nums[self.j].position]
                    self.nums[self.j], self.nums[self.j - 1] = self.nums[self.j - 1], self.nums[self.j]  # 更新map
                self.j -= 1
            else:
                if self.i < len(self.nums) - 1:
                    self.i += 1
                    self.j = len(self.nums) - 1
                else:
                    self.unschedule(self.update)


class Bar(ColorLayer):
    def __init__(self, num):
        super().__init__(127, 127, 127, 255, BAR_WIDTH, num * 3)

        self.num = num

        self.draw_outlines()

    def __gt__(self, other):
        return self.num > other.num

    def __ge__(self, other):
        return self.num >= other.num

    def __lt__(self, other):
        return self.num < other.num

    def __le__(self, other):
        return self.num <= other.num

    def draw_outlines(self):
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

    BAR_WIDTH = 40  # 最好被width整除
    COLUMNS = width // BAR_WIDTH

    director.run(DemoScene())
