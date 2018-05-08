from Board import Board
from Node import Node
from copy import deepcopy

class Player:
    playerPiece = None
    enemyPiece = None
    currentBoard = None
    BOARD_SIZE = 64
    PLACING_PHASE_MOVES = 24
    phase = "moving"
    killerMoves = None
    bestMove = None
    bestScore = -float('inf')


    def __init__(self, colour):
        if colour == "white":
            self.playerPiece = "W"
            self.enemyPiece = "B"
        else:
            self.playerPiece = "B"
            self.enemyPiece = "W"

        self.currentBoard = Board(self.BOARD_SIZE)
        # self.killerMoves = [2][3]

        self.currentBoard.addPiece("B", 3, 2)
        self.currentBoard.addPiece("B", 3, 3)
        self.currentBoard.addPiece("B", 3, 5)
        self.currentBoard.addPiece("B", 2, 2)
        self.currentBoard.addPiece("B", 2, 4)
        self.currentBoard.addPiece("B", 1, 0)
        self.currentBoard.addPiece("W", 0, 2)
        self.currentBoard.__str__()

        # self.ABRoot(self.currentBoard, 3, self.playerPiece)
        # self.ABPruning(self.currentBoard, 4, -float('inf'), float('inf'), self.playerPiece)

        # self.currentBoard._shrink_board()
        # self.currentBoard._shrink_board()

    def action(self, turns):
        if self.phase == "placing" and turns > self.PLACING_PHASE_MOVES:
            self.phase == "moving"
        depth = 4
        move = self.ABPruning(self.currentBoard, depth, -float('inf'), float('inf'), self.playerPiece)



    def update(self, action):
        if type(action[0]) is tuple:
            self.currentBoard.movePiece(action[0], action[1])
        elif type(action[0]) is int:
            self.currentBoard.addPiece(self.enemyPiece, action[0], action[1])



    def ABPruning(self, board, depth, a, b, player):
        if depth == 0 or len(self.currentBoard.getPossiblePiecePlaces()) == 0:
            return board.evaluateBoard(self.playerPiece)

        bestMove = None
        bestVal = -float('inf')

        if player == self.playerPiece:
            value = -float('inf')

            if self.phase == "placing":
                moves = board.getPossiblePiecePlaces()
            else:
                moves = board.checkMoves(player)

            for move in moves:
                newBoard = deepcopy(board)

                if self.phase == "placing":
                    newBoard.addPiece(player, move[0], move[1])
                else:
                    newBoard.movePiece(move[0], move[1])

                value = max(value, self.ABPruning(newBoard, depth - 1, a, b, self.enemyPiece))
                if value > bestVal and depth == 4:
                    bestVal = value
                    bestMove = move
                    print(bestMove)
                a = max(a, value)
                if b <= a:
                    break;

        else:
            value = float('inf')

            if self.phase == "placing":
                moves = board.getPossiblePiecePlaces()
            else:
                moves = board.checkMoves(player)

            for move in moves:
                newBoard = deepcopy(board)

                if self.phase == "placing":
                    newBoard.addPiece(player, move[0], move[1])
                else:
                    newBoard.movePiece(move[0], move[1])

                value = min(value, self.ABPruning(newBoard, depth - 1, a, b, self.playerPiece))
                b = min (b, value)
                if b <= a:
                    break;

        return value


t = Player("white")
t.action(1)
