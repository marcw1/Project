'''
Created on 6 May 2018

@author: chooyisiumaria
'''
from AbstractPlayer import AbstractPlayer
from Node import Node
import random
import time
from copy import deepcopy

class Player(AbstractPlayer):
    
    time_limit = 0.01
    
    def action(self, turns):
        start_time = time.time()
        while time.time() - start_time < self.time_limit:
            action = self._run_sim(turns)
        self.board.doAction(action)
        
        # checks to change to moving phase
        if turns in [22, 23]:
            self.board.phase = 'moving'
            
        return action
    
    # returns the best move
    def _run_sim(self, turns):
        action = random.choice(self._get_all_moves(turns))
        return action
    
    def UCTselect(self, node):    
        pass
    
    def doRandomRollout(self, node):
        board = deepcopy(node.board)
        winner = board.check_winner()
        while (winner == None):
            action = random.choice(board.checkActions)      
            board.doAction(action)
            winner = board.check_winner()
            
        if winner == node.board.current_team():
            node.wins += 1
            
        node.visits += 1
        
        
    