import matplotlib.pyplot as plt
import time
import random

# Question 1. Implement the function is clockwise that will take as input three points A, B and C and return True if (A,B,C) is in clockwise ordering, False otherwise 

# function that checks if three points a,b,c are clockwise positioned 
def is_clockwise(a,b,c):
	# check if (cy−ay)*(bx−ax)<(by−ay)*(cx−ax)
	# if the condition is satisfied, then the 3 points are in clockwise direction
	if ((c[1]-a[1])*(b[0]-a[0]) < (b[1]-a[1])*(c[0]-a[0])):
		return True
	else:
		return False


# Question 2. Implement the function convex hull 2d gift wrapping that will compute the convex hull using the Gift Wrapping algorithm.

# compute with naive method the convex hull of the points cloud pts 
# and store it as a list of vectors
def convex_hull_2d_gift_wrapping(pts):

	# find the leftmost point as the initial starting point
	l = 0
	for i in range(1,len(pts)):	
		if pts[i][0] < pts[l][0]:
			l = i
	# store the leftmost starting point
	lm = pts[l]
	# create a list to store the points on the conven hull 
	lst = []
	lst.append(lm)

	# keep iterating the list of points to find the convex hull point one by one in clockwise direction
	# find the next starting point which can form clockwise circles with all other point and the current starting point
	while (True):
		# choose a point p as the next temporary checking point
		# if the current starting point is the last element in the list, then set point p to be the first element in the list
		# otherwise, set the point to be the next point in the list of the current starting point
		if l == len(pts)-1:
			p = 0
		else:
			p = l+1

		# update the current point in clockwise direction
		for i in range(len(pts)):
			if i == l or i == p:
				continue
			# if the starting point, any other point i and current point p form a clockwise circle
			# then the point i will be the next upper point selected to be evaluated as the current point
			if (is_clockwise(pts[l],pts[i],pts[p])):
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
#pts = [[0,1], [6,3], [10,2], [4,5], [8,4],[1,4.5],[4,2],[5,3.5],[7,0.5],[2,0.7]]
#[[0, 1], [1, 4.5], [4, 5], [8, 4], [10, 2], [7, 0.5], [2, 0.7]]

#pts = [[0,1], [6,3], [10,2], [4,5], [8,4],[1,4.5],[4,2],[5,3.5],[7,0.5]]
#[[0, 1], [1, 4.5], [4, 5], [8, 4], [10, 2], [7, 0.5]]

#pts = [[0,1], [6,3], [10,2], [4,5]]
#[[0, 1], [4, 5], [10, 2]]

#print(convex_hull_2d_gift_wrapping(pts))


# Question 3. Implement the function convex hull 2d divide conquer that will compute the convex hull using the Divide-and-Conquer strategy.

