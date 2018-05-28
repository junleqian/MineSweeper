"""
Class definition of of RandomSet

A set that is required to have:
    O(1) pop a random item
    O(1) insert
    O(1) search

Note: Python set() 's "random" pop method
is "arbitary" instead of random, which means you just
can't depend on the pop order instead of guaranteeing
randomness. The "arbitary" behavior isn't what we want
in this game.
Try it. If you keep reinstantiating a Python set with
the same list of items, the pop order is exactly
the same every time. Therefore, we write our own
random set class.
"""
from __future__ import print_function
from random import randint


class BoardGrid(object):
    def __init__(self, hidden, value):
        self.hidden = hidden
        self.value = value


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
    def __init__(self, height, width, num_of_mines):
        num_of_mines = min(height*width, num_of_mines)

        # initialize the board with all zeros, reprenting the mine count
        # use 'M' to represent a mine
        # don't do [[0]*width]*height, as Python will copy only the references
        # for the internal lists, which cause every row change to to all rows.
        self.board = [ [ BoardGrid(hidden=True, value=0) for _ in xrange(0, width) ] for _ in xrange(0, height) ]

        self.has_lost = False

        self.grounds = height * width - num_of_mines

        # initialize a random set and add all coordinates into the random set
        # O(N), N is the number of grids on the board
        random_set = RandomSet()
        for i in xrange(0, height):
            for j in xrange(0, width):
                random_set.add((i, j))

        # O(K) if we need K mines
        while num_of_mines > 0:
            # O(1) pop
            i,  j = random_set.pop()
            self.board[i][j] = BoardGrid(hidden=True, value='M')
            # increase mine counts surronding the current mine
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for direction in directions:
                x, y = i + direction[0], j + direction[1]
                if x >= 0 and y >= 0 and x < height and y < width and self.board[x][y].value != 'M':
                    # if it is a valid grid and it is not a mine
                    self.board[x][y].value += 1
            num_of_mines -= 1

    def __repr__(self):
        result = ""
        for i in xrange(0, len(self.board)):
            max_digits = len(str(len(self.board)))
            for j in xrange(0, 1+max_digits+4*len(self.board[0])):
                result += "-"
            result += "\n"
            result += "{}".format(i+1).zfill(max_digits)
            for j in xrange(0, len(self.board[0])):
                if self.board[i][j].hidden:
                    grid = " "
                else:
                    grid = self.board[i][j].value
                result += "| {} ".format(grid)
            result += "|\n"
        for i in xrange(0, 1+max_digits+4*len(self.board[0])):
            result += "-"
        return result


    def display(self):
        print(self)


    def win(self):
        if self.grounds == 0:
            self.show_all_mines()
            return True
        return False

    def lost(self):
        return self.has_lost

    def show_all_mines(self):
        for i in xrange(len(self.board)):
            for j in xrange(len(self.board[0])):
                if self.board[i][j].value in set(['M', 'B']):
                    self.board[i][j].hidden = False

    def step_on(self, row, column):
        if self.board[row][column].hidden == False:
            return
        if self.board[row][column].value == 'M':
            self.board[row][column].value = 'B'
            self.show_all_mines()
            self.has_lost = True
            return
        self.sweep(row, column)

    def sweep(self, row, column):
        if self.board[row][column].value == 'M':
            return

        self.board[row][column].hidden = False
        self.grounds -= 1

        if self.board[row][column].value != 0:
            return

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1) ]
        for direction in directions:
            new_row = row + direction[0]
            new_col = column + direction[1]
            if (new_row >= 0 and new_col >= 0 and new_row < len(self.board) and new_col < len(self.board[0]) and
                    self.board[new_row][new_col].hidden):
                    self.sweep(new_row, new_col)
