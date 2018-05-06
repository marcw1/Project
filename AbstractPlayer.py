from Board import Board
from abc import ABC, abstractmethod

class AbstractPlayer(ABC):

    def __init__(self, colour):
        self.colour = colour
        self.board = Board()

    # returns an action (placement or movement)
    @abstractmethod
    def action(self, turns):
        pass

    # updates the board state based on an action
    def update(self, action):
        self.board.doAction(action)
