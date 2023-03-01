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

        self.nums = [randint(10, 200) for _ in range(COLUMNS)]
        self.nums_map = [Bar] * COLUMNS  # 通过索引同时访问Bar对象和数字
        for idx, num in enumerate(self.nums):
            tmp = Bar(idx, num * 3)
            self.nums_map[idx] = tmp
            self.add(tmp, z=1)
        self.elapsed = 1
        self.i = 0
        self.j = self.i + 1
        self.min = self.i
        self.backup = self.nums_map[0]  # 默认值

        self.schedule(self.update)

    def update(self, dt):
        self.elapsed += 1
        self.backup.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        if self.elapsed > 3:
            self.elapsed = 1  # tick
            self.backup = self.nums_map[self.j]
            self.backup.color = 255, 0, 0

            if self.nums[self.j] < self.nums[self.min]:
                self.min = self.j

            self.j += 1
            if self.j == len(self.nums):
                [self.nums_map[self.i].position,
                 self.nums_map[self.min].position] = [self.nums_map[self.min].position,  # 更新坐标
                                                      self.nums_map[self.i].position]
                self.nums_map[self.min], self.nums_map[self.i] = self.nums_map[self.i], self.nums_map[self.min]
                self.nums[self.min], self.nums[self.i] = self.nums[self.i], self.nums[self.min]  # 更新map

                self.i += 1
                self.j = self.i + 1
                self.min = self.i
                if self.i == len(self.nums) - 1:
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
