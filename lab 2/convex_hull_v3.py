import matplotlib.pyplot as plt
import time
import random


# Question 1. Implement the function is clockwise that will take as input three points A, B and C and return True if (A,B,C) is in clockwise ordering, False otherwise

# function that checks if three points a,b,c are clockwise positioned
def is_clockwise(a, b, c):
    # check if (cy−ay)*(bx−ax)<(by−ay)*(cx−ax)
    # if the condition is satisfied, then the 3 points are in clockwise direction
    if ((c[1] - a[1]) * (b[0] - a[0]) < (b[1] - a[1]) * (c[0] - a[0])):
        return True
    else:
        return False


# Question 2. Implement the function convex hull 2d gift wrapping that will compute the convex hull using the Gift Wrapping algorithm.

# compute with naive method the convex hull of the points cloud pts
# and store it as a list of vectors
def convex_hull_2d_gift_wrapping(pts):
    # find the leftmost point as the initial starting point
    l = 0
    for i in range(1, len(pts)):
        if pts[i][0] < pts[l][0]:
            l = i
    # store the leftmost starting point
    lm = pts[l]
    # create a list to store the points on the convex hull
    lst = []
    lst.append(lm)

    # keep iterating the list of points to find the convex hull point one by one in clockwise direction
    # find the next starting point which can form clockwise circles with all other points and the current starting point
    while (True):
        # choose a point p as the next temporary checking point
        # if the current starting point is the last element in the list, then set point p to be the first element in the list
        # otherwise, set the point to be the next point in the list of the current starting point for a quicker search
        p = (l + 1) % len(pts)

        # update the current point in clockwise direction
        for i in range(len(pts)):
            if i == l or i == p:
                continue
            # if the starting point, any other point i and current point p form a clockwise circle
            # then the current point p will be updated to point i for further evaluation
            if (is_clockwise(pts[l], pts[i], pts[p])):
                p = i

        # break the loop once the next point is the same as the initial leftmost starting point
        # which means all points are evaluated and the convex hull is formed
        if pts[p] == lm:
            break

        # otherwise, update the starting point to p and keep finding the next most clockwise point by repeating the process
        l = p
        lst.append(pts[l])

    return lst


# The time complexity for the gift wrapping algorithm is O(nh)

# test examples
# pts = [[0,1], [6,3], [10,2], [4,5], [8,4],[1,4.5],[4,2],[5,3.5],[7,0.5],[2,0.7]]
# [[0, 1], [1, 4.5], [4, 5], [8, 4], [10, 2], [7, 0.5], [2, 0.7]]

# pts = [[0,1], [6,3], [10,2], [4,5], [8,4],[1,4.5],[4,2],[5,3.5],[7,0.5]]
# [[0, 1], [1, 4.5], [4, 5], [8, 4], [10, 2], [7, 0.5]]

# pts = [[0,1], [6,3], [10,2], [4,5]]
# [[0, 1], [4, 5], [10, 2]]

# pts = [[2,3.3], [5,3.5],[6,3], [10,2], [4,5], [8,4],[1,4.5],[7,2]]
# print(convex_hull_2d_gift_wrapping(pts))


# Question 3. Implement the function convex hull 2d divide conquer that will compute the convex hull using the Divide-and-Conquer strategy.

