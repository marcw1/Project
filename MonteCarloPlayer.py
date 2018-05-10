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
    # total number of simulations allowed
    total_sim = 150
    # exploration parameter for UCT selection
    C = 1
    temp = 0
    
    def action(self, turns):
        
        #creates a root node
        root = Node(None, deepcopy(self.board), None)
        node = root
        
        
        #put shit in the middle first haha
        if self.temp <15:
            self.temp += 1
            while node.untriedActions != []:
                child = node.expand()
                child.boardEval(child.board)
            best = sorted(node.children, key=lambda c: c.value)[0]
            self.board.doAction(best.action)
            return best.action
        
        #keeps running UCTS until time is up
        '''start_time = time.time()
        while time.time() - start_time < self.time_limit:'''
        #keeps running UCTS until certain number of moves
        for _ in range(self.total_sim):
            
            # Selection
            while node.children != [] and node.untriedActions == []:
                node = self.UCTselectChildNode(node)
    
            # Expansion
            if node.untriedActions != []:
                node = node.expand()
    
            # Simulation
            winner = self.randomSimulation(node)
            #winner = self.bestMoveSimulation(node)
    
            # Backpropagation
            while node.pred != None:
                self.addWins(node, winner) # update win values
                node = node.pred
            self.addWins(node, winner)
            
        action = sorted(root.children, key=lambda c: c.visits)[-1].action       
        self.board.doAction(action)
        return action
    

    
    def UCTselectChildNode(self, node):
        ''' selects a child node based on UCB1 formula
            exploration parameter C
        '''
        selected = sorted(node.children, key=lambda c: c.wins/c.visits \
                 + self.C*sqrt(2*log1p(node.visits)/c.visits))[-1]
        return selected  
        
    
    def randomSimulation(self, node):
        ''' does a completely random rollout to the end
        '''
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
    
    '''
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
            
        return winner
    '''
      
    def addWins(self, node, winner):
        ''' updates the win and visit values of a node
        '''
        if winner == node.board.enemy_team:
            node.wins += 1
        elif winner == 'draw':
            node.wins += 0.5
        node.visits += 1
        
        
    