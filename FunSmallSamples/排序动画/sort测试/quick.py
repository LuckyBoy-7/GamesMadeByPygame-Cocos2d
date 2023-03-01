from random import randint


alist = [randint(1, 50) for _ in range(20)]


exchange = []
def quick_sort(start, end, alist):
    pivot = start
    left = pivot + 1
    right = end

    while True:
        while left <= right and alist[left] <= alist[pivot]:
            left += 1
            exchange.append((-1, -1, left, -1, pivot))
        while left <= right and alist[right] >= alist[pivot]:
            right -= 1
            exchange.append((-1, -1, -1, right, pivot))  # 左交换, 右交换, 左基准, 右基准, 当前基准
        if left < right:
            alist[left], alist[right] = alist[right], alist[left]
            exchange.append((left, right, -1, right, pivot))
        else:
            alist[pivot], alist[right] = alist[right], alist[pivot]
            break

    if start < right - 1:
        quick_sort(start, right - 1, alist)
    if right + 1 < end:
        quick_sort(right + 1, end, alist)

quick_sort(0, len(alist) - 1, alist)
print(alist)
print(exchange)
