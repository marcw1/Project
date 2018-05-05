'''
Created on 5 May 2018

@author: chooyisiumaria


A Player that always makes a random move
'''
from AbstractPlayer import AbstractPlayer
import random

class Player(AbstractPlayer):
    
    def action(self, turns):
        if self.phase == 'placing':
            if turns >= self.PLACING_PHASE_MOVES-2:
                self.phase = 'moving'
            move = random.choice(self.board.getPossiblePiecePlaces(self.colour))
            self.board.addPiece(self.colour, *move)
            return move
        elif self.phase == 'moving':
            if turns in [128, 129, 192, 193]:
                self.board.shrink_board()
            move = random.choice(self.board.checkMoves(self.colour))
            self.board.makeMove(move)
            return (move.full)
            