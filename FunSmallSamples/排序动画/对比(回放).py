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

    def update(self, dt):
        self.elapsed += 1
        if getattr(self, "bar_backup", None):
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

    def _bubble_sort(self, nums):
        nums = list(bar.num for bar in nums)
        i = 0
        while i < len(nums):
            is_exchange = False
            for j in range(len(nums) - 1, i, -1):
                if nums[j] < nums[j - 1]:
                    is_exchange = True
                    nums[j - 1], nums[j] = nums[j], nums[j - 1]
                    self.exchange_pos.append((j - 1, j))
                    i = j - 1
            if not is_exchange:
                return
            i += 1

    def exchange(self):
        self.left, self.right = self.exchange_pos[self.i]
        self.nums[self.right].position, self.nums[self.left].position = self.nums[self.left].position, self.nums[
            self.right].position
        self.nums[self.right], self.nums[self.left] = self.nums[self.left], self.nums[self.right]


class CockTailSortLayer(SortLayer):
    def __init__(self):
        super().__init__("_cock_tail_sort_sort")

    def _cock_tail_sort_sort(self, nums):
        nums = list(bar.num for bar in nums)
        for i in range(len(nums) // 2):
            for j in range(len(nums) - 1, i, -1):
                if nums[j] < nums[j - 1]:
                    nums[j - 1], nums[j] = nums[j], nums[j - 1]
                    self.exchange_pos.append((j - 1, j))
            for k in range(i + 1, len(nums) - 1):
                if nums[k] > nums[k + 1]:
                    nums[k + 1], nums[k] = nums[k], nums[k + 1]
                    self.exchange_pos.append((k + 1, k))

    def exchange(self):
        self.left, self.right = self.exchange_pos[self.i]
        self.nums[self.right].position, self.nums[self.left].position = self.nums[self.left].position, self.nums[
            self.right].position
        self.nums[self.right], self.nums[self.left] = self.nums[self.left], self.nums[self.right]


class SelectionSortLayer(SortLayer):
    def __init__(self):
        super().__init__("_selection_sort")

    def _selection_sort(self, nums):
        nums = list(bar.num for bar in nums)
        for i in range(len(nums)):
            k = i
            for j in range(i + 1, len(nums)):
                if nums[j] < nums[k]:
                    k = j
                self.exchange_pos.append((-1, j))
            self.exchange_pos.append((k, i))
            nums[k], nums[i] = nums[i], nums[k]

    def exchange(self):
        self.left, self.right = self.exchange_pos[self.i]
        if self.left != -1:
            self.nums[self.right].position, self.nums[self.left].position = self.nums[self.left].position, self.nums[
                self.right].position
            self.nums[self.right], self.nums[self.left] = self.nums[self.left], self.nums[self.right]


class InsertionSortLayer(SortLayer):
    def __init__(self):
        super().__init__("_insertion_sort")

    def _insertion_sort(self, nums):
        nums = list(bar.num for bar in nums)
        for i in range(len(nums) - 1):
            j = i + 1
            backup = nums[j]
            while j > 0 and backup < nums[j - 1]:
                self.exchange_pos.append((j, nums[j - 1]))
                nums[j] = nums[j - 1]
                j -= 1
            self.exchange_pos.append((j, backup))
            nums[j] = backup

    def exchange(self):
        self.right, self.num = self.exchange_pos[self.i]
        self.nums[self.right].scale_y = self.num / self.nums[self.right].height


class ShellSortLayer(SortLayer):
    def __init__(self):
        super().__init__("_shell_sort")

    def _insertion_sort(self, start, gap, alist):
        for i in range(start, len(alist) - gap, gap):
            j = i + gap
            backup = alist[j].num
            while j > start and backup < alist[j - gap].num:
                alist[j].num = alist[j - gap].num
                self.exchange_pos.append((j, alist[j - gap].num))
                j -= gap
            alist[j].num = backup
            self.exchange_pos.append((j, backup))

    def _shell_sort(self, nums):
        gap = len(nums)
        while gap != 0:
            gap //= 2
            for start in range(gap):
                self._insertion_sort(start, gap, self.nums)

    def exchange(self):
        self.right, self.num = self.exchange_pos[self.i]
        self.nums[self.right].scale_y = self.num / self.nums[self.right].height


class QuickSortLayer(Layer):
    def __init__(self):
        super().__init__()

        self.nums = [Bar(num=num) for num in data]
        for idx, bar in enumerate(self.nums):
            bar.position = idx * BAR_WIDTH, 0
            self.add(bar, z=1)

        self.elapsed = 1

        self.i = 0
        self.bar_backup_pivot = self.nums[0]  # 默认值
        self.bar_backup_left = self.nums[0]  # 默认值
        self.bar_backup_right = self.nums[0]  # 默认值
        self.exchange_pos = []
        self._quick_sort(0, len(self.nums) - 1, list(self.nums))

        self.schedule(self.update)

    def _quick_sort(self, start, end, alist):
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
            self._quick_sort(start, right - 1, alist)
        if right + 1 < end:
            self._quick_sort(right + 1, end, alist)

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


class MergeSortLayer(SortLayer):
    def __init__(self):
        super().__init__("_merge_sort")

        self.bar_backup = self.exchange_pos[0][0]  # 默认值

    def _merge_sort(self, alist, start=0):
        if len(alist) > 1:
            mid = len(alist) // 2
            left = alist[:mid]
            right = alist[mid:]

            self._merge_sort(left, start)
            self._merge_sort(right, start + mid)

            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    alist[k] = left[i]
                    self.exchange_pos.append((left[i], start + k))  # from_tick, to_pos
                    i += 1
                else:
                    alist[k] = right[j]
                    self.exchange_pos.append((right[j], start + k))  # from_tick, to_pos
                    j += 1
                k += 1

            while i < len(left):
                alist[k] = left[i]
                self.exchange_pos.append((left[i], start + k))  # from_tick, to_pos
                i += 1
                k += 1
            while j < len(right):
                alist[k] = right[j]
                self.exchange_pos.append((right[j], start + k))  # from_tick, to_pos
                j += 1
                k += 1
        return alist

    def update(self, dt):
        self.elapsed += 1
        self.bar_backup.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        if self.elapsed > threshold:
            self.elapsed = 1  # tick
            self.bar_backup, self.right = self.exchange_pos[self.i]
            self.bar_backup.position = BAR_WIDTH * self.right, 0
            self.i += 1
            if self.i == len(self.exchange_pos):
                self.unschedule(self.update)
            self.bar_backup.color = 255, 0, 0


class BucketSortLayer(SortLayer):
    def __init__(self):
        super().__init__("_bucket_sort")

        self.bar_backup = self.exchange_pos[0][0]  # 默认值

    def _insertion_sort(self, alist, start):  # 这里用了trick, 没有用scale_y
        for i in range(len(alist) - 1):
            j = i + 1
            backup = alist[j]
            while j > 0 and backup < alist[j - 1]:
                self.exchange_pos.append((alist[j - 1], start + j))  # from to
                alist[j] = alist[j - 1]
                j -= 1
            self.exchange_pos.append((backup, start + j))  # from to
            alist[j] = backup

    def _bucket_sort(self, alist):
        bucket_num = len(alist) // 2  # 桶的个数, 向上取整
        max_num = max(alist).num
        min_num = min(alist).num
        gap = (max_num - min_num) // bucket_num + 1  # 桶的个数, 向上取整
        ans = [[] for _ in range(bucket_num)]  # 桶的个数
        for idx, num in enumerate(alist):  # 模拟扫描
            self.exchange_pos.append((num, idx))
        for num in alist:  # 桶计
            ans[(num.num - min_num) // gap].append(num)
        start = 0
        for lst in ans:  # 入桶
            for idx, num in enumerate(lst):
                self.exchange_pos.append((num, start + idx))
            start += len(lst)

        start = 0
        for lst in ans:  # 桶排序
            self._insertion_sort(lst, start)
            start += len(lst)

    def update(self, dt):
        self.elapsed += 1
        self.bar_backup.color = 127, 127, 127  # 一个放在elapse外面, 一个放在里面, 能显示, 否则计算太快, 看不出变化
        if self.elapsed > threshold:
            self.elapsed = 1  # tick
            self.bar_backup, self.right = self.exchange_pos[self.i]
            self.bar_backup.position = BAR_WIDTH * self.right, 0
            self.i += 1
            if self.i == len(self.exchange_pos):
                self.unschedule(self.update)
            self.bar_backup.color = 255, 0, 0


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

    BAR_WIDTH = 20  # 最好被width整除
    COLUMNS = width // BAR_WIDTH

    # data range(数据范围)
    data_lowest, data_highest = 10, height - 20

    threshold = 0  # 调速用, 大于此阈值执行一次操作
    data = [randint(data_lowest, data_highest) for _ in range(COLUMNS)]  # 共用的sort数据
    # data = [num for num in range(data_lowest, data_highest, 5)][:COLUMNS]  # 共用的sort数据
    # data = [num for num in range(data_highest, data_lowest, -5)][:COLUMNS]  # 共用的sort数据

    layers = [BubbleSortLayer, InsertionSortLayer,
              SelectionSortLayer, ShellSortLayer,
              QuickSortLayer, CockTailSortLayer,
              MergeSortLayer, BucketSortLayer,
              HeapSortLayer]
    # layers = [BucketSortLayer]
    # layers = [BubbleSortLayer, CockTailSortLayer]
    LAYER_NUMS = len(layers)
    edge_grid_num = ceil(LAYER_NUMS ** 0.5)
    width, height = width / edge_grid_num, height / edge_grid_num

    director.run(SortScene())
