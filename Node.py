from copy import deepcopy

class Node:

    def __init__(self, pred, wins, visits, board, action):
        self.pred = pred
        self.children = []
        self.wins = wins
        self.visits = visits
        self.board = board
        self.action = action

    # used for min heap
    def __lt__(self, other):
        return self.total < other.total

    # hashes based on board
    def __hash__(self):
        return hash(self.board)

    def __str__(self):
        myString = str(self.board) + "move: " + str(self.move) + "\ncost: "
        + str(self.cost) + "\nest: " + str(self.total - self.cost) + "\ntotal: "
        + str(self.total)
        return myString

    # returns a list of child nodes as a result of making all possible actions
    def expand(self):
        actions = self.board.checkActions()
        for action in actions:
            newBoard = deepcopy(self.board)
            newBoard.doAction(action)
            child = Node(self, 0, 0, newBoard, action)
            self.children.append(child)
