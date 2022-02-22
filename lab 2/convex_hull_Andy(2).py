#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import time
import random


# In[2]:


# function that checks if three points a,b,c are clockwise positioned 
def is_clockwise(a,b,c):
    return (c[1] - a[1]) * (b[0] - a[0]) < (b[1] - a[1]) * (c[0] - a[0])

# function that checks if three points a,b,c are counterclockwise positioned 
def is_counterclockwise(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


# In[3]:


def convex_hull_2d_gift_wrapping_helper(pts, start, end):
    if start == end:
        return []
    
    LEFTMOST_INDEX = start  # leftmost point index in pts
    convex_hull = []
    point_on_hull_index = LEFTMOST_INDEX  # leftmost point is guaranteed to be part of convex hull
    while True:
        convex_hull.append(pts[point_on_hull_index])
        endpoint_index = start  # initial endpoint for a candidate edge on the hull
        for i in range(start, end):
            if point_on_hull_index == endpoint_index or is_clockwise(pts[point_on_hull_index],
                                                                     pts[endpoint_index],
                                                                     pts[i]):
                endpoint_index = i  # found greater right turn, update endpoint
        point_on_hull_index = endpoint_index  # endpoint_index can be added to convex hull at next round
        if endpoint_index == LEFTMOST_INDEX:
            break
    return convex_hull


# In[4]:


# compute with naive method the convex hull of the points cloud pts 
# and store it as a list of vectors
def convex_hull_2d_gift_wrapping(pts):
    # return in counterclockwise order, starts from the leftmode point
    return convex_hull_2d_gift_wrapping_helper(pts, 0, len(pts))


# In[5]:


def counterclockwise_shift(i, arr):
    N = len(arr)
    return (i + 1) % N

def clockwise_shift(i, arr):
    N = len(arr)
    return (i + N - 1) % N


# In[6]:


def get_rightmost_point(pts):
    rightmost = 0
    for i in range(1, len(pts)):
        if pts[i][0] > pts[rightmost][0]:
            rightmost = i
    return rightmost

def get_leftmost_point(pts):
    return 0
    '''
    leftmost = 0
    for i in range(1, len(pts)):
        if pts[i][0] > pts[leftmost][0]:
            leftmost = i
    return leftmost
    '''


# In[7]:


def liftup_connection(left_convex_hull, upper_r, right_convex_hull, upper_l):
    while True:
        left_changed = False
        r_next = counterclockwise_shift(upper_r, left_convex_hull)
        while is_clockwise(right_convex_hull[upper_l],
                           left_convex_hull[upper_r],
                           left_convex_hull[r_next]):
            upper_r = r_next
            r_next = counterclockwise_shift(upper_r, left_convex_hull)
            left_changed = True

        right_changed = False
        l_next = clockwise_shift(upper_l, right_convex_hull)
        while is_counterclockwise(left_convex_hull[upper_r],
                                  right_convex_hull[upper_l],
                                  right_convex_hull[l_next]):
            upper_l = l_next
            l_next = clockwise_shift(upper_l, right_convex_hull)
            right_changed = True

        if not left_changed and not right_changed:
            return (upper_r, upper_l)

def pulldown_connection(left_convex_hull, lower_r, right_convex_hull, lower_l):
    while True:
        left_changed = False
        r_next = clockwise_shift(lower_r, left_convex_hull)
        while is_counterclockwise(right_convex_hull[lower_l],
                                  left_convex_hull[lower_r],
                                  left_convex_hull[r_next]):
            lower_r = r_next
            r_next = clockwise_shift(lower_r, left_convex_hull)
            left_changed = True

        right_changed = False
        l_next = counterclockwise_shift(lower_l, right_convex_hull)
        while is_clockwise(left_convex_hull[lower_r],
                           right_convex_hull[lower_l],
                           right_convex_hull[l_next]):
            lower_l = l_next
            l_next = counterclockwise_shift(lower_l, right_convex_hull)
            right_changed = True

        if not left_changed and not right_changed:
            return (lower_r, lower_l)


# In[8]:


def merge(left_convex_hull, right_convex_hull):
    # connect 2 hulls together and adjust the connection points
    RIGHTMOST_FROM_LEFT_HULL = get_rightmost_point(left_convex_hull)
    LEFTMOST_FROM_RIGHT_HULL = get_leftmost_point(right_convex_hull)

    (upper_r, upper_l) = liftup_connection(
        left_convex_hull, RIGHTMOST_FROM_LEFT_HULL,
        right_convex_hull, LEFTMOST_FROM_RIGHT_HULL)
    (lower_r, lower_l) = pulldown_connection(
        left_convex_hull, RIGHTMOST_FROM_LEFT_HULL,
        right_convex_hull, LEFTMOST_FROM_RIGHT_HULL)
    
    # merge the 2 hulls from the connection points
    convex_hull = []
    for i in range(lower_r + 1):
        convex_hull.append(left_convex_hull[i])
    if upper_l > 0:
        for i in range(lower_l, upper_l + 1):
            convex_hull.append(right_convex_hull[i])
    else:
        for i in range(lower_l, len(right_convex_hull)):
            convex_hull.append(right_convex_hull[i])
        convex_hull.append(right_convex_hull[0])    
    if upper_r > 0:
        for i in range(upper_r, len(left_convex_hull)):
            convex_hull.append(left_convex_hull[i])

    return convex_hull


# In[9]:


def convex_hull_2d_divide_conquer_helper(pts, start, end):
    if end - start < 5:
        return convex_hull_2d_gift_wrapping_helper(pts, start, end)
    
    mid = (1 + start + end) // 2
    left_convex_hull = convex_hull_2d_divide_conquer_helper(pts, start, mid)
    right_convex_hull = convex_hull_2d_divide_conquer_helper(pts, mid, end)
    return merge(left_convex_hull, right_convex_hull)


# In[10]:


# compute with divide and conquer method the convex hull of the points  
# cloud pts and store it as a list of vectors
def convex_hull_2d_divide_conquer(pts):
    # return in counterclockwise order, starts from the leftmode point
    return convex_hull_2d_divide_conquer_helper(pts, 0, len(pts))


# In[11]:


NUMBER_OF_POINTS = 100000

# generate random points and sort them accoridng to x coordinate
pts = []
for i in range(NUMBER_OF_POINTS): pts.append([random.random(),random.random()]) 
pts = sorted(pts, key=lambda x: x[0])



# compute the convex hulls
print("Computing convex hull using gift wrapping technique ... ",end="")
t = time.time()
hull_gift_wrapping = convex_hull_2d_gift_wrapping(pts)
print("done ! It took ",time.time() - t," seconds")

print("Computing convex hull using divide and conquer technique ... ",end="")
t = time.time()
hull_divide_conquer = convex_hull_2d_divide_conquer(pts)
print("done ! It took ",time.time() - t," seconds")

# close the convex hull for display
hull_gift_wrapping.append(hull_gift_wrapping[0])
hull_divide_conquer.append(hull_divide_conquer[0])


# In[12]:


# display the convex hulls
if NUMBER_OF_POINTS<1000:
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


# In[ ]:




