from random import randint


exchange_pos = []


def insertion_sort(start, gap, alist):
    for i in range(start, len(alist) - gap, gap):
        j = i + gap
        backup = alist[j]
        while j > start and backup < alist[j - gap]:
            alist[j] = alist[j - gap]
            exchange_pos.append((j - gap, j))
            j -= gap
        alist[j] = backup
        exchange_pos.append((-1, j))


def shell_sort(alist):
    gap = len(alist)
    while gap != 0:
        gap //= 2
        for start in range(gap):
            insertion_sort(start, gap, alist)

for _ in range(10):
    alist = [randint(1, 50) for _ in range(10)]
    shell_sort(alist)
    if alist != sorted(alist):
        print(alist)


print(exchange_pos)


for _ in range(10):
    alist = [randint(1, 50) for _ in range(10)]
    shell_sort(alist)
    if alist != sorted(alist):
        print(alist)