import random
import time
import math
from random import randrange


def bubble_sort(my_list):
    # do n passes on the list
    swapped = True
    while swapped:
        swapped = False

        # check neighbours and swap them if needed
        for j in range(len(my_list) - 1):
            if my_list[j] > my_list[j + 1]:
                temp = my_list[j]
                my_list[j] = my_list[j + 1]
                my_list[j + 1] = temp
                swapped = True


def selection_sort(my_list):
    for i in range(len(my_list) - 1):  # perform n-1 passes

        # find the minimum in the unsorted part of my_list
        min_index = i
        for j in range(i + 1, len(my_list)):
            if my_list[j] < my_list[min_index]:
                min_index = j

        # swap this min element with the first unsorted element from my_list 
        temp = my_list[i]
        my_list[i] = my_list[min_index]
        my_list[min_index] = temp


def insertion_sort(my_list):
    i = 1  # i is the size of the sorted list
    while i < len(my_list):  # while the list is not sorted yet
        j = i

        # place the element j at the proper place in the sorted list
        while j > 0 and my_list[j - 1] > my_list[j]:
            # swap
            temp = my_list[j]
            my_list[j] = my_list[j - 1]
            my_list[j - 1] = temp
            j = j - 1

        i = i + 1


def merge_sort(my_list):
    # if the list is empty or contains just one element, no need to sort 
    if len(my_list) <= 1: return my_list

    # we divide the work in two halves, and sort them recursively
    mid = int(len(my_list) / 2)
    left = merge_sort(my_list[:mid])
    right = merge_sort(my_list[mid:])

    # merge the two sorted halves, while keeping the list sorted
    my_sorted_list = []
    while left != [] or right != []:
        if left == []:
            my_sorted_list.append(right.pop(0))  # left is empty
        elif right == []:
            my_sorted_list.append(left.pop(0))  # right is empty
        elif left[0] < right[0]:
            my_sorted_list.append(left.pop(0))
        else:
            my_sorted_list.append(right.pop(0))

    return my_sorted_list


# function to swap the element in a heap or list
def swap(heap, parent_index, child_index):
    parent = heap[parent_index]
    child = heap[child_index]
    heap[parent_index] = child
    heap[child_index] = parent


# function to generate a random pivot
def random_pivot(my_list, low_index, high_index):
    rand_pivot = random.randrange(low_index, high_index + 1)
    swap(my_list, high_index, rand_pivot)
    return partition(my_list, low_index, high_index)


# function to find the partition position
def partition(my_list, low_index, high_index):
    smaller = low_index - 1

    # always use the higher index of element to be the pivot
    # As we have already swapped the random pivot with the last element
    pivot = my_list[high_index]

    # loop through all elements in the list, and compare with the pivot
    for i in range(low_index, high_index):

        # if the current element is less than or equal to the pivot, then put this element to the left of the pivot
        if my_list[i] <= pivot:
            smaller += 1

            # swap
            swap(my_list, i, smaller)

    # swap the pivot
    pivot = smaller + 1
    swap(my_list, pivot, high_index)

    return pivot


def quick_sort_helper(my_list, low_index, high_index):
    # base case
    if len(my_list) == 1:
        return my_list

    # recursion to divide the list
    if low_index < high_index:
        partition_index = random_pivot(my_list, low_index, high_index)

        # sort the left part
        quick_sort_helper(my_list, low_index, partition_index - 1)

        # sort the right part
        quick_sort_helper(my_list, partition_index + 1, high_index)


def quick_sort(my_list):
    return quick_sort_helper(my_list, 0, len(my_list) - 1)


# Q2
# if we want to sort a sorted or almost sorted list by using quick sort with the lowest or highest index as the pivot
# then we will have the worst case for quick sort, which will take O(n**2) time complexity.
# If we want to solve this problem, we can randomly choose the pivot, I have implemented the random_pivot function
# which can randomly generate a pivot


