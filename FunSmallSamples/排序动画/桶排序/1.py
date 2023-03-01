from random import randint

alist = [randint(1, 50) for _ in range(20)]

print(sorted(alist))
exchange = []


# def insertion_sort(alist):
#     for i in range(len(alist) - 1):
#         j = i + 1
#         backup = alist[j]
#         while j > 0 and backup < alist[j - 1]:
#             alist[j] = alist[j - 1]
#             j -= 1
#         alist[j] = backup
#
#
# def bucket_sort(alist):
#     bucket_num = 3
#     max_num = max(alist)
#     min_num = min(alist)
#     gap = (max_num - min_num) // bucket_num + 1  # 桶的个数, 向上取整
#     ans = [[] for _ in range(bucket_num)]  # 桶的个数
#     for num in alist:
#         ans[(num - min_num) // gap].append(num)
#
#     for lst in ans:
#         insertion_sort(lst)
#
# print(bucket_sort(alist))
def insertion_sort(alist, start):
    for i in range(len(alist) - 1):
        j = i + 1
        backup = alist[j]
        while j > 0 and backup < alist[j - 1]:
            exchange.append((alist[j - 1], start + j))  # from to
            alist[j] = alist[j - 1]
            j -= 1
        alist[j] = backup


def bucket_sort(alist):
    bucket_num = 3
    max_num = max(alist)
    min_num = min(alist)
    gap = (max_num - min_num) // bucket_num + 1  # 桶的个数, 向上取整
    ans = [[] for _ in range(bucket_num)]  # 桶的个数
    for num in alist:
        ans[(num - min_num) // gap].append(num)

    start = 0
    for lst in ans:
        insertion_sort(lst, start)
        start += len(lst)

print(bucket_sort(alist))