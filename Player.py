from Board import Board

class Player:
    colour = ""
    currentBoard = None
    BOARD_SIZE = 64
    PLACING_PHASE_MOVES = 24
    phase = "placing"


    def __init__(self, colour):
        self.colour = colour
        self.currentBoard = Board(self.BOARD_SIZE)
        self.currentBoard.addPiece("O", 3, 4)
        self.currentBoard.addPiece("W", 4, 4)
        self.currentBoard.__str__()
        self.currentBoard.checkMoves("O")


    def action(self, turns):
        if self.phase == "placing" and turns > self.PLACING_PHASE_MOVES:
            self.phase == "moving"


    def update(self, action):
        print("Nothing yet")


t = Player("White")