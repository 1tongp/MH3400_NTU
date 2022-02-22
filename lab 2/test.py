# find the next convex point
#for k in range(0, len(pts)):
    #convex_check = True
    #for j in range(0, len(pts)):
        #if not is_clockwise(pts[leftmost_index], pts[k],
                            #pts[j]) and k != leftmost_index and j != leftmost_index and k != j:
            #convex_check = False
        #if is_clockwise(pts[leftmost_index], pts[k],
                       #pts[j]) and k != leftmost_index and j != leftmost_index and k != j:
           # convex_check = False
  #  if convex_check:
      #  leftmost_index = k
     #   print("next", k)
      #  convex_hull.append(pts[leftmost_index])

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

    m = 1
    convex_hull_list.append(pts[leftmost_index])
    current = leftmost_index

    while True:
        next_p = current
        for y in range(len(pts)):
            c = cross(convex_hull_list[m - 1], pts[y], pts[next_p])
            if c > 0:
                next_p = y

        convex_hull_list.append(pts[next_p])
        m += 1
        current = next_p

        if next_p == leftmost_index:
            break

    return convex_hull_list







    m = 1
    p = leftmost_index
    convex_hull_list.append(pts[p])

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

