# All notations in this module are taken from Introduction to Algorithms 3rd ed by CLRS

from math import floor


def left(i):
    return 2 * i


def right(i):
    return 2 * i + 1


def parent(i):
    return floor(i / 2)


def identity_function(x):
    return x


def max_heapify(a, i, heap_size, score_function=identity_function):
    left_child = left(i)
    right_child = right(i)

    largest = 0

    if left_child <= heap_size and score_function(a[left_child]) > score_function(a[i]):
        largest = left_child
    else:
        largest = i

    if right_child <= heap_size and score_function(a[right_child]) > score_function(a[largest]):
        largest = right_child

    if largest != i:
        temp = a[i]
        a[i] = a[largest]
        a[largest] = temp

        max_heapify(a, largest, heap_size,score_function)


def build_max_heap(a, score_function=identity_function):
    for i in reversed(range(floor(len(a) / 2))):
        max_heapify(a, i, len(a) - 1, score_function)


def pick_max(heap_array, score_function=identity_function, zero_value=0):
    result = heap_array[0]
    heap_array[0] = zero_value
    max_heapify(heap_array, 0, len(heap_array) - 1, score_function)
    return result
