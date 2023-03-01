from random import randint
from math import ceil

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.draw import Line
from cocos.text import Label


class DemoScene(Scene):
    def __init__(self):
        super(DemoScene, self).__init__()

        self.add(ColorLayer(255, 255, 255, 200), z=1)  # 背景涂白

        k = 0
        self.draw_dividing_lines()
        for i in range(edge_grid_num):
            for j in range(edge_grid_num):
                tmp = layers[k]()
                tmp.anchor = 0, 0
                tmp.scale = 1 / edge_grid_num
                tmp.position = i * width, j * height
                tmp.add(self.create_label(layers[k].__name__[:-5]))
                self.add(tmp, z=2)
                k += 1
                if k == len(layers):
                    return

    def create_label(self, name):
        w, h = director.get_window_size()
        label = Label(name,
                      position=(w / 2, h - 30),
                      font_size=30,
                      color=(0, 0, 0, 255),
                      anchor_x="center",
                      anchor_y="center")
        return label

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


class SortLayer(Layer):
    def __init__(self, sort_kind):
        super().__init__()

        self.nums = [Bar(num=num) for num in data]
        for idx, bar in enumerate(self.nums):
            bar.position = idx * BAR_WIDTH, 0
            self.add(bar, z=1)

        self.elapsed = 1
        self.i = 0
        self.exchange_pos = []
        eval(f"self.{sort_kind}()")
        if self.exchange_pos:  # 可能已经有序, 则无序排序
            self.bar_backup = self.nums[self.exchange_pos[0][0]]  # 默认值

            self.schedule(self.update)

    def update(self, dt):
        self.elapsed += 1
        self.bar_backup.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        if self.elapsed > threshold:
            self.elapsed = 1  # tick
            self.exchange()
            self.i += 1
            if self.i == len(self.exchange_pos):
                self.unschedule(self.update)
            self.bar_backup = self.nums[self.right]
            self.bar_backup.color = 255, 0, 0


class BubbleSortLayer(SortLayer):
    def __init__(self):
        super().__init__("_bubble_sort")

    def _bubble_sort(self):
        nums = list(bar.num for bar in self.nums)
        k = 0
        for i in range(k, len(nums)):
            is_exchange = False
            for j in range(len(nums) - 1, i, -1):
                if nums[j] < nums[j - 1]:
                    is_exchange = True
                    nums[j - 1], nums[j] = nums[j], nums[j - 1]
                    self.exchange_pos.append((j - 1, j))
                    k = j - 1
            if not is_exchange:
                return

    def exchange(self):
        self.left, self.right = self.exchange_pos[self.i]
        self.nums[self.right].position, self.nums[self.left].position = self.nums[self.left].position, self.nums[
            self.right].position
        self.nums[self.right], self.nums[self.left] = self.nums[self.left], self.nums[self.right]


class Bar(ColorLayer):
    def __init__(self, num):
        super().__init__(127, 127, 127, 255, BAR_WIDTH, num)

        self.anchor = 0, 0
        self.width -= 3
        self.num = num

    def __gt__(self, other):
        return self.num > other.num

    def __ge__(self, other):
        return self.num >= other.num

    def __lt__(self, other):
        return self.num < other.num

    def __le__(self, other):
        return self.num <= other.num


if __name__ == '__main__':
    director.init(width=1200, height=700)
    width, height = director.get_window_size()

    BAR_WIDTH = 20  # 最好被width整除
    COLUMNS = width // BAR_WIDTH

    # data range(数据范围)
    data_lowest, data_highest = 50, height - 50  # 随便的数据
    # data_lowest, data_highest = height - 200, height - 150  # 测试(数据极度有序)
    data_lowest, data_highest = 10, height - 10  # 测试(数据极度无序)

    threshold = 0  # 调速用, 大于此阈值执行一次操作
    data = [randint(data_lowest, data_highest) for _ in range(COLUMNS)]  # 共用的sort数据
    # data = [num for num in range(data_lowest, data_highest, 10)][:COLUMNS]  # 共用的sort数据
    # data = [num for num in range(data_highest, data_lowest, -10)][:COLUMNS]  # 共用的sort数据

    layers = [BubbleSortLayer, InsertionSortLayer,
              SelectionSortLayer, ShellSortLayer,
              QucikSortLayer, CockTailSortLayer]
    # layers = [BubbleSortLayer]  # 调试
    # layers = [CockTailSortLayer, BubbleSortLayer]
    LAYER_NUMS = len(layers)
    edge_grid_num = ceil(LAYER_NUMS ** 0.5)
    width, height = width / edge_grid_num, height / edge_grid_num

    director.run(DemoScene())
