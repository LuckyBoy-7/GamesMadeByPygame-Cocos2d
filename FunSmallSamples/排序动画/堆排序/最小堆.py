from random import randint


class Heap(object):
    def __init__(self):
        self.heap_list = [-1]
        self.current_size = 0

    def perc_up(self, i):
        while i // 2 > 0:
            left = i // 2
            if self.heap_list[left] > self.heap_list[i]:
                self.heap_list[left], self.heap_list[i] = self.heap_list[i], self.heap_list[left]
            i //= 2

    def insert(self, val):
        self.heap_list.append(val)
        self.current_size += 1
        self.perc_up(self.current_size)

    def perc_down(self, i):
        while i * 2 <= self.current_size:
            mc = self.get_min_child(i)
            if self.heap_list[i] > self.heap_list[mc]:
                self.heap_list[i], self.heap_list[mc] = self.heap_list[mc], self.heap_list[i]
            i = mc

    def get_min_child(self, i):
        left = i * 2
        right = i * 2 + 1
        if right > self.current_size:
            return left
        else:
            if self.heap_list[left] > self.heap_list[right]:
                return right
            return left

    def del_min(self):
        retval = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.current_size -= 1
        self.heap_list.pop()
        self.perc_down(1)

        return retval

    def __repr__(self):
        return str(self.heap_list)


heap = Heap()
for num in [randint(1, 100) for num in range(10)]:
    heap.insert(num)
print(heap)
for i in range(heap.current_size):
    print(heap.del_min())
