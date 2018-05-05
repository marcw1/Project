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
            move = random.choice(self.board.getPossiblePiecePlaces())
            return move
        else:
            move = random.choice(self.board.getMoves(self.colour))
            return move
            