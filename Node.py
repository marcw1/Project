class Node:
    # predecessor
    pred = None
    # path cost g(n)
    cost = 0
    # estimated total cost f(n)
    total = 0
    # board state
    board = None
    # last move made to get here
    move = None

    def __init__(self, pred, cost, total, board, move):
        self.pred = pred
        self.cost = cost
        self.total = total
        self.board = board
        self.move = move

    # used for min heap
    def __lt__(self, other):
        return self.total < other.total

    # hashes based on board
    def __hash__(self):
        return hash(self.board)

    def __str__(self):
        myString = str(self.board) + "move: " + str(self.move) + "\ncost: "
        + str(self.cost) + "\nest: " + str(self.total - self.cost) + "\ntotal: "
        + str(self.total)
        return myString

    # returns a list of child nodes as a result of making all possible moves \
    # for "O" team
    def expand(self):
        children = []
        moves = self.board.getMoves("O")
        for move in moves:
            newBoard = self.board.makeMove(move)
            child = Node(self, self.cost + 1, self.cost + 1, newBoard, move)
            children.append(child)
        return children
