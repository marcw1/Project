from Board import Board
from Strategy import Strategy

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

        self.currentBoard._shrink_board()
        self.currentBoard._shrink_board()

    def action(self, turns):
        if self.phase == "placing" and turns > self.PLACING_PHASE_MOVES:
            self.phase == "moving"

        self.strategy.makePlacingPhaseMove(self.currentBoard)
        self.currentBoard.__str__()
        print("\n\n\n")

    def update(self, action):
        print("Nothing yet")



t = Player("White")
while (True):
    m = input("f: ")
    t.action(1)