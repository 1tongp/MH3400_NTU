from random import shuffle, randrange, random
import math

MAZE_SIZE = 10

# function to convert the g graph into an adjacency list
# key is the node in the graph, value is the next possible nodes from key node
def graph_dic(graph):
    coor_dic = dict()
    for i in range(MAZE_SIZE * MAZE_SIZE):
        coor_dic[i] = set(graph[i])
    return coor_dic

# function to find the path by using dfs algo
def dfs_paths(graph, start, goal, result, path = None):

    # first time calling dfs_paths function, start finding the path from start node
    if path is None and start != goal:
        path = [start]

    # found a path from start node to goal node
    if start == goal:
        result.append(path)

    # find the next possible node if did not reach the goal node
    for next_node in graph[start] - set(path):
        dfs_paths(graph, next_node, goal, result, path + [next_node])

    return result

def DFS_search(g, start_node, end_node):

    # convert the adjacency list format to represent the graph
    graph = graph_dic(g)

    # result container contains the possible path from the starting node to the ending node
    result_container = []
    result = dfs_paths(graph, start_node, end_node, result_container)

    # there is no possible path between the starting node to the ending node, return []
    if not result:
        return []

    # return founded path
    return result[0]

# function to find the path (also the shortest path) by using bfs Algo
def bfs_paths(graph, start, goal):

    # queue records the next possible nodes
    # paths records the corresponding accumulated path from start to current node
    queue = [start]
    paths = [[start]]

    while queue:
        node = queue.pop(0)
        path = paths.pop(0)

        # find the next possible node
        for next_node in graph[node] - set(path):

            # found the path, simply return this path
            if next_node == goal:
                return path + [next_node]

            # otherwise, loop again to try on next possible node
            else:
                queue.append(next_node)
                paths.append(path + [next_node])


def BFS_search(g, start_node, end_node):

    # convert the adjacency list format to represent the graph
    graph = graph_dic(g)

    # find the path which is also the shortest path
    result = bfs_paths(graph, start_node, end_node)

    # if there is no path available from start node to goal node, just simple return an empty list
    if not result:
        return []

    # return the founded path
    return result


def make_maze():
    vis = [[0] * MAZE_SIZE + [1] for _ in range(MAZE_SIZE)] + [[1] * (MAZE_SIZE + 1)]
    ver = [["|:"] * MAZE_SIZE + ['|'] for _ in range(MAZE_SIZE)] + [[]]
    hor = [["+-"] * MAZE_SIZE + ['+'] for _ in range(MAZE_SIZE + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+ "
            if yy == y: ver[y][max(x, xx)] = " :"
            walk(xx, yy)

    walk(randrange(MAZE_SIZE), randrange(MAZE_SIZE))

    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])

    s_temp = s
    graph = [[] for i in range(MAZE_SIZE * MAZE_SIZE)]
    for col in range(MAZE_SIZE):
        for row in range(MAZE_SIZE):
            if s_temp[(2 * row + 1) * (2 * MAZE_SIZE + 2) + (2 * col)] == " " or (
                    random() < 1 / (2 * MAZE_SIZE) and col != 0):
                graph[col + MAZE_SIZE * row].append(col - 1 + MAZE_SIZE * row)
                graph[col - 1 + MAZE_SIZE * row].append(col + MAZE_SIZE * row)

            if s_temp[(2 * row + 2) * (2 * MAZE_SIZE + 2) + (2 * col) + 1] == " " or (
                    random() < 1 / (2 * MAZE_SIZE) and row != MAZE_SIZE - 1):
                graph[col + MAZE_SIZE * row].append(col + MAZE_SIZE * (row + 1))
                graph[col + MAZE_SIZE * (row + 1)].append(col + MAZE_SIZE * row)

    return s, graph


def print_maze(g, path, players):
    s = ""
    for col in range(MAZE_SIZE): s += "+---"
    s += "+\n"

    for row in range(MAZE_SIZE):
        s += "|"
        for col in range(MAZE_SIZE):
            if row * MAZE_SIZE + col == players[0]:
                s += "👨 "
            elif row * MAZE_SIZE + col == players[1]:
                s += "🍒 "
            elif row * MAZE_SIZE + col in path:
                ind = path.index(row * MAZE_SIZE + col)
                if path[ind + 1] == row * MAZE_SIZE + col + 1:
                    s += " → "
                elif path[ind + 1] == row * MAZE_SIZE + col - 1:
                    s += " ← "
                elif path[ind + 1] == row * MAZE_SIZE + col + MAZE_SIZE:
                    s += " ↓ "
                elif path[ind + 1] == row * MAZE_SIZE + col - MAZE_SIZE:
                    s += " ↑ "
                else:
                    s += "ppp"
            else:
                s += "   "
            if (row * MAZE_SIZE + col + 1) in g[row * MAZE_SIZE + col]:
                s += " "
            else:
                s += "|"

        s += "\n+"
        for col in range(MAZE_SIZE):
            if ((row + 1) * MAZE_SIZE + col) in g[row * MAZE_SIZE + col]:
                s += "   +"
            else:
                s += "---+"
        s += "\n"

    print(s)


s, g = make_maze()
players = [0, MAZE_SIZE * MAZE_SIZE - 1]
print(g)

print("\n\n ******** PERFORMING DFS ********")
path_DFS = DFS_search(g, players[0], players[1])
print_maze(g, path_DFS, players)
print("Path length for DFS is %i" % (len(path_DFS) - 1))

print("\n\n ******** PERFORMING BFS ********")
path_BFS = BFS_search(g, players[0], players[1])
print_maze(g, path_BFS, players)
print("Path length for BFS is %i" % (len(path_BFS) - 1))
