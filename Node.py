from copy import deepcopy
import random

class Node:

    def __init__(self, pred, board, action):
        self.pred = pred
        self.children = []
        self.wins = 0
        self.visits = 0
        self.board = board
        self.action = action
        if pred is None:
            self.depth = 0
        else:
            self.depth = pred.depth + 1
        self.untriedActions = self.board.checkActions()
        random.shuffle(self.untriedActions)

    # used for min heap
    def __lt__(self, other):
        return self.total < other.total

    # hashes based on board
    def __hash__(self):
        return hash(self.board)

    def __str__(self):
        myString = "move: " + str(self.action) + '\n wins:' + str(self.wins) + '\n visits:' + str(self.visits) + '\n depth:' + str(self.depth)
        return myString

    # randomly expands an action to return a child node
    def expand(self):
        action = self.untriedActions.pop()
        newBoard = deepcopy(self.board)
        newBoard.doAction(action)
        child = Node(self, newBoard, action)
        self.children.append(child)
        return child
