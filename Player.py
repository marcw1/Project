from Board import Board
from Node import Node
from copy import deepcopy

class Player:
    playerPiece = None
    enemyPiece = None
    currentBoard = None
    BOARD_SIZE = 64
    PLACING_PHASE_MOVES = 23
    phase = "placing"
    killerMoves = None
    bestMove = None
    bestScore = -float('inf')
    depth = 2


    def __init__(self, colour):
        if colour == "white":
            self.playerPiece = "W"
            self.enemyPiece = "B"
        else:
            self.playerPiece = "B"
            self.enemyPiece = "W"

        self.currentBoard = Board(self.BOARD_SIZE)
        self.killerMoves = [[None for x in range(1)] for x in range(self.depth)]


        # self.currentBoard.addPiece(3, 2, "B")
        # self.currentBoard.addPiece(3, 3, "B")
        # self.currentBoard.addPiece(3, 5, "B")
        # self.currentBoard.addPiece(2, 2, "B")
        # self.currentBoard.addPiece(2, 4, "B")
        # self.currentBoard.addPiece(1, 0, "B")
        # self.currentBoard.addPiece(0, 2, "W")
        # self.currentBoard.__str__()


    def action(self, turns):
        blank, move = self.ABPruning(self.currentBoard, self.depth, -float('inf'), float('inf'), self.playerPiece)

        self.currentBoard.doAction(move)

        # self.currentBoard.__str__()
        # print(self.currentBoard.pieces)
        print("trying move: ", move, self.phase, turns)

        if self.phase == "placing" and turns == 22 or turns == 23:
            self.phase = "moving"

        return move


    def update(self, action):
        self.currentBoard.doAction(action)



    def ABPruning(self, board, depth, a, b, player):
        if depth == 0 or len(self.currentBoard.getPossiblePiecePlaces(player)) == 0:
            return board.evaluateBoard(self.playerPiece), None

        bestMove = None
        bestVal = -float('inf')

        if self.phase == "placing":
            moves = board.getPossiblePiecePlaces(player)
        else:
            # moves = board.getAllPieceMovesForTeam(player)
            moves = board.checkMoves(player)

        # Killer heuristic
        for slot in range(0, len(self.killerMoves[depth-1])-1):
            killerMove = self.killerMoves[depth-1][slot]
            for m in range(0, len(moves)):
                if m == killerMove:
                    self.addKillerMove(depth-1, m)
                    break;

        killerMoves = []
        for killerMove in self.killerMoves[depth -1]:
            if killerMove is not None:
               killerMoves.append(killerMove)

        moves = killerMoves + moves
        value = 0

        for move in moves:
            newBoard = deepcopy(board)

            newBoard.doAction(move)

            if player == self.playerPiece:
                value = -float('inf')

                value = max(value, self.ABPruning(newBoard, depth - 1, a, b, self.enemyPiece)[0])
                # Hard-coded for now
                if value > bestVal and depth == self.depth:
                    bestVal = value
                    bestMove = move
                    # print(bestMove)
                a = max(a, value)
                if b <= a:
                    self.addKillerMove(depth-1, move)
                    break;

            else:
                value = float('inf')
                value = min(value, self.ABPruning(newBoard, depth - 1, a, b, self.playerPiece)[0])
                b = min (b, value)
                if b <= a:
                    break;

        return (value, bestMove)

    def addKillerMove(self, depth, move):
        for i in range(len(self.killerMoves[depth]) - 2, -1, -1):
            self.killerMoves[depth][i + 1] = self.killerMoves[depth][i]
        self.killerMoves[depth][0] = move