# compute with divide and conquer method the convex hull of the points  
# cloud pts and store it as a list of vectors
def convex_hull_2d_divide_conquer(pts):
	pts = sorted(pts)
	# directly return the convex hull calling gift wrapping algorithm if the number of points less or equal to 4
	if len(pts) <= 4:
		return convex_hull_2d_gift_wrapping(pts)

	# otherwise, divide the points into two subparts recursively 
	mid = int(len(pts) // 2)
	left = convex_hull_2d_divide_conquer(pts[:mid])
	right = convex_hull_2d_divide_conquer(pts[mid:])

	return merge(left,right)


# merge function for divide and conquer algo
def merge(leftp, rightp):

	# find the rightmost point of the left side points
	r = r_copy = 0
	for i in range(1,len(leftp)):	
		if leftp[i][0] > leftp[r][0]:
			r = i
	# make a copy of the original rightmost point 
	r_copy = r

	# find the leftmost point of the right side points 
	# l = l_copy = 0
	# for i in range(1,len(rightp)):	
	# 	if rightp[i][0] < rightp[l][0]:
	# 		l = i

	# direcly extarct the leftmost point since 
	# it will be the first element stored in the clockwsie direction returned from gift wrapping
	# make a copy of the original leftmost point 
	l = l_copy = 0
	#l_copy = l

	# store the lefomost point of the right side and the rightmost point of the left side 
	lm = rightp[l]
	rm = leftp[r]

	# create a list to store the index of points that form the conven hull 
	lst = []

	while True:
		while True:
			# loop through right side points
			while (True):
				if l == len(rightp)-1:
					p = 0
				else:
					# choose the next point in the list of the current starting point
					# the next point must be the point in the clockwise direction for a quicker search
					p = l+1

				for i in range(len(rightp)):
					if i == p:
						continue
					if (is_clockwise(leftp[r],rightp[i],rightp[p])):
						p = i
				l = p
				# break the loop once the next clockwise point is found
				break

			# loop through left side points
			while (True):
				if r == 0:
					p = -1
				else:
					# choose the previous point in the list of the current starting point
					# since the point will be in the counter-clockwise direction for a quicker search
					p = r-1

				for i in range(len(leftp)):
					if i == p:
						continue
					if ( not is_clockwise(rightp[l],leftp[i],leftp[p])):
						p = i
				r = p
				break

			qualified = True
			for i in range(len(rightp)):
				if  rightp[i] == rightp[l] or rightp[i] == lm:
					continue
				if not is_clockwise(leftp[r],rightp[l],rightp[i]):
					qualified = False
					break

			if qualified:
				# break the loop if the upper convex hull is found 
				# store the convex hull points in clockwise dorection
				# lst.append(leftp[r])
				# lst.append(rightp[l])
				lst.append(r)
				lst.append(l)
				break

		# set the initial starting point to the original leftmost and rightmost point 
		# for a new loop searching the convex hull
		l = l_copy
		r = r_copy
		while True:
			# loop through right side points
			while (True):
				if l == 0:
					p = -1
				else:
					# choose the previous point in the list of the current starting point
					# since the point will be in the counter-clockwise direction for a quicker search
					p = l-1

				for i in range(len(rightp)):
					if i == p:
						continue
					if ( not is_clockwise(leftp[r],rightp[i],rightp[p])):
						p = i
				l = p
				break

			# loop through left side points
			while (True):
				if r == len(leftp)-1:
					p = 0
				else:
					# choose the next point in the list of the current starting point
					# since the point will be in the clockwise direction for a quicker search
					p = r+1

				for i in range(len(leftp)):
					if i == p:
						continue
					if (is_clockwise(rightp[l],leftp[i],leftp[p])):
						p = i
				r = p
				break

			qualified = True
			for i in range(len(rightp)):
				if  rightp[i] == rightp[l] or rightp[i] == lm:
					continue			
				if is_clockwise(leftp[r],rightp[l],rightp[i]):
					qualified = False
					break
			if qualified:
				# lst.append(rightp[l])
				# lst.append(leftp[r])
				# store the index of the convex hull point in clockwise direction
				lst.append(l)
				lst.append(r)
				break
		break

	# store all the connevx hull points together from the leftmost point in clockwise direction
	# hull = []

	# for i in range(0,leftp.index(lst[0])+1):
	# 	hull.append(leftp[i])

	# if lst[2] == rightp[0]:
	# 	ubound = len(rightp)
	# 	for j in range(rightp.index(lst[1]),ubound):
	# 		hull.append(rightp[j])
	# 	hull.append(lst[2])
	# else:
	# 	ubound = rightp.index(lst[2]) + 1
	# 	for j in range(rightp.index(lst[1]),ubound):
	# 		hull.append(rightp[j])

	# if (lst[3] == leftp[-1]):
	# 	hull.append(lst[3])
	# elif lst[3] == leftp[0]:
	# 	return hull

	# else:
	# 	for i in range(leftp.index(lst[3]),len(leftp)):
	# 		hull.append(leftp[i])

	# return hull

	# store all the connevx hull points together from the leftmost point in clockwise direction
	hull = []

	# store the points on the left upper side of the convex hull 
	for i in range(0,lst[0]+1):
		hull.append(leftp[i])

	# store the points on the right upper and lower side of the convex hull 
	if rightp[lst[2]] == rightp[0]:
		ubound = len(rightp)
		for j in range(lst[1],ubound):
			hull.append(rightp[j])
		hull.append(rightp[lst[2]])
	else:
		ubound = lst[2] + 1
		for j in range(lst[1],ubound):
			hull.append(rightp[j])

	# store the points on the left lower side of the convex hull 
	if (leftp[lst[3]] == leftp[-1]):
		hull.append(leftp[lst[3]])
	elif leftp[lst[3]] == leftp[0]:
		return hull

	else:
		for i in range(lst[3],len(leftp)):
			hull.append(leftp[i])

	return hull

# The time complexity for the gift wrapping algorithm is O(n)

#pts = [[0,1], [6,3], [10,2], [4,5], [8,4],[1,4.5],[3.6,2],[5,3.5],[7,0.5],[2,0.7]]
#[[0, 1], [1, 4.5], [4, 5], [8, 4], [10, 2], [7, 0.5], [2, 0.7]]

#pts = [[0,1], [6,3], [10,2], [4,5], [8,4],[1,4.5],[5,3.5],[7,0.5]]
#[[0, 1], [1, 4.5], [4, 5], [8, 4], [10, 2], [7, 0.5]]

#pts = [[0,1], [6,3], [10,2], [4,5]]
#[[0, 1], [4, 5], [10, 2]]

#pts = [[0,1], [1,4.5], [6,3], [8,4], [10,2], [4,5], [7,0.5]]


#pts = [[0,1], [6,3], [10,2], [4,5], [8,4],[1,4.5],[7.5,2]]
#[[0,1],[1,4.5],[4, 5], [8, 4], [10, 2]]

pts = [[2,3.3], [5,3.5],[6,3], [10,2], [4,5], [8,4],[1,4.5],[7,2]]
#[[1, 4.5], [4, 5], [8, 4], [10, 2], [7, 2], [2, 3.3]]

#pts = [[0.050275632788999935, 0.6212190525141322], [0.06742111176249388, 0.27803426557052924], [0.12877781374127695, 0.031173212754512014], [0.16422647534425872, 0.7801098392476471], [0.18329745656608076, 0.7409020187783513], [0.19043894765102898, 0.5012192215115943], [0.19826469282179593, 0.11692507601015412], [0.2142606511308549, 0.9696450597946759], [0.23023927731860006, 0.9907474890685675], [0.23305629868742328, 0.15465271215313836], [0.30547433223960274, 0.1346492825862644], [0.3700284184514113, 0.22689752962313736], [0.38204833950573436, 0.6720935290492157], [0.39007694968260476, 0.24353779172767043], [0.45047853231883617, 0.06139250631697968], [0.4699128310398303, 0.5198358465702191], [0.6358075592007094, 0.7793521534225599], [0.7970165131917074, 0.7557157074785478], [0.8759363389523784, 0.875919408977944], [0.9269472371613845, 0.953460561538792]]
# [[0.050275632788999935, 0.6212190525141322], [0.06742111176249388, 0.27803426557052924], [0.12877781374127695, 0.031173212754512014], [0.16422647534425872, 0.7801098392476471], [0.18329745656608076, 0.7409020187783513], [0.19043894765102898, 0.5012192215115943], [0.19826469282179593, 0.11692507601015412], [0.2142606511308549, 0.9696450597946759], [0.23023927731860006, 0.9907474890685675], [0.23305629868742328, 0.15465271215313836], [0.30547433223960274, 0.1346492825862644], [0.3700284184514113, 0.22689752962313736], [0.38204833950573436, 0.6720935290492157], [0.39007694968260476, 0.24353779172767043], [0.45047853231883617, 0.06139250631697968], [0.4699128310398303, 0.5198358465702191], [0.6358075592007094, 0.7793521534225599], [0.7970165131917074, 0.7557157074785478], [0.8759363389523784, 0.875919408977944], [0.9269472371613845, 0.953460561538792]]
# print(convex_hull_2d_divide_conquer(pts))
    


NUMBER_OF_POINTS = 1000000

# generate random points and sort them accoridng to x coordinate
pts = []
for i in range(NUMBER_OF_POINTS): pts.append([random.random(),random.random()]) 
pts = sorted(pts, key=lambda x: x[0])



# compute the convex hulls

# gift wrapping
print("Computing convex hull using gift wrapping technique ... ",end="")
t = time.time()
hull_gift_wrapping = convex_hull_2d_gift_wrapping(pts)
print("done ! It took ",time.time() - t," seconds")


# divide and conquer
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


    
