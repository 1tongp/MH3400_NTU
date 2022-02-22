import random
import print_tree
from AVL_tree import *

# 1st step
print("\n\n ******************* 1st STEP: search node *******************")
# code that creates the same tree as in the lecture nodes on AVL trees
N54 = Node(1, None, None, 54)
N39 = Node(1, None, None, 39)
N24 = Node(1, None, None, 24)
N71 = Node(1, None, None, 71)
N45 = Node(2, N39, N54, 45)
N6 = Node(2, None, N24, 6)
N67 = Node(3, N45, N71, 67)
N33 = Node(4, N6, N67, 33)
my_AVL_tree = AVL_tree(N33)
print_tree.print_tree(my_AVL_tree)

# code that searches node 54 (in order to test the search_node function)
print("searching " + str(54) + " ... ", end="")
stack = my_AVL_tree.search_node(54)
print(stack)
if stack == []:
    print("ERROR: empty list returned by search_node")
elif stack == None:
    print("ERROR: None returned by search_node")
elif stack[-1][0] != None:
    print("found this: ", end="")
    print(stack[-1][0].key)
    print("Here is the path to find it: ")
    for i in stack: print("[" + str(i[0].key) + " , " + i[1] + "]")
    if stack[0][0].key != 33 or stack[0][1] != 'o': print("ERROR: wrong output of search_node function")
    if stack[1][0].key != 67 or stack[1][1] != 'r': print("ERROR: wrong output of search_node function")
    if stack[2][0].key != 45 or stack[2][1] != 'l': print("ERROR: wrong output of search_node function")
    if stack[3][0].key != 54 or stack[3][1] != 'r': print("ERROR: wrong output of search_node function")
else:
    print("ERROR: found nothing :-/")
print("")

# code that searches node 55 (in order to test the search_node function)
print("\nsearching " + str(55) + " ... ", end="")
stack = my_AVL_tree.search_node(55)
print(stack)

# 2nd step
print("\n\n ******************* 2nd STEP: add node *******************")
# code that adds node 62 (in order to test the add_node function)
print("adding " + str(62))
t = my_AVL_tree.add_node(62)
if t == None: print("ERROR: no node is returned from add_node function")
print_tree.print_tree(my_AVL_tree)
print("")

# 3rd step
print("\n\n ******************* 3rd STEP: remove node *******************")
# code that removes node 24 (in order to test the remove_node function)
print("removing " + str(24))
t = my_AVL_tree.remove_node(24)
if t == None: print("ERROR: no node is returned from remove_node function")
print_tree.print_tree(my_AVL_tree)
print("")

print("\n\n ******************* 3rd STEP: remove node *******************")
# code that removes node 24 (in order to test the remove_node function)
print("removing " + str(54))
t = my_AVL_tree.remove_node(54)
if t == None: print("ERROR: no node is returned from remove_node function")
print_tree.print_tree(my_AVL_tree)
print("")

# 4th step
print("\n\n ******************* 4th STEP: general test *******************")
# code that randomly adds and removes nodes in the AVL tree (to test that all is working fine)
my_AVL_tree = AVL_tree(None)
L = []
for j in range(3):
    for i in range(10):
        v = random.randint(0, 99)
        print("adding " + str(v), end="")
        if my_AVL_tree.add_node(v) != None:
            L.append(v)
        print_tree.print_tree(my_AVL_tree)

    for i in range(2):
        if len(L) > 1:
            v = random.randint(0, len(L) - 1)
        else:
            print("Empty tree, can't remove a node !")
            break
        print("removing " + str(L[v]), end="")
        if my_AVL_tree.remove_node(L[v]) != None:
            L.remove(L[v])
        print_tree.print_tree(my_AVL_tree)

# print("------- add")

