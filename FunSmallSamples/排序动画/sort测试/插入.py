from random import randint


alist = [randint(1, 50) for _ in range(20)]


# def insertion_sort(alist):
#     for i in range(len(alist) - 1):
#         j = i + 1
#         backup = alist[j]
#         while j > 0 and backup < alist[j - 1]:
#             alist[j] = alist[j - 1]
#             j -= 1
#         alist[j] = backup


# def insertion_sort(alist):
#     i = 0
#     while i < len(alist) - 1:
#         j = i + 1
#         backup = alist[j]
#         while j > 0 and backup < alist[j - 1]:
#             alist[j] = alist[j - 1]
#             j -= 1
#         alist[j] = backup
#         i += 1



# def insertion_sort(alist):
#     i = 0
#     while i < len(alist) - 1:
#         j = i + 1
#         backup = alist[j]
#         while True:
#             if j > 0 and backup < alist[j - 1]:
#                 alist[j] = alist[j - 1]
#                 j -= 1
#             else:
#                 alist[j] = backup
#                 i += 1
#                 break

# def insertion_sort(alist):
#     i = 0
#     while True:
#         if i < len(alist) - 1:
#             j = i + 1
#             backup = alist[j]
#             while True:
#                 if j > 0 and backup < alist[j - 1]:
#                     alist[j] = alist[j - 1]
#                     j -= 1
#                 else:
#                     alist[j] = backup
#                     i += 1
#                     break
#         else:
#             break

def insertion_sort(alist):
    i = 0
    j = i + 1
    backup = alist[j]
    while True:
        if i < len(alist) - 1:
            if j > 0 and backup < alist[j - 1]:
                alist[j] = alist[j - 1]
                j -= 1
            else:
                alist[j] = backup
                i += 1
                if i == len(alist) - 1:
                    break
                j = i + 1
                backup = alist[j]

        else:
            break




insertion_sort(alist)
print(alist)
