import matplotlib.pyplot as plt
import time
import random


# import pylab


def orientation(p, q, r):
    '''
    To find orientation of ordered triplet (p, q, r).
    The function returns following values
    0 --> p, q and r are collinear
    1 --> Clockwise
    2 --> Counterclockwise
    '''
    val = (q[1] - p[1]) * (r[0] - q[0]) - \
          (q[0] - p[0]) * (r[1] - q[1])

    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


# function that checks if three points a,b,c are clockwise positioned
# def is_clockwise(a, b, c):
#     a_x = a[0]
#     a_y = a[1]
#     b_x = b[0]
#     b_y = b[1]
#     c_x = c[0]
#     c_y = c[1]
#     operation_lhs = (c_y - a_y) * (b_x - a_x)
#     operation_rhs = (b_y - a_y) * (c_x - a_x)
#     if operation_lhs < operation_rhs:
#         return True
#     return False

def is_clockwise(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) < (b[1] - a[1]) * (c[0] - a[0])


# print(is_clockwise((0, 1), (4, 5), (6, 3)))


# compute with naive method the convex hull of the points cloud pts
# and store it as a list of vectors
def convex_hull_2d_gift_wrapping(pts):
    leftmost_index = 0
    convex_hull_list = []
    # pts_copy = pts.copy()
    # find the left most point among pts
    # for j in range(1, len(pts)):
    #     if pts[j][0] < pts[leftmost_index][0]:
    #         leftmost_index = j
    #     elif pts[j][0] == pts[leftmost_index][0]:
    #         if pts[j][1] > pts[leftmost_index][1]:
    #             leftmost_index = j

    # print("left most: ", leftmost_index)
    # record the left most point into the convex hull list
    # convex_hull.append(pts[leftmost_index])

    # pts_copy.pop(leftmost_index)
    p = leftmost_index
    convex_hull_list.append(pts[p])
    m = 1
    while True:
        if p == len(pts) - 1:
            next_p = 0
        else:
            next_p = p + 1
        # next_p = p
        # for q in range(len(pts)):
        # if p + 1 < len(pts):
        #     next_p = p + 1
        # else:
        #     next_p = p

        for h in range(len(pts)):
            # if orientation(pts[p], pts[h], pts[q]) == 2:
            if is_clockwise(convex_hull_list[m-1], pts[h], pts[next_p]):
                next_p = h
        p = next_p
        convex_hull_list.append(pts[p])
        m+=1

        if p == leftmost_index:
            break
    # for q in range(len(pts)):
    #     convex_hull_list.append(pts[p])
    #     # q = (p + 1) % len(pts)
    #     # for q in range(len(pts)):
    #     if p == q:
    #         continue
    #     for h in range(len(pts)):
    #         # if orientation(pts[p], pts[h], pts[q]) == 2:
    #         if is_clockwise(pts[p], pts[h], pts[q]):
    #             p = h
    #
    #     if p == leftmost_index:
    #         break

    return convex_hull_list[:-1]


# def convex_hull_q2(pts):
#     leftmost_index = 0
#     convex_hull_list = []
#     ptss = sorted(pts)
#     # pts_copy = pts.copy()
#     # find the left most point among pts
#     for j in range(1, len(ptss)):
#         if ptss[j][0] < ptss[leftmost_index][0]:
#             leftmost_index = j
#         elif ptss[j][0] == ptss[leftmost_index][0]:
#             if ptss[j][1] > ptss[leftmost_index][1]:
#                 leftmost_index = j
#
#     y = 0
#     while True:
#         convex_hull_list.append(ptss[leftmost_index])
#         endpoint = 0
#         for h in range(1, len(ptss)):
#             if (endpoint == leftmost_index) or (not is_clockwise(ptss[leftmost_index], ptss[h], convex_hull_list[y])):
#                 endpoint = h
#         y += 1
#         leftmost_index = endpoint
#
#         if endpoint == convex_hull_list[0]:
#             break
#     return convex_hull_list

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull_q2(pts):
    leftmost_index = 0
    convex_hull_list = []
    # pts_copy = pts.copy()
    # find the left most point among pts
    for j in range(1, len(pts)):
        if pts[j][0] < pts[leftmost_index][0]:
            leftmost_index = j
        elif pts[j][0] == pts[leftmost_index][0]:
            if pts[j][1] > pts[leftmost_index][1]:
                leftmost_index = j

    p = leftmost_index
    convex_hull_list.append(pts[p])
    m = 1
    while True:
        j = 0
        # next_p = (p + 1) % len(pts)
        # next_p = p
        # for q in range(len(pts)):
        # if p + 1 < len(pts):
        #     next_p = p + 1
        # else:
        #     next_p = p
        for h in range(1, len(pts)):
            if pts[h] == pts[p] or pts[h] == pts[j]:
                continue
            if pts[j] == pts[p]:
                j += 1
            # if orientation(pts[p], pts[h], pts[q]) == 2:
            if is_clockwise(convex_hull_list[m - 1], pts[h], pts[j]):
                # if is_clockwise(pts[p], pts[h], pts[j]):
                j = h
        p = j
        convex_hull_list.append(pts[p])
        m += 1

        if j == leftmost_index:
            break

    return convex_hull_list[:-1]


