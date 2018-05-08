'''
Created on 5 May 2018

@author: chooyisiumaria


A Player that always makes a random move
'''
from AbstractPlayer import AbstractPlayer
import random

class Player(AbstractPlayer):
    
    def action(self, turns):
        
        actions = self.board.checkActions()
        action = None
        if len(actions) > 0:
            action = random.choice(actions)
        self.board.doAction(action)
            
        return action
            