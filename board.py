"""
Class definition of of RandomSet

A set that is required to have:
    O(1) pop a random item
    O(1) insert
    O(1) search

Note: Python set() 's "random" pop method
has a similar implementation in C.
"""
from __future__ import print_function
from random import randint

class RandomSet(object):
    def __init__(self):
        self.item_set = set()
        self.item_list = []

    # override len function O(1)
    def __len__(self):
        return len(self.item_set)

    def pop(self):
        # if no item is in the random set
        if len(self.item_set) == 0:
            # return NULL
            return None

        # decide a random index for the item to pop
        # it's O(1) to get length from a Python set
        item_index = randint(0, len(self.item_set)-1)

        # store the item
        item = self.item_list[item_index]

        # remove item from the set
        self.item_set.remove(item)
        # swap the list item to the end of the list, O(1)
        self.item_list[item_index] = self.item_list[-1]
        self.item_list[-1] = item
        # pop it from the list O(1)
        self.item_list.pop()

        return item

    def add(self, item):
        # Both of the list append and set add operations
        # are O(1)
        self.item_list.append(item)
        self.item_set.add(item)

    # override __contains__ to impelment the search
    # so that we can use the "in" operator for this class.
    def __contains__(self, item):
        # set lookup is O(1)
        if item in self.item_set:
            return True
        return False


"""
Class definition of the mine board
"""
class Board(object):
    def __init__(self, height, width, NumOfMines):
        NumOfMines = min(height*width, NumOfMines)

        # initialize the board with all zeros, reprenting the mine count
        # use 'M' to represent a mine
        # don't do [[0]*width]*height, as Python will copy only the references
        # for the internal lists, which cause every row change to to all rows.
        self.board = [ [ 0 for _ in xrange(0, width) ] for _ in xrange(0, height) ]

        # initialize a random set and add all coordinates into the random set
        # O(N), N is the number of grids on the board
        random_set = RandomSet()
        for i in xrange(0, height):
            for j in xrange(0, width):
                random_set.add((i, j))

        # O(K) if we need K mines
        while NumOfMines > 0:
            # O(1) pop
            i,  j = random_set.pop()
            self.board[i][j] = 'M'
            # increase mine counts surronding the current mine
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for direction in directions:
                x, y = i + direction[0], j + direction[1]
                if x >= 0 and y >= 0 and x < height and y < width and self.board[x][y] != 'M':
                    # if it is a valid grid and it is not a mine
                    self.board[x][y] += 1
            NumOfMines -= 1

    def __repr__(self):
        result = ""
        for i in xrange(0, len(self.board)):
            for j in xrange(0, 1+2*len(self.board[0])):
                result += "-"
            result += "\n"
            for j in xrange(0, len(self.board[0])):
                result += "|{}".format(self.board[i][j])
            result += "|\n"
        for i in xrange(0, 1+2*len(self.board[0])):
            result += "-"
        result += "\n"
        return result

    def display(self):
        print(self)
