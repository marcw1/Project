from Board import Board
from Move import Move
from abc import ABC, abstractmethod

class AbstractPlayer(ABC):
    colour = ""
    currentBoard = None
    BOARD_SIZE = 64
    PLACING_PHASE_MOVES = 24
    phase = "placing"
    strategy = None


    def __init__(self, colour):
        self.colour = colour
        self.currentBoard = Board(self.BOARD_SIZE)

    # returns an action (placement or movement)
    @abstractmethod
    def action(self, turns):
        pass

    # updates the board state based on an action
    def update(self, action):
        count = sum([len(t) for t in action])
        #if action is a move
        if count == 4:
            self.board = self.board.makeMove(Move(*action))
        #if action is a placement
        elif count == 2:
            self.board.addPiece(self.colour, *action)
            


