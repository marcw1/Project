'''
Created on 5 May 2018

@author: chooyisiumaria


A Player that always makes a random move
'''
from AbstractPlayer import AbstractPlayer
import random

class Player(AbstractPlayer):
    
    def action(self, turns):
        
        move = random.choice(self._get_all_moves(turns))
        self.board.doAction(move)
        
        # checks to change to moving phase
        if turns in [22, 23]:
            self.board.phase = 'moving'
            
        return move
            