# print("--------compute")
# N8 = Node(1, None, None, 8)
# N1 = Node(1, None, None, 1)
# N6 = Node(1, None, None, 6)
# N9 = Node(2, N8, None, 9)
# N12 = Node(1, None, None, 12)
# N2 = Node(2, N1, None, 2)
# N7 = Node(3, N6, N9, 7)
# N11 = Node(2, None, N12, 11)
# N3 = Node(3, N2, None, 3)
# N10 = Node(4, N7, N11, 10)
# N4 = Node(5, N3, N10, 4)
# my_AVL_tree = AVL_tree(N4)
# print_tree.print_tree(my_AVL_tree)
# print(my_AVL_tree.compute_height(N3))
#
# print("-----------right rotation")
# N4 = Node(1, None, None, 4)
# N3 = Node(2, N4, None, 3)
# N2 = Node(3, N3, None, 2)
# N5 = Node(1, None, None, 5)
# N1 = Node(4, N2, N5, 1)
# my_AVL_tree = AVL_tree(N1)
# print_tree.print_tree(my_AVL_tree)
# print(my_AVL_tree.rotation_tree(N1, N2, N3, N4))
# print_tree.print_tree(my_AVL_tree)
#
# print("-----------left rotation")
# N4 = Node(1, None, None, 4)
# N3 = Node(2, None, N4, 3)
# N2 = Node(3, None, N3, 2)
# N5 = Node(1, None, None, 5)
# N1 = Node(4, N5, N2, 1)
# my_AVL_tree = AVL_tree(N1)
# print_tree.print_tree(my_AVL_tree)
# print(my_AVL_tree.rotation_tree(N1, N2, N3, N4))
# print_tree.print_tree(my_AVL_tree)
#
# print("-----------right left rotation")
# N4 = Node(1, None, None, 4)
# N3 = Node(2, N4, None, 3)
# N2 = Node(3, None, N3, 2)
# N5 = Node(1, None, None, 5)
# N1 = Node(4, N5, N2, 1)
# my_AVL_tree = AVL_tree(N1)
# print_tree.print_tree(my_AVL_tree)
# print(my_AVL_tree.rotation_tree(N1, N2, N3, N4))
# print_tree.print_tree(my_AVL_tree)
#
# print("-----------left right rotation")
# N4 = Node(1, None, None, 4)
# N3 = Node(2, None, N4, 3)
# N2 = Node(3, N3, None, 2)
# N5 = Node(1, None, None, 5)
# N1 = Node(4, N2, N5, 1)
# my_AVL_tree = AVL_tree(N1)
# print_tree.print_tree(my_AVL_tree)
# print(my_AVL_tree.rotation_tree(N1, N2, N3, N4))
# print_tree.print_tree(my_AVL_tree)

# print("-----------Q3")
# N4 = Node(1, None, None, 4)
# N3 = Node(2, None, N4, 3)
# N2 = Node(3, N3, None, 2)
# # N5 = Node(1, None, None, 5)
# # N1 = Node(4, N2, N5, 1)
# my_AVL_tree = AVL_tree(N2)
# print_tree.print_tree(my_AVL_tree)
# # print(my_AVL_tree.rotation_tree(None,N2,N3,N4))
# print(my_AVL_tree.backtrack_height_from_add([[2, 'o'], [3, 'l'], [4, 'r']]))
# print_tree.print_tree(my_AVL_tree)

print("--------remove")
N27 = Node(1, None, None, 27)
N50 = Node(1, None, None, 50)
N81 = Node(1, None, None, 81)
N10 = Node(2, None, N27, 10)
N47 = Node(2, None, N50, 47)
N71 = Node(1, None, None, 71)
N96 = Node(2, N81, None, 96)
N39 = Node(3, N10, N47, 39)
N75 = Node(3, N71, N96, 75)
N68 = Node(4, N39, N75, 68)
my_AVL_tree = AVL_tree(N68)
print_tree.print_tree(my_AVL_tree)
print(my_AVL_tree.remove_node(96))
print_tree.print_tree(my_AVL_tree)

# print("--------add")
# N16 = Node(1, None, None, 16)
# # N91 = Node(1, None, None, 91)
# N0 = Node(1, None, None, 1)
# N12 = Node(1, None, None, 12)
# N31 = Node(2, N16, None, 31)
# N34 = Node(1, None, None, 34)
# # N62 = Node(1, None, None, 62)
# # N86 = Node(1, None, None, 86)
# # N99 = Node(2, N91, None, 91)
# N9 = Node(2, N0, N12, 9)
# N32 = Node(3, N31, N34, 32)
# N13 = Node(4, N9, N32, 13)
# N48 = Node(5, N13, None, 48)
# my_AVL_tree =
