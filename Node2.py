from copy import deepcopy

class Node2:
    parent = None
    value = 0
    board = None
    turns = 0
    playerPiece = None
    enemyPiece = None
    piece = None
    children = None
    Name = "test"

    def __init__(self, parent, board, turns, piece):
        self.parent = parent
        self.board = board
        self.turns = turns
        self.piece = "B" if piece == "W" else "W"
        self.value = board.evaluateBoard("W")
        self.children = []
        # if (self.turns == 1):
        #     print("turns: ", self.turns, "score: ", self.value, "piece: ", self.piece)
        #     print(self.board.__str__(), "\n")
        self.expand()

    # used for min heap
    def __lt__(self, other):
        return self.score < other.score

    # hashes based on board
    def __hash__(self):
        return hash(self.board)

    # returns a list of child nodes as a result of making all possible moves
    def expand(self):
        moves = self.board.getPossiblePiecePlaces()
        if self.turns == 3:
            return
        for move in moves:
            if len(self.children) > 20:
                break
            newBoard = deepcopy(self.board)
            newBoard.addPiece(self.piece, move[0], move[1])
            child = Node2(self,  newBoard, self.turns + 1, self.piece)
            self.children.append(child)
        return