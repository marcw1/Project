from Board import Board
from Move import Move
from abc import ABC, abstractmethod

class AbstractPlayer(ABC):
    colour = ""
    board = None
    BOARD_SIZE = 64
    PLACING_PHASE_MOVES = 24
    phase = "placing"
    strategy = None


    def __init__(self, colour):
        self.colour = colour
        self.board = Board()

    # returns an action (placement or movement)
    @abstractmethod
    def action(self, turns):
        pass

    # updates the board state based on an action
    def update(self, action):
        #if action is a move
        if isinstance(action[0], int):
            self.board.addPiece(self.colour, *action)
        #if action is a placement
        else:
            self.board = self.board.makeMove(Move(*action))
            


