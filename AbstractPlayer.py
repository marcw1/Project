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
        self.board.doAction(self.enemyColour, action)
      
    # returns list of all possible actions      
    def _get_all_moves(self, turns):
        if turns in [128, 129] and self.board.n_shrinks == 0:
            self.board.shrink_board()
        elif turns in [192, 193] and self.board.n_shrinks == 1:
            self.board.shrink_board()
        actions = self.board.checkActions(self.colour)
        return actions
