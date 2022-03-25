import matplotlib.pyplot as plt
import time
import numpy as np
import random
import heapq
import math

INFINITY = math.inf  # defines a variable for infinity


# displays a MST
def plot_MST(pts, MST):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    for i in range(len(MST)):
        for j in range(len(MST)):
            if MST[i][j] != np.infty: ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], "bo-")
    ax.title.set_text('Minimum Spanning Tree')


# computes the Euclidean distance between two points p1 and p2
def euclidean_distance(p1, p2):
    return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


# computes the length of a TSP solution
def compute_sol_length(graph, solution):
    length = 0
    for i in range(len(solution) - 1): length = length + graph[solution[i]][solution[i + 1]]
    return length


# computes with random method the TSP solution
def TSP_random(graph):
    return list(np.random.permutation(len(graph)))


# computes with closest neighbor method the TSP solution
def TSP_closest_neighbor(graph):
    # start with a random node
    random_start = random.randrange(len(graph))
    start_node = random_start
    sol = [random_start]

    # loop through the distance list of the start_node
    min_node = 0
    while not (len(sol) == len(graph)):
        min_length = float("inf")

        # find the possible minimum node which will become to the next start node
        for j in range(len(graph[start_node])):
            if graph[start_node][j] < min_length and j != start_node and j not in sol:
                min_length = graph[start_node][j]
                min_node = j

        # record the current node as marked
        sol.append(min_node)
        start_node = min_node

    # go back to the original start node
    sol.append(random_start)
    return sol


# helper function for prims_algo to check whether we have already marked all nodes
def marked(bucket):
    flag = False
    for i in bucket:
        if i == 0:
            flag = True

    # false for visited all node, true for there are still have nodes to be visited
    return flag


# computes the Minimum Spanning Tree by using the Prim's Algorithm
def prims_algo(graph):
    distance_list = []
    start_node = 0
    for i in range(len(graph)):
        if i == start_node:
            distance_list.append([0, start_node])
        else:
            distance_list.append([INFINITY, None])
    node_list = []
    bucket = [0] * len(graph)

    while marked(bucket):
        min_distance = INFINITY
        min_node = -1
        prev_node = None

        # find the node with minimum distance
        for i in range(len(distance_list)):
            if bucket[i] == 0 and distance_list[i][0] < min_distance:
                min_distance = distance_list[i][0]
                min_node = i
                prev_node = distance_list[i][1]

        # recorded in the node_list
        node_list.append((prev_node, min_node))
        bucket[min_node] = 1

        # updated the distance list according to the current min node
        for i in range(len(graph[min_node])):
            if distance_list[i][0] > graph[min_node][i] and bucket[i] == 0:
                distance_list[i][0] = graph[min_node][i]
                distance_list[i][1] = min_node

    return node_list

# function to compute a Minimum Spanning Tree for the graph
def compute_MST(graph):
    prim = prims_algo(graph)
    graph_MST = prim[1:]
    return graph_MST

# function to visit all nodes from a graph by using depth first search
def dfs(visited_list, graph, start_node):
    visited_list += [start_node]
    for i in range(len(graph[start_node])):
        if graph[start_node][i] != INFINITY and i not in visited_list:
            visited_list = dfs(visited_list, graph, i)
    return visited_list


# computes the preorder walk in the tree corresponding to DFS
def DFS_preorder(graph, start_node):
    visited_list = []
    path = dfs(visited_list, graph, start_node)
    return path


# computes with Minimum Spanning Tree the TSP solution
def TSP_min_spanning_tree(graph):
    MST = compute_MST(graph)

    graph_MST = [[]] * len(graph)
    for i in range(len(graph)): graph_MST[i] = [np.infty for j in range(len(graph))]
    for i in range(len(MST)):
        graph_MST[MST[i][0]][MST[i][1]] = graph[MST[i][0]][MST[i][1]]
        graph_MST[MST[i][1]][MST[i][0]] = graph[MST[i][1]][MST[i][0]]

    plot_MST(pts, graph_MST)
    return DFS_preorder(graph_MST, 0)


NUMBER_OF_POINTS = 20

# generates random points and sort them accoridng to x coordinate
pts = []
for i in range(NUMBER_OF_POINTS): pts.append([random.randint(0, 1000), random.randint(0, 1000)])
pts = sorted(pts, key=lambda x: x[0])

graph = [[]] * NUMBER_OF_POINTS
for i in range(NUMBER_OF_POINTS): graph[i] = [euclidean_distance(pts[i], pts[j]) for j in range(NUMBER_OF_POINTS)]

# computes the TSP solutions
print("Computing TSP solution using random technique ... ", end="")
t = time.time()
TSP_sol_random = TSP_random(graph)
print("done ! \n It took %.2f seconds - " % (time.time() - t), end="")
print("length found: %.2f" % (compute_sol_length(graph, TSP_sol_random)))

print("Computing TSP solution using closest neighbor technique ... ", end="")
t = time.time()
TSP_sol_closest_neighbor = TSP_closest_neighbor(graph)
print("done ! \n It took %.2f seconds - " % (time.time() - t), end="")
print("length found: %.2f" % (compute_sol_length(graph, TSP_sol_closest_neighbor)))

print("Computing TSP solution using Minimum Spanning Tree technique ... ", end="")
t = time.time()
TSP_sol_min_spanning_tree = TSP_min_spanning_tree(graph)
print("done ! \n It took %.2f seconds - " % (time.time() - t), end="")
print("length found: %.2f" % (compute_sol_length(graph, TSP_sol_min_spanning_tree)))

# closes the TSP solution for display if needed
if TSP_sol_random[0] != TSP_sol_random[-1]: TSP_sol_random.append(TSP_sol_random[0])
if TSP_sol_closest_neighbor[0] != TSP_sol_closest_neighbor[-1]: TSP_sol_closest_neighbor.append(
    TSP_sol_closest_neighbor[0])
if TSP_sol_min_spanning_tree[0] != TSP_sol_min_spanning_tree[-1]: TSP_sol_min_spanning_tree.append(
    TSP_sol_min_spanning_tree[0])

# displays the TSP solution
if NUMBER_OF_POINTS < 100:
    fig = plt.figure()
    ax = fig.add_subplot(221)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.title.set_text('Points')
    ax = fig.add_subplot(222)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.plot([pts[x][0] for x in TSP_sol_random], [pts[x][1] for x in TSP_sol_random], "ro--")
    ax.title.set_text('TSP Random')
    ax = fig.add_subplot(223)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.plot([pts[x][0] for x in TSP_sol_closest_neighbor], [pts[x][1] for x in TSP_sol_closest_neighbor], "ro--")
    ax.title.set_text('TSP Closest Neighbor')
    ax = fig.add_subplot(224)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.plot([pts[x][0] for x in TSP_sol_min_spanning_tree], [pts[x][1] for x in TSP_sol_min_spanning_tree], "ro--")
    ax.title.set_text('TSP Minimum Spanning Tree')
    plt.show(block=True)
