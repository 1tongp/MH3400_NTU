# class that represents a tree node
import copy


class Node:
    def __init__(self, height, left, right, key):
        self.height = height
        self.left = left
        self.right = right
        self.key = key


# class that represents an AVL tree
class AVL_tree:
    find_all_nodes = []
    paths = []

    def __init__(self, root):
        self.root = root

    # method that adds a node into the AVL tree
    def search_node(self, value):
        stack = []
        t = self.root
        stack.append([t, 'o'])
        while True:
            if t == None: return stack
            if value > t.key:
                t = t.right
                stack.append([t, 'r'])
            elif value < t.key:
                t = t.left
                stack.append([t, 'l'])
            else:
                return stack

    # method that computes the height of a node t and also detects unbalanced between the left and right childs the
    def compute_height(self, t):
        """
        mathematical function to calculate the node's balance factor is right child's balance factor minus left child's
        balance factor
        1. for a node with no children, the balance factor is 0
        2. for a node with one level of right child but no left child, the balance factor is -1
        3. for a node with one level of left child but no right child, the balance factor is 1
        :param t: node that wishes to check if it is balanced
        :return: True for unbalanced, False for balanced
        """
        if t.right is not None and t.left is not None:
            balance_factor = t.right.height - t.left.height
        elif t.right is None and t.left is None:
            balance_factor = 0
        elif t.right is None and t.left is not None:
            balance_factor = 0 - t.left.height
        elif t.right is not None and t.left is None:
            balance_factor = t.right.height - 0

        if balance_factor == -1 or balance_factor == 1 or balance_factor == 0:
            return False
        return True

    # function to update the height for each node after the rotation process
    def height_update_strategy(self, t):
        if t is not None:
            if t.right is not None and t.left is not None:
                t.height = max(t.right.height, t.left.height) + 1
            elif t.right is None and t.left is not None:
                t.height = t.left.height + 1
            elif t.right is not None and t.left is None:
                t.height = t.right.height + 1
            else:
                t.height = 1

    # function to update the child for ancestor node when rotate
    def ancestor_child_update(self, ancestor, ori_child, new_child):
        if ancestor is not None:
            if ancestor.right == ori_child:
                ancestor.right = new_child
            else:
                ancestor.left = new_child
        else:
            self.root = new_child

    # function to apply right rotation for zig-zig case
    def zig_zig_right(self, a, z, y, x):

        # update the child for ancestor node a
        self.ancestor_child_update(a, z, y)

        # update new child for node z
        z.left = y.right

        # update new child for node y
        y.right = z

        # update the new height for node z
        self.height_update_strategy(z)

        # update the new height for node y
        y.height = max(x.height, z.height) + 1

        # update the new height for node a
        self.height_update_strategy(a)

    # function to apply left rotation for zig-zig case
    def zig_zig_left(self, a, z, y, x):

        # update the child for ancestor node a
        self.ancestor_child_update(a, z, y)

        # update the child node for z node
        z.right = y.left

        # update the child node for y node
        y.left = z

        # update the new height for node z
        self.height_update_strategy(z)

        # update the new height for node y
        y.height = max(z.height, x.height) + 1

        # update the new height for node a
        self.height_update_strategy(a)

    # function to apply the right left rotation for zig-zag case
    def zig_zag_right_left(self, a, z, y, x):

        # update the child for ancestor node a
        self.ancestor_child_update(a, z, x)

        # update new child for node y
        y.left = x.right

        # update new child for node z
        z.right = x.left

        # update new child for node x
        x.right = y
        x.left = z

        # update new height for node y
        self.height_update_strategy(y)

        # update new height for node z
        self.height_update_strategy(z)

        # update new height for node x
        self.height_update_strategy(x)

        # update new height for node a
        self.height_update_strategy(a)

    # function to apply the left right rotation for zig-zag case
    def zig_zag_left_right(self, a, z, y, x):

        # update the child for ancestor node a
        self.ancestor_child_update(a, z, x)

        # update new child for node y
        y.right = x.left

        # update new child for node z
        z.left = x.right

        # update new child for node x
        x.left = y
        x.right = z

        # update new height for node z
        self.height_update_strategy(z)

        # update new height for node y
        self.height_update_strategy(y)

        # update new height for node x
        self.height_update_strategy(x)

        # update new height for node a
        self.height_update_strategy(a)

    # method that applies a rotation correction
    def rotation_tree(self, a, z, y, x):
        # case 1: zig-zig right rotation
        if z.left == y and y.left == x:
            self.zig_zig_right(a, z, y, x)

        # case 2: zig-zig left rotation
        elif z.right == y and y.right == x:
            self.zig_zig_left(a, z, y, x)

        # case 3: zig-zag right left rotation
        elif z.right == y and y.left == x:
            self.zig_zag_right_left(a, z, y, x)

        # case 4: zig zag left right rotation
        elif z.left == y and y.right == x:
            self.zig_zag_left_right(a, z, y, x)

    # function to find the deepest node of a tree, and return the path of it/them
    def find_deepest_leaf_node(self):
        self.find_all_nodes = []
        self.find_all_node(self.root)
        max_height = 0
        deep_node_path = []
        for i in range(len(self.find_all_nodes)):
            path = self.search_node(self.find_all_nodes[i].key)
            if len(path) > max_height:
                max_height = len(path)

        for i in range(len(self.find_all_nodes)):
            path = self.search_node(self.find_all_nodes[i].key)
            if len(path) == max_height:
                deep_node_path.append(path)
        return deep_node_path

    # method that will look for possible unbalances in the tree after a node has been added
    def backtrack_height_from_add(self, path):

        # reverse the list of node to check if there exist an unbalanced node
        for i in reversed(range(len(path) - 2)):

            # if the node has an unbalanced balance factor, then we need to rotate it
            if self.compute_height(path[i][0]):
                z = path[i][0]
                y = path[i + 1][0]
                x = path[i + 2][0]
                if i - 1 < 0:
                    a = None
                else:
                    a = path[i - 1][0]
                self.rotation_tree(a, z, y, x)

    # method that will look for possible unbalances in the tree after a node has been removed
    def backtrack_height_from_remove(self, path):

        # reverse the list of node to check if there exist an unbalanced node
        for i in reversed(range(len(path) - 2)):
            if self.compute_height(path[i][0]):
                z = path[i][0]
                y = path[i + 1][0]
                x = path[i + 2][0]
                if i - 1 < 0:
                    a = None
                else:
                    a = path[i - 1][0]
                self.rotation_tree(a, z, y, x)

            # if the length of the path is less or equal to two, check if the root is balance

        for i in reversed(range(len(path))):
            if self.compute_height(path[i][0]):
                z = path[i][0]

                # find y, y is one of the child node of z, and y has the higher height.
                if z.right is not None and z.left is not None:
                    if z.right.height > z.left.height:
                        y = z.right
                    elif z.right.height < z.left.height:
                        y = z.left
                    else:
                        y = z.right
                elif z.right is None and z.left is not None:
                    y = z.left
                elif z.right is not None and z.left is None:
                    y = z.right

                # find x, x is one of the child node of y, and x has the higher height
                if y.right is not None and y.left is not None:
                    if y.right.height > y.left.height:
                        x = y.right
                    elif y.right.height < y.left.height:
                        x = y.left
                    else:
                        x = y.right
                elif y.right is None and y.left is not None:
                    x = y.left
                elif y.right is not None and y.left is None:
                    x = y.right

                # rotate the tree
                if i - 1 < 0:
                    a = None
                else:
                    a = path[i - 1][0]
                self.rotation_tree(a, z, y, x)


    # method that adds a node into the AVL tree
    def add_node(self, value):
        new_node = Node(1, None, None, value)
        path = self.search_node(value)

        # create a new tree
        if len(path) == 0:
            self.root = new_node
            return new_node

        elif path[0][0] is None:
            self.root = new_node
            return new_node

        # if already exists this value, do nothing and then return None
        if path[len(path) - 1][0] is not None:
            return None

        path[len(path) - 1][0] = new_node
        add_direction = path[len(path) - 1][1]
        ancestor = path[len(path) - 2][0]
        if add_direction == 'r':
            ancestor.right = new_node
        else:
            ancestor.left = new_node

        # adjust the height of each node
        for i in reversed(range(len(path))):
            self.height_update_strategy(path[i][0])

        # rotate the tree if appropriate
        self.backtrack_height_from_add(path)

        # adjust the height of each node
        for i in reversed(range(len(path))):
            self.height_update_strategy(path[i][0])

        # loop through the deepest path to check if the tree is a Balanced tree
        path_list = self.find_deepest_leaf_node()
        z = None
        y = None
        x = None
        for i in range(len(path_list)):
            for j in reversed(range(len(path_list[i]) - 2)):
                if self.compute_height(path_list[i][j][0]):
                    z = path_list[i][j][0]
                    y = path_list[i][j + 1][0]
                    x = path_list[i][j + 2][0]
                # find a
                if j - 1 >= 0:
                    a = path_list[i][j - 1][0]
                else:
                    a = None
                if z and y and x:
                    self.rotation_tree(a, z, y, x)

        return new_node

    # function to find all children from node t
    def find_all_node(self, t):

        if t.right:
            self.find_all_nodes.append(t.right)
            self.find_all_node(t.right)

        if t.left:
            self.find_all_nodes.append(t.left)
            self.find_all_node(t.left)
        return self.find_all_nodes

    # method that removes a node from the AVL tree
    def remove_node(self, value):
        path = self.search_node(value)
        removed_node = path[len(path) - 1][0]

        # if there is no node to remove
        if len(path) == 0:
            return None
        if path[len(path) - 1][0] is None:
            return None

        # remove the node, if the node is not the root
        if len(path) > 1:
            sub_ancestor = path[len(path) - 2][0]
            remove_direction = path[len(path) - 1][1]
            if remove_direction == 'r':
                sub_ancestor.right = None
            else:
                sub_ancestor.left = None

            # adjust the height for each node
            for i in reversed(range(len(path[0: len(path) - 1]))):
                self.height_update_strategy(path[i][0])

            # rotate the tree to the balance tree before adding remaining nodes
            self.backtrack_height_from_remove(path[0:len(path) - 1])

        # find the nodes that need to add back to the tree after a specific node has been removed
        self.find_all_nodes = []
        add_nodes = self.find_all_node(removed_node)

        # remove the node, if the node is the root of the tree
        if len(path) == 1:
            self.root = None
        for i in range(len(add_nodes)):
            self.add_node(add_nodes[i].key)
        self.find_all_nodes = []

        return removed_node
