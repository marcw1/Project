from copy import deepcopy
import random

class Node:

    def __init__(self, pred, board, action):
        self.pred = pred
        self.children = []
        self.wins = 0
        self.visits = 0
        self.board = board
        self.value = 0
        self.action = action
        if pred is None:
            self.depth = 0
        else:
            self.depth = pred.depth + 1
        self.untriedActions = self.board.checkActions()
        #random.shuffle(self.untriedActions)

    # used for min heap
    def __lt__(self, other):
        return self.total < other.total

    # hashes based on board
    def __hash__(self):
        return hash(self.board)

    def __str__(self):
        myString = "move: " + str(self.action) + \
        '\n wins:' + str(self.wins) + \
        '\n visits:' + str(self.visits) + \
        '\n depth:' + str(self.depth)
        return myString

    # expands an action to return a child node
    def expand(self):
        action = self.untriedActions.pop()
        newBoard = deepcopy(self.board)
        newBoard.doAction(action)
        child = Node(self, newBoard, action)
        self.children.append(child)
        return child
    
    
    # evaluates a board
    def boardEval(self, board):
        ''' f = no. my teams pieces - no. enemy team pieces
            g = no. of my traps
            h = no. of enemy's traps
            i = my piece centrality
            j = enemy piece centrality
        '''
        
        f = board.pieces[board.current_team] - board.pieces[board.enemy_team]
        g = board.find_traps(board.current_team)
        h = board.find_traps(board.enemy_team)
        i = 0
        # cycles over board twice as much as it needs to
        for piece in board._squares_with_piece(board.current_team):
            i += (piece[0])*(7-piece[0])*(piece[1])*(7-piece[1])
        j = 0
        for piece in board._squares_with_piece(board.enemy_team):
            if piece[0] == 4 and piece[1] == 3:
                j += 100
            j += (piece[0])*(7-piece[0])*(piece[1])*(7-piece[1])
        
        value = 100*f + 1*g - 1*h + 10*i - 0.1*j
        #print(value)
        #print(self.action)
        self.value = value
        return value

'''
    # evaluates an action
    def actionEval(self, board, action):
        pass
'''
