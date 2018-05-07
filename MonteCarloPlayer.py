'''
Created on 6 May 2018

@author: chooyisiumaria
'''
from AbstractPlayer import AbstractPlayer
from Node import Node
import random
import time
from copy import deepcopy
from math import sqrt, log1p
class Player(AbstractPlayer):
    
    #time_limit = 0.5 
    total_sim = 50
    UCTK = 1
    simulations = 0
    
    def action(self, turns):
        
        #creates a root node
        root = Node(None, deepcopy(self.board), None)
        node = root
        
        #keeps running MCTS until time is up
        '''start_time = time.time()
        while time.time() - start_time < self.time_limit:'''
        #keeps running MCTS until certain number of moves
        for _ in range(self.total_sim):
            
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
            #winner = self.bestMoveSimulation(node)
    
            # Backpropagate
            while node.pred != None: # backpropagate from the expanded node and work back to the root node
                self.addWins(node, winner) # update win values
                #print(node)
                node = node.pred
            self.addWins(node, winner)
            #print(node)
            
        action = sorted(root.children, key = lambda c: c.visits)[-1].action       
        self.board.doAction(action)
        #print(self.simulations)
        #self.simulations = 0            
        return action
    

    
    def UCTselectChild(self, node):
        ''' selects a child node based on UCB1 formula
            exploration parameter UCTK
        '''
        s = sorted(node.children, key=lambda c: c.wins/c.visits + self.UCTK*sqrt(2*log1p(c.pred.visits)/c.visits))[-1]
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
            
        #self.simulations += 1 
        return winner
    
    def bestMoveSimulation(self, node):
        board = deepcopy(node.board)
        winner = board.check_winner()
        while (winner is None):
            actions = board.checkActions()
            lastEval = node.boardEval(board)
            for action in actions:
                board.doAction(action)
                nowEval = node.boardEval(board)
                if nowEval >= lastEval:
                    break
                board.undoLastAction()
                
            winner = board.check_winner()
            
        #self.simulations += 1 
        return winner
    
    
    def addWins(self, node, winner):
        if winner == node.board.enemy_team:
            node.wins += 1
        elif winner == 'draw':
            node.wins += 0.5
        node.visits += 1
        
        
    