"""
the Game class
"""
from board import Board

class Difficulty(object):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

difficulties_available = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]

class Dimension(object):
    def __init__(self, height, width, mines):
        self.height = height
        self.width = width
        self.mines = mines

dimensions = {
    Difficulty.EASY: Dimension(8, 8, 10),
    Difficulty.MEDIUM: Dimension(16, 16, 40),
    Difficulty.HARD: Dimension(24, 24, 99)
}


class Game(object):
    name = None
    dimension = None
    @classmethod
    def start(cls):
        while cls.name is None:
            name = raw_input("What is your name?\n")
            if len(name) != 0:
                cls.name = name
            else:
                print "Name cannot be empty."
                continue
        while cls.dimension is None:
            difficulty = raw_input(
                "choose your difficulty:\n"
                "[easy (8x8, 10), medium (16x16, 40), hard (24x24, 99), custom]\n"
            ).lower()
            if difficulty != 'custom':
                if difficulty not in difficulties_available:
                    print("Invalid difficulty option."
                          "Please choose from "
                          "[easy (8x8, 10), medium (16x16, 40), hard (24x24, 99), custom]\n")
                    continue
                cls.dimension = dimensions[difficulty]
            else:
                dimension_input = raw_input(
                    "Please type height, width and number of mines separated by space. For example, '3 4 10'"
                    "means a 3x4 board with 10 mines: \n"
                )
                dimension = dimension_input.split()
                if len(dimension) != 3:
                    print("Invalid number of parameters given.\n")
                    continue
                try:
                    height = int(dimension[0])
                    width = int(dimension[1])
                    mines = int(dimension[2])
                except ValueError:
                    print("Non-integer dimension given.\n")
                    continue
                if height < 1 or width < 1 or mines < 1:
                    print("Please generate a board that is least 1x1 with at least 1 mine.\n")
                    continue
                cls.dimension = Dimension(height, width, mines)
        cls.board = Board(cls.dimension.height, cls.dimension.width, cls.dimension.mines)
        cls.board.display()
