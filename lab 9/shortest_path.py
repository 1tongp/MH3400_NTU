from random import randint
import math
import networkx as nx
import matplotlib.pyplot as plt

NODES = 8  # defines number of nodes in the graph
EDGES = 16  # defines number of edges in the graph
DIRECTED = True  # defines if the graph is directed or undirected
NEGATIVE_WEIGHT = False  # defines if the edges can have negative weight
INFINITY = math.inf  # defines a variable for infinity


# helper function for dijkstra algorithm to check if there is still an edge to go from the start node
def marked(bucket, distance_list):
    flag = False

    # if there is an unvisited node, and we can reach this node from the start node
    # then set the flag as True
    for i in range(len(distance_list)):
        if bucket[i] == 0 and distance_list[i][0] != INFINITY:
            flag = True

    # True means keep looping, false means stop the searching action
    return flag


# function that implements the Dijkstra's algorithm for single-pair shortest paths
def dijkstra(graph, start_node):
    D = [INFINITY] * len(graph)
    # bucket records if the node has been visited or not, 0 means not, 1 means visited
    bucket = [0] * len(graph)

    # distance list is a list of list in [weight, step stone node] format
    # weight is the accumulated weight from the start node to the current node
    # step stone node is the previous node for current node, which can link the start node and the current node
    # current node is the index of the distance list
    distance_list = []
    for i in range(len(graph)):
        if i == start_node:
            distance_list.append([0, start_node])
        else:
            distance_list.append([INFINITY, None])

    # start updating the distance list
    while marked(bucket, distance_list):

        # find the next node, which has the smallest weight
        min_distance = INFINITY
        next_node = -1
        for i in range(len(distance_list)):
            if distance_list[i][0] < min_distance and bucket[i] == 0:
                min_distance = distance_list[i][0]
                next_node = distance_list[i][1]

        # mark the next_node as visited
        bucket[next_node] = 1

        # update the distance for next_node
        D[next_node] = min_distance

        # find the next node to be reached, and update the distance_list
        for i in graph[next_node]:

            # break the loop if the current node has no way to go
            if not i:
                break

            # otherwise, start from the current node, and update the distance list if needed
            elif distance_list[i[0]][0] > min_distance + i[1]:
                distance_list[i[0]][0] = min_distance + i[1]
                distance_list[i[0]][1] = i[0]

    return D


# function that implements the Floyd-Warshall's algorithm for all-pairs the shortest paths
def floyd_warshall(graph):

    # initialize a list of list with all the values equal to Inf
    D = [[[INFINITY for i in range(len(graph))] for j in range(len(graph))] for k in range(len(graph) + 1)]
    D = D[len(graph)][:][:]

    # change the adjacency list graph into the adjacency matrix without any step stone
    for i in range(len(graph)):
        D[i][i] = 0
        for z in range(len(graph[i])):
            update_index = graph[i][z][0]
            update_value = graph[i][z][1]
            D[i][update_index] = update_value

    # core code for the floyd_warshall algorithm
    for k in range(len(graph)):
        for i in range(len(graph)):
            for z in range(len(graph)):

                # compare and update the distance if needed
                if D[i][z] > D[i][k] + D[k][z] and D[i][k] < INFINITY and D[k][z] < INFINITY:
                    D[i][z] = D[i][k] + D[k][z]

    return D


# function that creates the graph
def make_graph(NUMBER_NODES, NUMBER_EDGES, NEGATIVE_WEIGHT, DIRECTED):
    if NODES * NODES < NUMBER_EDGES:
        print("Impossible to generate a simple graph with %i nodes and %i edges!\n" % (NUMBER_NODES, NUMBER_EDGES))
        return None
    g = [[] for i in range(NUMBER_NODES)]
    for i in range(NUMBER_EDGES):
        while True:
            start_node = randint(0, NUMBER_NODES - 1)
            end_node = randint(0, NUMBER_NODES - 1)
            if NEGATIVE_WEIGHT:
                weight = randint(-20, 20)
            else:
                weight = randint(1, 20)
            if (start_node != end_node):
                found = False
                for j in range(len(g[start_node])):
                    if g[start_node][j][0] == end_node: found = True
                if not found: break
        g[start_node].append([end_node, weight])
        if DIRECTED == False: g[end_node].append([start_node, weight])
    return g


# function that prints the graph
def print_graph(g, DIRECTED):
    if DIRECTED:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    for i in range(len(g)): G.add_node(i)
    for i in range(len(g)):
        for j in range(len(g[i])): G.add_edge(i, g[i][j][0], weight=g[i][j][1])
    for i in range(len(g)):
        print("from node %02i: " % (i), end="")
        print(g[i])
    try:
        pos = nx.planar_layout(G)
        nx.draw(G, pos, with_labels=True)
    except nx.NetworkXException:
        print("\nGraph is not planar, using alternative representation")
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True)
    if DIRECTED:
        labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.3)
    else:
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)


print("\n\n ******** GENERATING GRAPH ********")
g = make_graph(NODES, EDGES, NEGATIVE_WEIGHT, DIRECTED)
if g == None:
    raise SystemExit(0)
elif NODES < 50 and EDGES < 2500:
    plt.figure(1, figsize=(10, 10))
    print_graph(g, DIRECTED)

print("\n\n ******** PERFORMING DIJKSTRA ********")
D = dijkstra(g, 0)
print("Single-Pair Distance Table (from node 0): ", end="")
print(D)
# for p in range(len(g)):
#     D = dijkstra(g, p)
#     print("Single-Pair Distance Table (from node ", p, ")", end="")
#     print(D)

print("\n\n ******** PERFORMING FLOYD WARSHALL ********")
D = floyd_warshall(g)
print("All-Pairs Distance Table: \n", end="")
for j in range(len(g)):
    print("from node %02i: " % (j), end="")
    print(D[j])