# compute with divide and conquer method the convex hull of the points
# cloud pts and store it as a list of vectors
def convex_hull_2d_divide_conquer(pts):
    pts = sorted(pts)
    # directly return the convex hull in  clockwise direction by calling gift wrapping algorithm
    # if the number of points are less or equal to 4
    if len(pts) <= 4:
        return convex_hull_2d_gift_wrapping(pts)

    # otherwise, divide the points into two subparts recursively
    mid = int(len(pts) // 2)
    left = convex_hull_2d_divide_conquer(pts[:mid])
    right = convex_hull_2d_divide_conquer(pts[mid:])

    return merge(left, right)


# merge function for divide and conquer algo
def merge(leftp, rightp):
    # find the rightmost point of the leftside points
    r = r_copy = 0
    for i in range(1, len(leftp)):
        if leftp[i][0] > leftp[r][0]:
            r = i
    # make a copy of the original rightmost point
    r_copy = r

    # direcly extarct the leftmost point of the rightside points since it will be the first element stored in the clockwsie direction returned from gift wrapping
    # make a copy of the original leftmost point
    l = l_copy = 0

    # store the leftmost point of the right side and the rightmost point of the left side
    lm = rightp[l]
    rm = leftp[r]

    # create a list to store the index of points that form the convex hull
    lst = []

    # upper convex hull
    while True:
        # loop through right side points
        # choose the next point p in the list of the current starting point
        # since the next point on upper conevx hull must be the point in the clockwise direction for a quicker search
        p = (l + 1) % len(rightp)

        for i in range(len(rightp)):
            if i == p:
                continue
            if (is_clockwise(leftp[r], rightp[i], rightp[p])):
                p = i
        # update the most clockwise point for the current right point on the leftside
        l = p

        # loop through left side points
        # choose the previous point in the list of the current starting point
        # since the point will be in the counter-clockwise direction for a quicker search
        p = (len(leftp) + (r - 1)) % len(leftp)

        for i in range(len(leftp)):
            if i == p:
                continue
            if (not is_clockwise(rightp[l], leftp[i], leftp[p])):
                p = i
        # update the most counter-clockwise point for the current left point on the rightside
        r = p

        # check if the upper convex is formed such that the current right point r on the leftside
        # and the current left point l on the rightside form a clockwise cirle
        # with any other point i of the rightside
        qualified = True
        for i in range(len(rightp)):
            if rightp[i] == rightp[l] or rightp[i] == lm:
                continue
            if not is_clockwise(leftp[r], rightp[l], rightp[i]):
                qualified = False
                break

        if qualified:
            # break the loop if the upper convex hull is found
            # store the convex hull points in clockwise direction
            lst.append(r)
            lst.append(l)
            break

    # lower convex hull
    # set the initial starting points to the original leftmost and rightmost point
    # for a new loop searching the convex hull
    l = l_copy
    r = r_copy

    while True:
        # loop through right side points
        # choose the previous point in the list of the current starting point
        # since the point will be in the counter-clockwise direction for a quicker search
        p = (len(rightp) + (l - 1)) % len(rightp)

        for i in range(len(rightp)):
            if i == p:
                continue
            if (not is_clockwise(leftp[r], rightp[i], rightp[p])):
                p = i
        # update the most clockwise point for the current right point on the leftside
        l = p

        # loop through left side points
        # choose the next point p in the list of the current starting point
        # since the next point on upper conevx hull must be the point in the clockwise direction for a quicker search
        p = (r + 1) % len(leftp)

        for i in range(len(leftp)):
            if i == p:
                continue
            if (is_clockwise(rightp[l], leftp[i], leftp[p])):
                p = i
        # update the most counter-clockwise point for the current left point on the rightside
        r = p

        # check if the lower convex is formed such that the current right point r on the leftside
        # and the current left point l on the rightside form a counter-clockwise cirle
        # with any other point i of the rightside
        qualified = True
        for i in range(len(rightp)):
            if rightp[i] == rightp[l] or rightp[i] == lm:
                continue
            if is_clockwise(leftp[r], rightp[l], rightp[i]):
                qualified = False
                break
        if qualified:
            # store the index of the convex hull points in clockwise direction
            lst.append(l)
            lst.append(r)
            break

    # store all the convex hull points together from the leftmost point in clockwise direction
    hull = []

    # store the points on the left upper side of the convex hull
    for i in range(0, lst[0] + 1):
        hull.append(leftp[i])

    # store the points on the right upper and lower side of the convex hull
    if rightp[lst[2]] == rightp[0]:
        for j in range(lst[1], len(rightp)):
            hull.append(rightp[j])
        hull.append(rightp[lst[2]])
    else:
        for j in range(lst[1], lst[2] + 1):
            hull.append(rightp[j])

    # store the points on the left lower side of the convex hull
    if (leftp[lst[3]] == leftp[-1]):
        hull.append(leftp[lst[3]])
    elif leftp[lst[3]] == leftp[0]:
        return hull

    else:
        for i in range(lst[3], len(leftp)):
            hull.append(leftp[i])

    return hull


# The time complexity for the divide and conquer algorithm is O(nlog(n))

# pts = [[0,1], [6,3], [10,2], [4,5], [8,4],[1,4.5],[3.6,2],[5,3.5],[7,0.5],[2,0.7]]
# [[0, 1], [1, 4.5], [4, 5], [8, 4], [10, 2], [7, 0.5], [2, 0.7]]

# pts = [[0,1], [6,3], [10,2], [4,5], [8,4],[1,4.5],[5,3.5],[7,0.5]]
# [[0, 1], [1, 4.5], [4, 5], [8, 4], [10, 2], [7, 0.5]]

# pts = [[0,1], [6,3], [10,2], [4,5]]
# [[0, 1], [4, 5], [10, 2]]

# pts = [[0,1], [1,4.5], [6,3], [8,4], [10,2], [4,5], [7,0.5]]

# pts = [[0,1], [6,3], [10,2], [4,5], [8,4],[1,4.5],[7.5,2]]
# [[0,1],[1,4.5],[4, 5], [8, 4], [10, 2]]

# pts = [[2,3.3], [5,3.5],[6,3], [10,2], [4,5], [8,4],[1,4.5],[7,2]]
# [[1, 4.5], [4, 5], [8, 4], [10, 2], [7, 2], [2, 3.3]]
# print(convex_hull_2d_divide_conquer(pts))


NUMBER_OF_POINTS = 1000000

# generate random points and sort them accoridng to x coordinate
pts = []
for i in range(NUMBER_OF_POINTS): pts.append([random.random(), random.random()])
pts = sorted(pts, key=lambda x: x[0])

# compute the convex hulls
print("Computing convex hull using gift wrapping technique ... ", end="")
t = time.time()
hull_gift_wrapping = convex_hull_2d_gift_wrapping(pts)
print("done ! It took ", time.time() - t, " seconds")

# divide and conquer
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
    plt.show(block=True)