def add_to_heap(heap, element):
    # add the element at the end of the heap
    heap.append(element)
    child_index = len(heap) - 1

    # create a new heap is there is no element in the heap
    if child_index == 0:
        return heap

    # otherwise, compare the element with its parents
    while True:
        parent_index = math.ceil(child_index / 2) - 1
        if parent_index < 0:
            break
        else:
            if heap[parent_index] > heap[child_index]:
                swap(heap, parent_index, child_index)
                child_index = parent_index
            else:
                break
    return heap


def remove_min_from_heap(heap):
    leaf_element = heap[len(heap) - 1]
    new_heap = [leaf_element]

    # if the heap has only one element, then return the empty list after remove the min element
    if len(heap) == 1:
        return []
    # rearrange the heap
    for i in range(1, len(heap) - 1):
        new_heap.append(heap[i])

    # loop through the whole heap to see if the position of all elements are appropriate
    parent_index = 0
    while True:
        left_child_index = 2 * parent_index + 1
        right_child_index = 2 * parent_index + 2
        if left_child_index < len(new_heap):
            if right_child_index < len(new_heap):
                if new_heap[left_child_index] < new_heap[right_child_index]:
                    if new_heap[parent_index] > new_heap[left_child_index]:
                        swap(new_heap, parent_index, left_child_index)
                        parent_index = left_child_index
                    else:
                        break
                else:
                    if new_heap[parent_index] > new_heap[right_child_index]:
                        swap(new_heap, parent_index, right_child_index)
                        parent_index = right_child_index
                    else:
                        break
            else:
                if new_heap[parent_index] > new_heap[left_child_index]:
                    swap(new_heap, parent_index, left_child_index)
                    parent_index = left_child_index
                else:
                    break
        else:
            break

    return new_heap


# function to build a heap from an input of list
def build_heap(lst):
    heap = []
    for i in range(len(lst)):
        heap = add_to_heap(heap, lst[i])
    return heap


# function for heap sort algorithm
def heap_sort(my_list):
    # convert the list into a heap type
    heap = build_heap(my_list)
    sorted_list = []

    # select the root of the heap each time, then we will get a sorted list
    while True:
        if len(heap) > 0:
            sorted_list.append(heap[0])
            heap = remove_min_from_heap(heap)
        else:
            break

    return sorted_list


def test_sorting(algo, my_tab, display):
    tab = my_tab.copy()
    print("testing", algo, str(" " * (14 - len(algo))), "... ", end='')
    t = time.time()
    temp = eval(algo + "(tab)")
    if temp != None: tab = temp
    print("done ! It took {:.2f} seconds".format(time.time() - t))
    if display: print(tab, end='\n\n')


print("\n ******** Testing to sort a small table of 30 elements ********")
NUMBER_OF_ELEMENTS = 30
tab = [random.randint(1, 40) for i in range(NUMBER_OF_ELEMENTS)]
# tab = list(set([random.randint(1, 40) for i in range(NUMBER_OF_ELEMENTS)]))
print("Original table: ")
print(tab, end='\n\n')
test_sorting("bubble_sort", tab, True)
test_sorting("selection_sort", tab, True)
test_sorting("insertion_sort", tab, True)
test_sorting("merge_sort", tab, True)
test_sorting("quick_sort", tab, True)
test_sorting("heap_sort", tab, True)

print("\n ******** Testing to sort a big table of 5000 elements ********")
NUMBER_OF_ELEMENTS = 5000
tab = list(set([random.random() for i in range(NUMBER_OF_ELEMENTS)]))
test_sorting("bubble_sort", tab, False)
test_sorting("selection_sort", tab, False)
test_sorting("insertion_sort", tab, False)
test_sorting("merge_sort", tab, False)
test_sorting("quick_sort", tab, False)
test_sorting("heap_sort", tab, False)

# Algorithms are fun!
