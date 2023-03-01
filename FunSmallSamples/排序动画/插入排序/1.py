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
        self.j = self.i + 1
        self.num_backup = self.nums[self.j].num
        self.bar_backup = self.nums[0]  # 默认值

        self.schedule(self.update)

    def update(self, dt):
        self.elapsed += 1
        self.bar_backup.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        if self.elapsed > 4:
            self.elapsed = 1  # tick
            self.bar_backup = self.nums[self.j]
            self.bar_backup.color = 255, 0, 0
            
            if self.i < len(self.nums) - 1:  # 未排完序
                if self.j > 0:
                    if self.num_backup < self.nums[self.j - 1].num:
                        self.nums[self.j].scale_y = self.nums[self.j - 1].num / self.nums[self.j].height
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

    BAR_WIDTH = 40  # 最好被width整除
    COLUMNS = width // BAR_WIDTH

    director.run(DemoScene())
