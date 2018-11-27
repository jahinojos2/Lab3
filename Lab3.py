import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 19:27:26 2018
@author: jaimeahinojos
"""


class Node:  # creates object with the set ID and next pointer
    def __init__(self, word, cd):

        self.key = word
        self.code = cd
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    def get_balance(self):
        # Get current height of left subtree, or -1 if None

        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        # Get current height of right subtree, or -1 if None

        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        # Calculate the balance factor.
        return left_height - right_height

    def update_height(self):

        # Get current height of left subtree, or -1 if None
        left_height = -1

        if self.left is not None:
            left_height = self.left.height

        # Get current height of right subtree, or -1 if None
        right_height = -1

        if self.right is not None:
            right_height = self.right.height

        # Assign self.height with calculated node height.
        self.height = max(left_height, right_height) + 1

    def set_child(self, which_child, child):

        # Ensure which_child is properly assigned.
        if which_child != "left" and which_child != "right":
            return False

        # Assign the left or right data member.
        if which_child == "left":
            self.left = child

        else:
            self.right = child

        # Assign the parent data member of the new child,
        # if the child is not None.
        if child is not None:
            child.parent = self

        # Update the node's height, since the subtree's structure
        # may have changed.
        self.update_height()
        return True

    # Replace a current child with a new child. Determines if
    # the current child is on the left or right, and calls
    # set_child() with the new node appropriately.
    # Returns True if the new child is assigned, False otherwise.
    def replace_child(self, current_child, new_child):

        if self.left is current_child:
            return self.set_child("left", new_child)

        elif self.right is current_child:
            return self.set_child("right", new_child)

        # If neither of the above cases applied, then the new child
        # could not be attached to this node.
        return False


class AVLTree:
    # Constructor to create an empty AVLTree. There is only
    # one data member, the tree's root Node, and it starts
    # out as None.
    def __init__(self):
        self.root = None

    # Performs a left rotation at the given node. Returns the
    # new root of the subtree.
    def rotate_left(self, node):
        # Define a convenience pointer to the right child of the
        # left child.
        right_left_child = node.right.left

        # Step 1 - the right child moves up to the node's position.
        # This detaches node from the tree, but it will be reattached
        # later.

        if node.parent is not None:
            node.parent.replace_child(node, node.right)

        else:  # node is root
            self.root = node.right
            self.root.parent = None

        # Step 2 - the node becomes the left child of what used
        # to be its right child, but is now its parent. This will
        # detach right_left_child from the tree.
        node.right.set_child('left', node)

        # Step 3 - reattach right_left_child as the right child of node.
        node.set_child('right', right_left_child)

        return node.parent

    # Performs a right rotation at the given node. Returns the
    # subtree's new root.

    def rotate_right(self, node):
        # Define a convenience pointer to the left child of the
        # right child.

        left_right_child = node.left.right

        # Step 1 - the left child moves up to the node's position.
        # This detaches node from the tree, but it will be reattached
        # later.

        if node.parent is not None:
            node.parent.replace_child(node, node.left)

        else:  # node is root
            self.root = node.left
            self.root.parent = None

        # Step 2 - the node becomes the right child of what used
        # to be its left child, but is now its parent. This will
        # detach left_right_child from the tree.
        node.left.set_child('right', node)

        # Step 3 - reattach left_right_child as the left child of node.
        node.set_child('left', left_right_child)

        return node.parent

    # Updates the given node's height and rebalances the subtree if
    # the balancing factor is now -2 or +2. Rebalancing is done by
    # performing a rotation. Returns the subtree's new root if
    # a rotation occurred, or the node if no rebalancing was required.
    def rebalance(self, node):

        # First update the height of this node.
        node.update_height()

        # Check for an imbalance.
        if node.get_balance() == -2:

            # The subtree is too big to the right.
            if node.right.get_balance() == 1:
                # Double rotation case. First do a right rotation
                # on the right child.
                self.rotate_right(node.right)

            # A left rotation will now make the subtree balanced.
            return self.rotate_left(node)

        elif node.get_balance() == 2:

            # The subtree is too big to the left
            if node.left.get_balance() == -1:
                # Double rotation case. First do a left rotation
                # on the left child.
                self.rotate_left(node.left)

            # A right rotation will now make the subtree balanced.
            return self.rotate_right(node)

        # No imbalance, so just return the original node.
        return node

    def insert(self, node):

        # Special case: if the tree is empty, just set the root to
        # the new node.

        if self.root is None:
            self.root = node
            node.parent = None

        else:
            # Step 1 - do a regular binary search tree insert.
            current_node = self.root

            while current_node is not None:
                # Choose to go left or right
                ascii1 = 1
                ascii2 = 1

                for i in range(len(node.key)):
                    ascii1 = ascii1 * ord(node.key[i])

                for i in range(len(current_node.key)):
                    ascii2 = ascii2 * ord(current_node.key[i])
                ascii1 = ascii1 / len(node.key)
                ascii2 = ascii2 / len(current_node.key)

                if ascii1 < ascii2:
                    # Go left. If left child is None, insert the new
                    # node here.

                    if current_node.left is None:
                        current_node.left = node
                        node.parent = current_node
                        current_node = None

                    else:
                        # Go left and do the loop again.
                        current_node = current_node.left

                else:
                    # Go right. If the right child is None, insert the
                    # new node here.

                    if current_node.right is None:
                        current_node.right = node
                        node.parent = current_node
                        current_node = None

                    else:
                        # Go right and do the loop again.
                        current_node = current_node.right

            # Step 2 - Rebalance along a path from the new node's parent up
            # to the root.

            node = node.parent

            while node is not None:
                self.rebalance(node)
                node = node.parent

    def remove_node(self, node):
        # Base case:
        if node is None:
            return False

        # Parent needed for rebalancing.
        parent = node.parent

        # Case 1: Internal node with 2 children
        if node.left is not None and node.right is not None:
            # Find successor

            successor_node = node.right

            while successor_node.left != None:
                successor_node = successor_node.left

            # Copy the value from the node
            node.key = successor_node.key

            # Recursively remove successor
            self.remove_node(successor_node)

            # Nothing left to do since the recursive call will have rebalanced
            return True

        # Case 2: Root node (with 1 or 0 children)
        elif node is self.root:

            if node.left is not None:
                self.root = node.left

            else:
                self.root = node.right

            if self.root is not None:
                self.root.parent = None

            return True

        # Case 3: Internal with left child only
        elif node.left is not None:
            parent.replace_child(node, node.left)

        # Case 4: Internal with right child only OR leaf
        else:
            parent.replace_child(node, node.right)

        # node is gone. Anything that was below node that has persisted is already correctly
        # balanced, but ancestors of node may need rebalancing.
        node = parent

        while node is not None:
            self.rebalance(node)
            node = node.parent

        return True


class RBTNode:
    def __init__(self, key, cd, parent, is_red=False, left=None, right=None):
        self.key = key
        self.code = cd
        self.left = left
        self.right = right
        self.parent = parent
        self.height = 0

        if is_red:
            self.color = "red"

        else:
            self.color = "black"

    # Returns true if both child nodes are black. A child set to None is considered
    # to be black.
    def are_both_children_black(self):

        if self.left != None and self.left.is_red():
            return False

        if self.right != None and self.right.is_red():
            return False
        return True

    def count(self):
        count = 1

        if self.left != None:
            count = count + self.left.count()

        if self.right != None:
            count = count + self.right.count()

        return count
    def update_height(self):

        # Get current height of left subtree, or -1 if None
        left_height = -1

        if self.left is not None:
            left_height = self.left.height

        # Get current height of right subtree, or -1 if None
        right_height = -1

        if self.right is not None:
            right_height = self.right.height

        # Assign self.height with calculated node height.
        self.height = max(left_height, right_height) + 1

    # Returns the grandparent of this node
    def get_grandparent(self):

        if self.parent is None:
            return None

        return self.parent.parent

    # Gets this node's predecessor from the left child subtree
    # Precondition: This node's left child is not None
    def get_predecessor(self):

        node = self.left

        while node.right is not None:
            node = node.right

        return node

    # Returns this node's sibling, or None if this node does not have a sibling
    def get_sibling(self):

        if self.parent is not None:

            if self is self.parent.left:
                return self.parent.right

            return self.parent.left

        return None

    # Returns the uncle of this node
    def get_uncle(self):

        grandparent = self.get_grandparent()

        if grandparent is None:
            return None

        if grandparent.left is self.parent:
            return grandparent.right

        return grandparent.left

    # Returns True if this node is black, False otherwise
    def is_black(self):

        return self.color == "black"

    # Returns True if this node is red, False otherwise
    def is_red(self):

        return self.color == "red"

    # Replaces one of this node's children with a new child
    def replace_child(self, current_child, new_child):

        if self.left is current_child:
            return self.set_child("left", new_child)

        elif self.right is current_child:
            return self.set_child("right", new_child)

        return False

    # Sets either the left or right child of this node
    def set_child(self, which_child, child):

        if which_child != "left" and which_child != "right":
            return False

        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child != None:
            child.parent = self

        self.update_height()
        return True


class RedBlackTree:
    def __init__(self):
        self.root = None

    def __len__(self):
        if self.root is None:
            return 0
        return self.root.count()

    def insert(self, key, cd):

        new_node = RBTNode(key, cd, None, True, None, None)

        self.insert_node(new_node)


    def insert_node(self, node):
        # Begin with normal BST insertion
        if self.root is None:
            # Special case for root
            self.root = node

        else:

            current_node = self.root

            while current_node is not None:
                ascii1 = 1
                ascii2 = 1

                for i in range(len(node.key)):
                    ascii1 = ascii1 * ord(node.key[i])

                for i in range(len(current_node.key)):
                    ascii2 = ascii2 * ord(current_node.key[i])

                ascii1 = ascii1 / len(node.key)
                ascii2 = ascii2 / len(current_node.key)

                if ascii1 < ascii2:

                    if current_node.left is None:
                        current_node.set_child("left", node)
                        break

                    else:
                        current_node = current_node.left

                else:

                    if current_node.right is None:
                        current_node.set_child("right", node)
                        break

                    else:
                        current_node = current_node.right

        # Color the node red
        node.color = "red"

        # Balance
        self.insertion_balance(node)

    def insertion_balance(self, node):

        node.update_height()
        # If node is the tree's root, then color node black and return

        if node.parent is None:
            node.color = "black"
            return

        # If parent is black, then return without any alterations
        if node.parent.is_black():
            return

        # References to parent, grandparent, and uncle are needed for remaining operations
        parent = node.parent

        grandparent = node.get_grandparent()

        uncle = node.get_uncle()

        # If parent and uncle are both red, then color parent and uncle black, color grandparent
        # red, recursively balance  grandparent, then return
        if uncle is not None and uncle.is_red():
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        # If node is parent's right child and parent is grandparent's left child, then rotate left
        # at parent, update node and parent to point to parent and grandparent, respectively
        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent
        # Else if node is parent's left child and parent is grandparent's right child, then rotate
        # right at parent, update node and parent to point to parent and grandparent, respectively
        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent

        # Color parent black and grandparent red
        parent.color = "black"
        grandparent.color = "red"

        # If node is parent's left child, then rotate right at grandparent, otherwise rotate left
        # at grandparent
        if node is parent.left:
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)

    def rotate_left(self, node):

        right_left_child = node.right.left

        if node.parent != None:
            node.parent.replace_child(node, node.right)

        else:  # node is root
            self.root = node.right
            self.root.parent = None

        node.right.set_child("left", node)
        node.set_child("right", right_left_child)

    def rotate_right(self, node):

        left_right_child = node.left.right

        if node.parent != None:
            node.parent.replace_child(node, node.left)

        else:  # node is root
            self.root = node.left
            self.root.parent = None

        node.left.set_child("right", node)
        node.set_child("left", left_right_child)


def pBST(node, f):

    if node:
        pBST(node.left, f)
        f.write(node.key + '\n')
        pBST(node.right, f)


def numNodes(node):

    if node is None:
        return 0
    return 1 + numNodes(node.left) + numNodes(node.right)


def patdepth(node, f, num):

    if node is None:
        return

    if num > node.height:
        print('BST does not have that depth')
        return

    if num == 0:
        f.write(node.key + '\n')
        return

    else:
        patdepth(node.left, f, num - 1)
        patdepth(node.right, f, num - 1)


def calculate_similarity(vector1, vector2):

    if vector1 is None or vector2 is None:
        print('Cannot proceed with an empty set.')
        return None

    array1 = np.array(vector1, dtype=float)
    array2 = np.array(vector2, dtype=float)

    array1 = array1.reshape(1,-1)
    array2 = array2.reshape(1,-1)

    return cosine_similarity(array1,array2)



def readFile(a):

    with open(a) as f:
        list = f.read().splitlines()

    return list

def search_bst(node, key):

    ascii2 = 1
    temp = node

    for i in range(len(key)):
        ascii2 = ascii2 * ord(key[i])

    ascii2 = ascii2/len(key)

    while temp is not None:
        ascii1=1

        for i in range(len(temp.key)):
            ascii1 = ascii1 * ord(temp.key[i])

        ascii1 = ascii1/len(temp.key)

        if temp.key == key:
            return temp.code

        elif ascii1 < ascii2:
            temp = temp.right

        else:
            temp = temp.left



def read_and_match(node):

    with open('match_words.txt') as f:

        list = f.read().splitlines()

    for i in range(len(list)):

        tempArray = list[i].split(' ')
        word1 = search_bst(node, tempArray[0])
        word2 = search_bst(node, tempArray[1])
        word_sim = calculate_similarity(word1,word2)

        print(tempArray[0]+' '+tempArray[1]+' '+str(word_sim))


def createAVL(list):

    avl = AVLTree()

    for i in range(len(list)):

        tempArray = list[i].split(' ')
        testWord = tempArray[0]

        if testWord[0].isalpha():
            newarray = []

            for j in range(len(tempArray)-1):
                newarray.append(tempArray[j+1])

            node = Node(testWord, newarray)
            avl.insert(node)

    nextStep(avl)


def createRedBlack(list):

    node = RedBlackTree()

    for i in range(len(list)):

        tempArray = list[i].split(' ')
        testWord = tempArray[0]

        if testWord[0].isalpha():
            newarray = []

            for j in range(len(tempArray)-1):
                newarray.append(tempArray[j+1])
            node.insert(testWord, newarray)

    nextStep(node)

def nextStep(node):#next step serves as a menu to continue after the Binary Search Tree is Created

    print('What would you like to do? (Enter Number)')
    print('1. Count the number of Nodes in BST ')
    print('2. Get the height of BST')
    print('3. Print BST to a file in ascending order')
    print('4. Print BST at certain Depth into file')
    print('5. Read Pair File and find similarity')
    print('6. Exit')

    answer = ''
    answer = input(str('Enter Number: '))

    if answer == 1:
        number = numNodes(node.root)
        print('Number of nodes in BST is: '+str(number))
        print
        nextStep(node)

    elif answer == 2:
        print(node.root.height)
        nextStep(node)

    elif answer == 3:
        f = open("writeFile.txt", "w+")
        pBST(node.root, f)
        nextStep(node)

    elif answer == 4:
        f = open("writeFile.txt", "w+")
        num = int(input(str('Enter Depth of tree you want to print: ')))
        patdepth(node.root, f, num)
        nextStep(node)

    elif answer == 5:
        read_and_match(node.root)

    elif answer == 6:
        print('goodbye')
        return

    else:
        print('Invalid Input')
        nextStep(node)


def main(list):#main caller to initiate if the Tree will be created as a AVL or Red Black Tree
    answer = input(str('To use an AVL tree type 1 to use a Red Black Tree type 2: '))
    i = 0
    while i != 3:
        if answer == 1:
            createAVL(list)
            break
        elif answer ==  2:
            createRedBlack(list)
            break
        else:
            print('Invalid Answer')
            answer = input(str('To use an AVL tree type 1 to use a Red Black Tree type 2: '))
            i += 1


text1 = 'glove.6B.50d.txt'
list = readFile(text1)
main(list)
