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

        self.nums = [Bar(num=randint(100, 500)) for _ in range(COLUMNS)]
        for idx, bar in enumerate(self.nums):
            bar.position = idx * BAR_WIDTH, 0
            self.add(bar, z=1)

        self.elapsed = 1

        self.i = 0
        self.bar_backup = self.nums[0]  # 默认值
        self.exchange_pos = []
        self.shell_sort(self.nums)
        # print([bar.num for bar in self.nums])
        # print(len(self.exchange_pos))

        self.schedule(self.update)

    def insertion_sort(self, start, gap, alist):
        for i in range(start, len(alist) - gap, gap):
            j = i + gap
            backup = alist[j].num
            while j > start and backup < alist[j - gap].num:
                alist[j].num = alist[j - gap].num
                self.exchange_pos.append((j, alist[j - gap].num))
                j -= gap
            alist[j].num = backup
            self.exchange_pos.append((j, backup))

    def shell_sort(self, alist):
        gap = len(alist)
        while gap != 0:
            gap //= 2
            for start in range(gap):
                self.insertion_sort(start, gap, alist)

    def update(self, dt):
        self.elapsed += 1
        self.bar_backup.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        if self.elapsed > 0:
            self.elapsed = 1  # tick
            right, num = self.exchange_pos[self.i]
            self.nums[right].scale_y = num / self.nums[right].height
            self.i += 1
            if self.i == len(self.exchange_pos):
                self.unschedule(self.update)
            self.bar_backup = self.nums[right]
            self.bar_backup.color = 255, 0, 0


class Bar(ColorLayer):
    def __init__(self, num):
        # 边框也会跟着scale变, 看着难受, 但又改不了height
        super().__init__(127, 127, 127, 255, BAR_WIDTH - 1, num)  # 留有间隙

        self.num = num
        self.anchor = 0, 0

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

    director.run(DemoScene())
