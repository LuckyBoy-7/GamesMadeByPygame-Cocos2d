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
        self.bar_backup_pivot = self.nums[0]  # 默认值
        self.bar_backup_left = self.nums[0]  # 默认值
        self.bar_backup_right = self.nums[0]  # 默认值
        self.exchange_pos = []
        self.quick_sort(0, len(self.nums) - 1, list(self.nums))

        self.schedule(self.update)

    def quick_sort(self, start, end, alist):
        pivot = start
        left = pivot + 1
        right = end
        while True:
            while left <= right and alist[left] <= alist[pivot]:
                self.exchange_pos.append((-1, left, right, pivot))  # 一定要先append
                left += 1
            while left <= right and alist[right] >= alist[pivot]:
                self.exchange_pos.append((-1, left, right, pivot))  # 左交换, 右交换, 左基准, 右基准, 当前基准
                right -= 1
            if left < right:
                self.exchange_pos.append((-2, left, right, pivot))
                alist[left], alist[right] = alist[right], alist[left]
            else:
                self.exchange_pos.append((-3, left, right, pivot))  # -1表示不交换, -2交换左右, -3交换pivot和right
                alist[pivot], alist[right] = alist[right], alist[pivot]
                break

        if start < right - 1:
            self.quick_sort(start, right - 1, alist)
        if right + 1 < end:
            self.quick_sort(right + 1, end, alist)

    def update(self, dt):
        self.elapsed += 1
        self.bar_backup_pivot.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        self.bar_backup_left.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        self.bar_backup_right.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        if self.elapsed > 0:
            self.elapsed = 1  # tick
            status, left, right, pivot = self.exchange_pos[self.i]
            if status == -2:  # -1表示不交换, -2交换左右, -3交换pivot和right
                self.nums[left].position, self.nums[right].position = self.nums[right].position, self.nums[
                    left].position
                self.nums[left], self.nums[right] = self.nums[right], self.nums[left]
            elif status == -3:
                self.nums[pivot].position, self.nums[right].position = self.nums[right].position, self.nums[
                    pivot].position
                self.nums[pivot], self.nums[right] = self.nums[right], self.nums[pivot]
            self.i += 1
            if self.i == len(self.exchange_pos):
                self.unschedule(self.update)
            self.bar_backup_pivot = self.nums[pivot]
            self.bar_backup_pivot.color = 255, 0, 0
            if left < len(self.nums):
                self.bar_backup_left = self.nums[left]
                self.bar_backup_left.color = 0, 255, 0
            self.bar_backup_right = self.nums[right]
            self.bar_backup_right.color = 0, 0, 255



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

    BAR_WIDTH = 10  # 最好被width整除
    COLUMNS = width // BAR_WIDTH

    director.run(DemoScene())
