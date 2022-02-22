import matplotlib.pyplot as plt
import time
import random


# function that checks if three points a,b,c are clockwise positioned 
def is_clockwise(a,b,c):
    return (c[1] - a[1]) * (b[0] - a[0]) < (b[1] - a[1]) * (c[0] - a[0])

# function that checks if three points a,b,c are counterclockwise positioned 
def is_counterclockwise(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

# compute with naive method the convex hull of the points cloud pts 
# and store it as a list of vectors
def convex_hull_2d_gift_wrapping(pts):
    LEFTMOST_INDEX = 0  # leftmost point index in pts

    convex_hull = []
    point_on_hull_index = LEFTMOST_INDEX # leftmost point is guaranteed to be part of convex hull
    while True:
        convex_hull.append(pts[point_on_hull_index])
        endpoint_index = 0 # initial endpoint for a candidate edge on the hull
        for i in range(len(pts)):
            if point_on_hull_index==endpoint_index or is_counterclockwise(pts[point_on_hull_index], pts[endpoint_index], pts[i]):
                endpoint_index = i # found greater left turn, update endpoint
        point_on_hull_index = endpoint_index # endpoint_index can be added to convex hull at next round
        if endpoint_index == LEFTMOST_INDEX:
            break
    return convex_hull


# compute with divide and conquer method the convex hull of the points  
# cloud pts and store it as a list of vectors
def convex_hull_2d_divide_conquer(pts):
    return [pts[0]]


    
NUMBER_OF_POINTS = 1000000

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

# display the convex hulls
if NUMBER_OF_POINTS<=1000000:
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


    