def convex_hull(points):
    """Computes the convex hull of a set of 2D points.

    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(points)

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 3:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    # lower_half = points[0: len(points) % 2]
    for p in points:
        # while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
        while len(lower) >= 2 and is_clockwise(p, lower[-2], lower[-1]):
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    # upper_half = points[len(points) % 2:len(points)]
    for p in reversed(points):
        # while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
        while len(upper) >= 2 and is_clockwise(upper[-2], upper[-1], p):
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list.
    return lower[:-1] + upper[:-1]


# print(convex_hull_2d_gift_wrapping([[0, 1], [6, 3], [10, 2], [4, 5]]))
# print("---")
# print(convex_hull([[0, 1], [6, 3], [10, 2], [4, 5]]))
# print(convex_hull_q2([[0, 1], [6, 3], [10, 2], [4, 5]]))


# compute with divide and conquer method the convex hull of the points
# cloud pts and store it as a list of vectors
def convex_hull_2d_divide_conquer(pts):
    return [pts[0]]


def convex_hull_dc(pts):
    if len(pts) == 4:
        return convex_hull_2d_gift_wrapping(pts)

    left_half = convex_hull_dc(pts[0: len(pts) / 2])
    right_half = convex_hull_dc(pts[len(pts) / 2:])
    return merge(left_half, right_half)

def merge(left_half, right_half):
    leftmost_index = 0
    rightmost_index = 0
    for j in range(1, len(pts)):
        if pts[j][0] < pts[leftmost_index][0]:
            leftmost_index = j
        elif pts[j][0] == pts[leftmost_index][0]:
            if pts[j][1] > pts[leftmost_index][1]:
                leftmost_index = j
    for j in range(1, len(pts)):
        if pts[j][0] > pts[rightmost_index][0]:
            rightmost_index = j
        elif pts[j][0] == pts[rightmost_index][0]:
            if pts[j][1] > pts[rightmost_index][1]:
                rightmost_index = j

    l_copy = leftmost_index.copy()
    r_copy = rightmost_index.copy()
    l = leftmost_index
    r = rightmost_index

    while True:
        orig_left = leftmost_index
        orig_right = rightmost_index
        if l == len(pts) - 1:
            next_l = 0
        else:
            next_l = l + 1

        if r == len(pts) - 1:
            next_r = 0
        else:
            next_r = r - 1

        for h in range(len(pts)):
            if is_clockwise(pts[l], pts[h], pts[next_l]):
                next_l = h
            if not is_clockwise(pts[r], pts[h], pts[next_r]):
                next_r = h
        r = next_r
        l = next_l


        #
        # while is_clockwise(pts[rightmost_index], pts[leftmost_index], pts[next_l]):
        #     leftmost_index = next_l
        # while is_clockwise(pts[leftmost_index], pts[rightmost_index], pts[next_r]):
        #     rightmost_index = next_r

        if r == orig_right and l == orig_left:
            break

    while True:
        orig_left = leftmost_index
        orig_right = rightmost_index
        if l_copy == len(pts) - 1:
            next_l_copy = 0
        else:
            next_l_copy = l_copy + 1

        if r_copy == len(pts) - 1:
            next_r_copy = 0
        else:
            next_r_copy = r_copy - 1

        for h in range(len(pts)):
            if not is_clockwise(pts[l_copy], pts[h], pts[next_l_copy]):
                next_l_copy = h
            if is_clockwise(pts[r_copy], pts[h], pts[next_r_copy]):
                next_r_copy = h
        r_copy = next_r_copy
        l_copy = next_l_copy

        #
        # while is_clockwise(pts[rightmost_index], pts[leftmost_index], pts[next_l]):
        #     leftmost_index = next_l
        # while is_clockwise(pts[leftmost_index], pts[rightmost_index], pts[next_r]):
        #     rightmost_index = next_r

        if r_copy == orig_right and l_copy == orig_left:
            break

    next_r = leftmost_index
    next_l = rightmost_index

    next_r_copy = l_copy
    next_l_copy = r_copy

    result = []
    start = rightmost_index
    while True:
        result.append(pts[rightmost_index])
        rightmost_index = next_l
        if start == rightmost_index:
            break
    return result





def c_convex_hull_2d_gift_wrapping(pts):
    # find the leftmost point as the initial starting point
    l = 0
    for i in range(1, len(pts)):
        if pts[i][0] < pts[l][0]:
            l = i
    # store the leftmost starting point
    lm = pts[l]
    # create a list to store the index of points that form the conven hull
    lst = []
    lst.append(l)
    # print(lst)

    # find the next starting point which form clockwise circle with any other point and the current starting poitn
    while (True):
        p = 0
        for i in range(1, len(pts)):
            # print("now"+str(pts[i]))
            if pts[i] == pts[l] or pts[i] == pts[p]:
                continue
            if pts[p] == pts[l]:
                p += 1
                # if the starting point, any other point i and current point p form a clockwise circle
            # then the point i will be the next upper point selected
            # print('compare')
            # print("l"+str(pts[l]))
            # print("i"+str(pts[i]))
            # print("p"+str(pts[p]))
            if (is_clockwise(pts[l], pts[i], pts[p])):
                p = i
                # print("update p"+str(pts[i]))

        # break the loop once the next point is the same as the initial leftmost starting point
        # which means the convex hull is formed
        if pts[p] == lm:
            # print('break')
            break

            # otherwise, update the starting point to p and keep finding the next most clockwise point
        l = p
        # print("update l starting"+str(pts[l]))
        lst.append(l)
        # print(lst)

    return [pts[i] for i in lst]


def cc_convex_hull_2d_gift_wrapping(pts):
    # find the leftmost point as the initial starting point
    l = 0
    for i in range(1, len(pts)):
        if pts[i][0] < pts[l][0]:
            l = i
    # store the leftmost starting point
    lm = pts[l]
    # create a list to store the index of points that form the conven hull
    lst = []
    lst.append(lm)
    # print(lst)

    # find the next starting point which form clockwise circle with any other point and the current starting poitn
    while (True):
        # choose a point as the
        if l == len(pts) - 1:
            p = 0
        else:
            p = l + 1
        for i in range(len(pts)):
            # print("now"+str(pts[i]))
            if i == l or i == p:
                continue
            # if the starting point, any other point i and current point p form a clockwise circle
            # then the point i will be the next upper point selected
            # print('compare')
            # print("l"+str(pts[l]))
            # print("i"+str(pts[i]))
            # print("p"+str(pts[p]))
            if (is_clockwise(pts[l], pts[i], pts[p])):
                p = i
                # print("update p"+str(pts[i]))

        # break the loop once the next point is the same as the initial leftmost starting point
        # which means the convex hull is formed
        if pts[p] == lm:
            # print('break')
            break

        # otherwise, update the starting point to p and keep finding the next most clockwise point
        l = p
        # print("update l starting"+str(pts[l]))
        lst.append(pts[l])
        # print(lst)

    return lst


NUMBER_OF_POINTS = 1000000

# generate random points and sort them accoridng to x coordinate
pts = []
for i in range(NUMBER_OF_POINTS): pts.append([random.random(), random.random()])
pts = sorted(pts, key=lambda x: x[0])

# compute the convex hulls
print("Computing convex hull using gift wrapping technique ... ", end="")
t = time.time()
hull_gift_wrapping = convex_hull_2d_gift_wrapping(pts)
# hull_gift_wrapping = c_convex_hull_2d_gift_wrapping(pts)
# hull_gift_wrapping = cc_convex_hull_2d_gift_wrapping(pts)
# hull_gift_wrapping = convex_hull(pts)
# hull_gift_wrapping = convex_hull_q2(pts)
print("done ! It took ", time.time() - t, " seconds")

print("Computing convex hull using divide and conquer technique ... ", end="")
t = time.time()
hull_divide_conquer = convex_hull_2d_divide_conquer(pts)
print("done ! It took ", time.time() - t, " seconds")

# close the convex hull for display
hull_gift_wrapping.append(hull_gift_wrapping[0])
hull_divide_conquer.append(hull_divide_conquer[0])

# display the convex hulls
if NUMBER_OF_POINTS <= 1000000:
    fig = plt.figure()
    ax = fig.add_subplot(131)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.title.set_text('Points')
    ax = fig.add_subplot(132)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.plot([x[0] for x in hull_gift_wrapping], [x[1] for x in hull_gift_wrapping], "ro--")
    ax.title.set_text('Gift Wrapping')
    ax = fig.add_subplot(133)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.plot([x[0] for x in hull_divide_conquer], [x[1] for x in hull_divide_conquer], "ro--")
    ax.title.set_text('Divide/Conquer')
    plt.show()
    # pylab.show()



