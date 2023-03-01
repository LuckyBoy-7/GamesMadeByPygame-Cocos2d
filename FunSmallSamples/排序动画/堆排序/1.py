"""
question: 1. 为什么鸡尾酒排序和冒牌排序看不出区别呢(冒泡优化过了)?
             因为这是回放, 中间的过程没有, 只有交换的过程,
             而这两者的交换次数是一样的, 这也是为什么这里的桶排序只要桶够多, 看起来基本上
             一遍就可以排序好, 但实际上也没那么快
"""

from random import randint
from math import ceil

from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.draw import Line
from cocos.text import Label


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


class SortScene(Scene):
    def __init__(self):
        super(SortScene, self).__init__()

        self.add(ColorLayer(255, 255, 255, 200), z=1)  # 背景涂白

        self.draw_dividing_lines()
        self.draw_layers()

    def draw_layers(self):
        k = 0
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

    @staticmethod
    def create_label(name):
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
    left: int
    right: int
    bar_backup: Bar

    def __init__(self, sort_kind=None):
        super().__init__()

        self.nums = [Bar(num=num) for num in data]
        for idx, bar in enumerate(self.nums):
            bar.position = idx * BAR_WIDTH, 0
            self.add(bar, z=1)

        self.elapsed = 1
        self.i = 0
        self.exchange_pos = []
        if sort_kind:
            eval(f"self.{sort_kind}(list(self.nums))")
        if self.exchange_pos:  # 可能已经有序, 则无需排序
            self.schedule(self.update)


class HeapSortLayer(SortLayer):
    def __init__(self):
        super().__init__()

        self.heap_list = [-1]
        self.current_size = 0

        for num in [bar.num for bar in self.nums]:
            self.insert(num)
        for i in range(self.current_size):
            self.del_min()

        self.bar_backup = self.nums[self.exchange_pos[0][0]]  # 默认值
        self.schedule(self.update)

    def perc_up(self, i):
        while i // 2 > 0:
            left = i // 2
            if self.heap_list[left] < self.heap_list[i]:
                self.heap_list[left], self.heap_list[i] = self.heap_list[i], self.heap_list[left]
                self.exchange_pos.append((left - 1, i - 1))
            i //= 2

    def insert(self, val):
        self.heap_list.append(val)
        self.current_size += 1
        self.perc_up(self.current_size)

    def perc_down(self, i):
        while i * 2 <= self.current_size:
            mc = self.get_max_child(i)
            if self.heap_list[i] < self.heap_list[mc]:
                self.heap_list[i], self.heap_list[mc] = self.heap_list[mc], self.heap_list[i]
                self.exchange_pos.append((mc - 1, i - 1))
            i = mc

    def get_max_child(self, i):
        left = i * 2
        right = i * 2 + 1
        if right > self.current_size:
            return left
        else:
            if self.heap_list[left] < self.heap_list[right]:
                return right
            return left

    def del_min(self):
        retval = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.exchange_pos.append((0, self.current_size - 1))
        self.current_size -= 1
        self.heap_list.pop()
        self.perc_down(1)

        return retval

    def update(self, dt):
        self.elapsed += 1
        self.bar_backup.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        if self.elapsed > threshold:
            self.elapsed = 1  # tick
            self.left, self.right = self.exchange_pos[self.i]
            self.bar_backup = self.nums[self.left]
            self.nums[self.left].position, self.nums[self.right].position = self.nums[self.right].position, self.nums[
                self.left].position
            self.nums[self.left], self.nums[self.right] = self.nums[self.right], self.nums[self.left]
            self.i += 1
            if self.i == len(self.exchange_pos):
                self.unschedule(self.update)
            self.bar_backup.color = 255, 0, 0


if __name__ == '__main__':
    director.init(width=1200, height=700)
    width, height = director.get_window_size()

    BAR_WIDTH = 10  # 最好被width整除
    COLUMNS = width // BAR_WIDTH

    # data range(数据范围)
    data_lowest, data_highest = 10, height - 10

    threshold = 0  # 调速用, 大于此阈值执行一次操作
    data = [randint(data_lowest, data_highest) for _ in range(COLUMNS)]  # 共用的sort数据
    # data = [num for num in range(data_lowest, data_highest, 5)][:COLUMNS]  # 共用的sort数据
    # data = [num for num in range(data_highest, data_lowest, -5)][:COLUMNS]  # 共用的sort数据

    # layers = [BucketSortLayer]
    layers = [HeapSortLayer]
    LAYER_NUMS = len(layers)
    edge_grid_num = ceil(LAYER_NUMS ** 0.5)
    width, height = width / edge_grid_num, height / edge_grid_num

    director.run(SortScene())
