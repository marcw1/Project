'''
Created on 5 May 2018

@author: chooyisiumaria


A Player that always makes a random move
'''
from AbstractPlayer import AbstractPlayer
import random

class Player(AbstractPlayer):
    
    def action(self, turns):
        if turns < self.PLACING_PHASE_MOVES:
            move = random.choice(self.board.getPossiblePiecePlaces(self.colour))
            self.board.addPiece(self.colour, *move)
            return move
        else:
            move = random.choice(self.board.checkMoves(self.colour))
            return (move.full)
            