import matplotlib.pyplot as plt
import time
import random


# Q1
# function that checks if three points a,b,c are clockwise positioned
def is_clockwise(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) < (b[1] - a[1]) * (c[0] - a[0])


# Q2
# helper function to shift left of a list, counterclockwise direction
def left_shift(p, pts):
    return (p + 1) % len(pts)


# helper function to shift right of a list, clockwise direction
def right_shift(p, pts):
    return (p + len(pts) - 1) % len(pts)


# compute with naive method the convex hull of the points cloud pts
# and store it as a list of vectors
def convex_hull_2d_gift_wrapping(pts):
    """
    Time complexity for this algo is O(nh) for average case. O(n**2) for worse case
    As each loop starts with the convex point which found in last loop, O(h) for outer loop and for each convex
    point loop, we need to loop the whole pts list again to find the next convex point, which takes O(n) for each loop.
    Therefore, in total O(nh) for average time.
    :param pts: a list of points which can form a diagram
    :return: convex point for the diagram
    """
    # As the array pts was sorted, the first one should be the leftmost one
    leftmost_index = 0
    p = leftmost_index

    # record the convex points and number of convex points
    # leftmost point is guaranteed to be part of convex hull
    convex_hull_list = [pts[p]]
    m = 1

    # start searching for the other convex points
    while True:
        next_p = left_shift(p, pts)

        # if the combination of leftmost point and the anchor point with every other points is clockwise
        # then the anchor point is a convex point
        for h in range(len(pts)):
            if is_clockwise(convex_hull_list[m - 1], pts[h], pts[next_p]):
                next_p = h

        # endpoint p can be added to the convex hull list during the next round
        p = next_p

        # record the convex point and update the number of convex points
        convex_hull_list.append(pts[p])
        m += 1

        # stop searching the convex point, if we loop back to the start point
        if p == leftmost_index:
            break

    return convex_hull_list[:-1]


# Q3
# helper function to push up the connection line between leftmost and rightmost
def pushup(left_convex_hull, upper_r, right_convex_hull, upper_l):
    while True:
        # set a boolean checker to indicate whether we have found the appropriate connection point for left part
        l_checker = False
        next_r = left_shift(upper_r, left_convex_hull)
        while is_clockwise(right_convex_hull[upper_l], left_convex_hull[upper_r], left_convex_hull[next_r]):
            upper_r = next_r
            next_r = left_shift(upper_r, left_convex_hull)
            l_checker = True

        # set a boolean checker to indicate whether we have found the appropriate connection point for right part
        r_checker = False
        next_l = right_shift(upper_l, right_convex_hull)
        while not is_clockwise(left_convex_hull[upper_r], right_convex_hull[upper_l], right_convex_hull[next_l]):
            upper_l = next_l
            next_l = right_shift(upper_l, right_convex_hull)
            r_checker = True

        # stop looping when we found the highest appropriate connection point
        if not l_checker and not r_checker:
            return upper_r, upper_l


# helper function to push down the connection line between leftmost and rightmost
def pushdown(left_convex_hull, lower_r, right_convex_hull, lower_l):
    while True:
        # set a boolean checker to indicate whether we have found the appropriate connection point for left part
        l_checker = False
        next_r = right_shift(lower_r, left_convex_hull)
        while not is_clockwise(right_convex_hull[lower_l], left_convex_hull[lower_r], left_convex_hull[next_r]):
            lower_r = next_r
            next_r = right_shift(lower_r, left_convex_hull)
            l_checker = True

        # set a boolean checker to indicate whether we have found the appropriate connection point for right part
        r_checker = False
        next_l = left_shift(lower_l, right_convex_hull)
        while is_clockwise(left_convex_hull[lower_r], right_convex_hull[lower_l], right_convex_hull[next_l]):
            lower_l = next_l
            next_l = left_shift(lower_l, right_convex_hull)
            r_checker = True

        # stop looping when we found the lowest appropriate connection point
        if not l_checker and not r_checker:
            return lower_r, lower_l


