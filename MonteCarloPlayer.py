'''
Created on 6 May 2018

@author: chooyisiumaria
'''
from AbstractPlayer import AbstractPlayer
from Node import Node
import random
import time
from copy import deepcopy
from math import sqrt, log2
class Player(AbstractPlayer):
    
    time_limit = 10
    UCTK = 1
    
    def action(self, turns):
        
        #creates a root node
        root = Node(None, deepcopy(self.board), None)
        
        #keeps running MCTS until time is up
        start_time = time.time()
        expanded = []
        node = root
        while time.time() - start_time < self.time_limit:
            
            # Select)
            while node.untriedActions == [] and node.children != []: # node is fully expanded and non-terminal
                #print(node)
                node = self.UCTselectChild(node)
                #print(node)
    
            # Expand
            if node.untriedActions != []: # if we can expand (i.e. state/node is non-terminal)
                node = node.expand()
                #print(node)
    
            # Rollout
            winner = self.randomSimulation(node)
    
            # Backpropagate
            while node.pred != None: # backpropagate from the expanded node and work back to the root node
                self.addWins(node, winner) # update win values
                #print(node)
                node = node.pred
            self.addWins(node, winner)
            #print(node)
            
        action = sorted(root.children, key = lambda c: c.visits)[-1].action       
        self.board.doAction(action)                 
        return action
    

    
    def UCTselectChild(self, node):
        ''' selects a child node based on UCB1 formula
            exploration parameter UCTK
        '''
        s = sorted(node.children, key=lambda c: c.wins/c.visits + self.UCTK*sqrt(2*log2(c.visits)/c.visits))[-1]
        return s  
        
    
    def randomSimulation(self, node):
        board = deepcopy(node.board)
        winner = board.check_winner()
        while (winner is None):
            action = None
            actions = board.checkActions()
            if len(actions) > 0:
                action = random.choice(board.checkActions())      
            board.doAction(action)
            winner = board.check_winner()
            
        return winner
    
    def addWins(self, node, winner):
        if winner == node.board.current_team:
            node.wins += 1
        node.visits += 1
        
        
    