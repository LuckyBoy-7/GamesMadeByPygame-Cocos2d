from random import randint
from math import ceil

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.draw import Line


class DemoScene(Scene):
    def __init__(self):
        super(DemoScene, self).__init__()

        self.add(ColorLayer(255, 255, 255, 200), z=1)  # 背景涂白

        k = 0
        self.draw_dividing_lines()
        for i in range(edge_grid_num):
            for j in range(edge_grid_num):
                tmp = layers[k]()
                tmp.position = i * width, j * height
                tmp.anchor = 0, 0
                tmp.scale = 1 / edge_grid_num
                self.add(tmp, z=2)
                k += 1
                if k == len(layers):
                    return

    def draw_dividing_lines(self):  # 画分割线
        w, h = director.get_window_size()
        for i in range(int(LAYER_NUMS ** 0.5) + 2):
            self.add(Line(start=(0, height * i),  # 水平线
                          end=(w, height * i),
                          color=(0, 200, 0, 255),
                          stroke_width=2), z=10)
        for j in range(int(LAYER_NUMS ** 0.5) + 2):
            self.add(Line(start=(width * j, 0),  # 竖直线
                          end=(width * j, h),
                          color=(0, 200, 0, 255),
                          stroke_width=2), z=10)


class BubbleSortLayer(Layer):
    def __init__(self):
        super().__init__()

        self.nums = [OutlineBar(num=randint(data_lowest, data_highest)) for _ in range(COLUMNS)]
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
        if self.elapsed > threshold:
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


class SelectionSortLayer(Layer):
    def __init__(self):
        super().__init__()

        self.nums = [OutlineBar(num=randint(data_lowest, data_highest)) for _ in range(COLUMNS)]
        for idx, bar in enumerate(self.nums):
            bar.position = idx * BAR_WIDTH, 0
            self.add(bar, z=1)
        self.elapsed = 1
        self.i = 0
        self.j = self.i + 1
        self.min = self.i
        self.backup = self.nums[0]  # 默认值

        self.schedule(self.update)

    def update(self, dt):
        self.elapsed += 1
        self.backup.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        if self.elapsed > threshold:
            self.elapsed = 1  # tick
            self.backup = self.nums[self.j]
            self.backup.color = 255, 0, 0

            if self.nums[self.j] < self.nums[self.min]:
                self.min = self.j

            self.j += 1
            if self.j == len(self.nums):
                [self.nums[self.i].position,
                 self.nums[self.min].position] = [self.nums[self.min].position,  # 更新坐标
                                                  self.nums[self.i].position]
                self.nums[self.min], self.nums[self.i] = self.nums[self.i], self.nums[self.min]

                self.i += 1
                self.j = self.i + 1
                self.min = self.i
                if self.i == len(self.nums) - 1:
                    self.unschedule(self.update)


class InsertionSortLayer(Layer):
    def __init__(self):
        super().__init__()

        self.nums = [InsertionBar(num=randint(data_lowest, data_highest)) for _ in range(COLUMNS)]
        for idx, bar in enumerate(self.nums):
            bar.position = idx * BAR_WIDTH, 0
            self.add(bar, z=1)

        self.elapsed = 1
        self.i = 0
        self.j = self.i + 1
        self.num_backup = self.nums[self.j].num
        self.bar_backup = self.nums[0]  # 默认值

        self.schedule(self.update)

    def update(self, dt):
        self.elapsed += 1
        self.bar_backup.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        if self.elapsed > threshold:
            self.elapsed = 1  # tick
            self.bar_backup = self.nums[self.j]
            self.bar_backup.color = 255, 0, 0

            if self.i < len(self.nums) - 1:  # 未排完序
                if self.j > 0:
                    if self.num_backup < self.nums[self.j - 1].num:
                        self.nums[self.j].scale_y = self.nums[self.j - 1].num / self.nums[
                            self.j].height
                        self.nums[self.j].num = self.nums[self.j - 1].num
                        self.j -= 1
                    if self.num_backup >= self.nums[self.j - 1].num or self.j == 0:
                        self.nums[self.j].scale_y = self.num_backup / self.nums[self.j].height
                        self.nums[self.j].num = self.num_backup
                        self.i += 1
                        self.j = self.i + 1
                        if not self.j == len(self.nums):
                            self.num_backup = self.nums[self.j].num
                        else:
                            self.unschedule(self.update)
            # print([num.num for num in self.nums])


class Bar(ColorLayer):
    def __init__(self, num):
        super().__init__(127, 127, 127, 255, BAR_WIDTH, num)

        self.num = num

    def __gt__(self, other):
        return self.num > other.num

    def __ge__(self, other):
        return self.num >= other.num

    def __lt__(self, other):
        return self.num < other.num

    def __le__(self, other):
        return self.num <= other.num


class OutlineBar(Bar):
    def __init__(self, num):
        super().__init__(num)
        self.draw_outlines()

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


class InsertionBar(Bar):
    def __init__(self, num):
        super().__init__(num)
        self.anchor = 0, 0
        self.width -= 2


if __name__ == '__main__':
    director.init(width=1200, height=700)
    width, height = director.get_window_size()

    BAR_WIDTH = 60  # 最好被width整除
    COLUMNS = width // BAR_WIDTH

    # data range
    data_lowest, data_highest = 100, height - 50
    threshold = 0

    layers = [BubbleSortLayer, InsertionSortLayer, SelectionSortLayer]
    LAYER_NUMS = len(layers)
    edge_grid_num = ceil(LAYER_NUMS ** 0.5)
    width, height = width / edge_grid_num, height / edge_grid_num

    director.run(DemoScene())