# merge function for divide and conquer algorithm
# connect 2 hulls together and adjust the connection points
def merge(left_convex_hull, right_convex_hull):

    # find the rightmost point of the left part
    left_rightmost = 0
    for i in range(1, len(left_convex_hull)):
        if left_convex_hull[i][0] > left_convex_hull[left_rightmost][0]:
            left_rightmost = i

    # find the leftmost point of the right part
    right_leftmost = 0

    # connect two part together by connecting the convex point of each side
    #     # variable declaration: upper_r is upper connection point from right part
    #     # upper_l is upper connection point from left part
    #     # lower_r is lower connection point from right part
    #     # lower_l is lower connection point from left part
    (upper_r, upper_l) = pushup(left_convex_hull, left_rightmost, right_convex_hull, right_leftmost)
    (lower_r, lower_l) = pushdown(left_convex_hull, left_rightmost, right_convex_hull, right_leftmost)

    # merge the 2 hulls from the connection points
    convex_hull_list = []
    for i in range(lower_r + 1):
        convex_hull_list.append(left_convex_hull[i])
    if upper_l > 0:
        for i in range(lower_l, upper_l + 1):
            convex_hull_list.append(right_convex_hull[i])
    else:
        for i in range(lower_l, len(right_convex_hull)):
            convex_hull_list.append(right_convex_hull[i])

        # avoid error for edge case
        if lower_l != 0:
            convex_hull_list.append(right_convex_hull[0])
    if upper_r > 0:
        for i in range(upper_r, len(left_convex_hull)):
            convex_hull_list.append(left_convex_hull[i])

    return convex_hull_list


# As we directly used index to divide the diagram,
# we need to set the anchor point as the starting point of the divided pts list
def q3_gift_wrapping_helper(pts, start, end):
    # base case
    if start == end:
        return []

    leftmost = start
    convex_hull = []
    p = leftmost
    m = 1
    convex_hull.append(pts[p])

    while True:

        # initial next point for a candidate edge on the hull
        # all other processes are similar with the previous Q2 version.
        next_p = start

        for i in range(start, end):
            if p == next_p or is_clockwise(convex_hull[m - 1], pts[next_p], pts[i]):
                next_p = i
        p = next_p
        convex_hull.append(pts[p])
        m += 1

        if next_p == leftmost:
            break
    return convex_hull[:-1]


# function to divide the whole hull
def convex_hull_2d_divide_conquer_index_divide(pts, start, end):
    # base case: when the length of the array is divided to 4 or less element,
    # use gift wrapping algorithm to find the convex point
    if end - start < 5:
        return q3_gift_wrapping_helper(pts, start, end)

    mid = (1 + start + end) // 2

    # start dividing the pts list
    left_convex_hull = convex_hull_2d_divide_conquer_index_divide(pts, start, mid)
    right_convex_hull = convex_hull_2d_divide_conquer_index_divide(pts, mid, end)

    return merge(left_convex_hull, right_convex_hull)


# compute with divide and conquer method the convex hull of the points
# cloud pts and store it as a list of vectors
def convex_hull_2d_divide_conquer(pts):
    """
    The time complexity of this algo is O(nlogn) for average case, O(n**2) for worse case. The merging step takes O(n),
    and because we divided the pts list in two part, so the total complexity, which takes O(logn) for each loop to find
    the convex points. Therefore, in total O(nlogn) for average case to find the convex point.
    :param pts: a list of point which form a diagram
    :return: a list of convex point for this diagram
    """
    # return in counterclockwise order, starts from the leftmost point
    # use index to divide the points array for time saving purpose instead of copy the array
    return convex_hull_2d_divide_conquer_index_divide(pts, 0, len(pts))


NUMBER_OF_POINTS = 1000000

# generate random points and sort them according to x coordinate
ptss = []
for y in range(NUMBER_OF_POINTS): ptss.append([random.random(), random.random()])
ptss = sorted(ptss, key=lambda x: x[0])

# compute the convex hulls
print("Computing convex hull using gift wrapping technique ... ", end="")
t = time.time()
hull_gift_wrapping = convex_hull_2d_gift_wrapping(ptss)
print("done ! It took ", time.time() - t, " seconds")

print("Computing convex hull using divide and conquer technique ... ", end="")
t = time.time()
hull_divide_conquer = convex_hull_2d_divide_conquer(ptss)
print("done ! It took ", time.time() - t, " seconds")

# close the convex hull for display
hull_gift_wrapping.append(hull_gift_wrapping[0])
hull_divide_conquer.append(hull_divide_conquer[0])

# display the convex hulls
if NUMBER_OF_POINTS <= 1000000:
    fig = plt.figure()
    ax = fig.add_subplot(131)
    ax.plot([x[0] for x in ptss], [x[1] for x in ptss], "ko")
    ax.title.set_text('Points')
    ax = fig.add_subplot(132)
    ax.plot([x[0] for x in ptss], [x[1] for x in ptss], "ko")
    ax.plot([x[0] for x in hull_gift_wrapping], [x[1] for x in hull_gift_wrapping], "ro--")
    ax.title.set_text('Gift Wrapping')
    ax = fig.add_subplot(133)
    ax.plot([x[0] for x in ptss], [x[1] for x in ptss], "ko")
    ax.plot([x[0] for x in hull_divide_conquer], [x[1] for x in hull_divide_conquer], "ro--")
    ax.title.set_text('Divide/Conquer')
    plt.show(block=True)

# Algorithms are fun!
