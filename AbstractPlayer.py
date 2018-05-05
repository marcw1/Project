from Board import Board
from Move import Move
from abc import ABC, abstractmethod

class AbstractPlayer(ABC):
    colour = ""
    enemyColour = ""
    COLOURS = ("white", "black")
    PLACING_PHASE_MOVES = 24
    phase = 'placing'

    def __init__(self, colour):
        self.colour = colour
        for colour in self.COLOURS:
            if colour != self.colour:
                self.enemyColour = colour
        self.board = Board()

    # returns an action (placement or movement)
    @abstractmethod
    def action(self, turns):
        pass

    # updates the board state based on an action
    def update(self, action):
        #if action is a placement
        if isinstance(action[0], int):
            self.board.addPiece(self.enemyColour, *action)
        #if action is a move
        else:
            self.board.makeMove(Move(*action))
            


