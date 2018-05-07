from Board import Board
from Strategy import Strategy
from Node2 import Node2

class Player:
    colour = ""
    currentBoard = None
    BOARD_SIZE = 64
    PLACING_PHASE_MOVES = 24
    phase = "placing"
    strategy = None


    def __init__(self, colour):
        self.colour = colour
        self.currentBoard = Board(self.BOARD_SIZE)
        self.strategy = Strategy(self.currentBoard)

        self.currentBoard.addPiece("B", 3, 2)
        self.currentBoard.addPiece("B", 3, 3)
        self.currentBoard.addPiece("B", 3, 5)
        self.currentBoard.addPiece("B", 2, 2)
        self.currentBoard.addPiece("B", 2, 4)
        self.currentBoard.addPiece("B", 1, 0)

        # self.currentBoard._shrink_board()
        # self.currentBoard._shrink_board()

    def action(self, turns):
        if self.phase == "placing" and turns > self.PLACING_PHASE_MOVES:
            self.phase == "moving"
        else:
            self.makePlacingPhaseMove()

        # self.currentBoard.__str__()
        print("\n\n\n")


    def update(self, action):
        print("Nothing yet")

    def makePlacingPhaseMove(self):
        t = Node2(None, self.currentBoard, 0, "B")
        self.currentBoard.__str__()
        # t.expand()
        self.ABPruning(t)
        # self.currentBoard.evaluateBoard("B")


    def ABPruning(self, node):
        b = float('inf')
        bestVal = -float('inf')
        bestNode = None

        for childNode in node.children:
            value = self.min(childNode, bestVal, b)
            if value > bestVal:
                bestVal = value
                bestNode = childNode
        print("Best Score: ", bestNode.value)
        print(bestNode.board.__str__())
        return bestNode

    def min(self, node, a, b):
        if len(node.children) == 0:
            return node.value

        value = float('inf')
        for childNode in node.children:
            value = min(value, self.max(childNode, a, b))
            if value <= a:
                return value
            b = min(b, value)

        return value

    def max(self, node, a, b):
        if len(node.children) == 0:
            return node.value
        value = -float('inf')

        for childNode in node.children:
            value = max(value, self.min(childNode, a, b))
            if value >= b:
                return value
            a = max(a, value)
        return value


t = Player("White")
while (True):
    m = input("f: ")
    t.action(1)