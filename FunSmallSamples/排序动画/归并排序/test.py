from random import randint


alist = [randint(1, 50) for _ in range(20)]

print(sorted(alist))
exchange = []
# def merge_sort(alist):
#     if len(alist) > 1:
#         mid = len(alist) // 2
#         left = alist[:mid]
#         right = alist[mid:]
#
#         merge_sort(left)
#         merge_sort(right)
#
#         i = j = k = 0
#         while i < len(left) and j < len(right):
#             if left[i] < right[j]:
#                 alist[k] = left[i]
#                 i += 1
#             else:
#                 alist[k] = right[j]
#                 j += 1
#             k += 1
#
#         while i < len(left):
#             alist[k] = left[i]
#             i += 1
#             k += 1
#         while j < len(left):
#             alist[k] = right[j]
#             j += 1
#             k += 1
#     return alist

def merge_sort(alist, start=0):
    if len(alist) > 1:
        mid = len(alist) // 2
        left = alist[:mid]
        right = alist[mid:]

        merge_sort(left, 0)
        merge_sort(right, mid)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                alist[k] = left[i]
                exchange.append((i, start + k))  # from_tick, to
                i += 1
            else:
                alist[k] = right[j]
                exchange.append((j, start + k))  # from_tick, to
                j += 1
            k += 1

        while i < len(left):
            alist[k] = left[i]
            exchange.append((i, start + k))  # from_tick, to
            i += 1
            k += 1
        while j < len(right):
            alist[k] = right[j]
            j += 1
            exchange.append((j, start + k))  # from_tick, to
            k += 1
    return alist
print(merge_sort(alist))
# print(exchange)







