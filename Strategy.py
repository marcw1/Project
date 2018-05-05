from Board import Board
import random

class Strategy:
    board = None

    def __init__(self, board):
        self.board = board

    def makePlacingPhaseMove(self, board):
        count = 0
        x, y = random.choice(board.getPossiblePiecePlaces())
        board.addPiece("W", x, y)
        for x, y in board._squares_with_piece("W"):
            a, b = board._eliminate_about(x, y)
            print("a: ", a, "b: ", b)
            count += (a + b)

        print("Score: ", count)

    def movingPhase(self):
        print("moving phase")
