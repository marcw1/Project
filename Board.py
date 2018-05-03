from Piece import Piece
from Move import Move


class Board:
    size = None
    board = None
    n_shrinks = 0
    pieces = {'W': 0, 'B': 0}

    # makes an empty board
    def __init__(self, size):
        self.board = [['-' for _ in range(8)] for _ in range(8)]
        for square in [(0, 0), (7, 0), (7, 7), (0, 7)]:
            x, y = square
            self.board[y][x] = 'X'
        self.n_shrinks = 0

    def _squares_with_piece(self, piece):
        """
        Generate coordinates of squares currently containing a piece
        :param piece: string representation of the piece type to check for
        """
        for x in range(8):
            for y in range(8):
                if self.board[y][x] == piece:
                    yield (x, y)


    # returns formatted string of current board state
    def __str__(self):
        """String representation of the current board state."""
        for row in self.board:
            print(*row)


    def _within_board(self, x, y):
        """
        Check if a given pair of coordinates is 'on the board'.

        :param x: column value
        :param y: row value
        :return: True iff the coordinate is on the board
        """
        for coord in [y, x]:
            if coord < 0 or coord > 7:
                return False
        if self.board[y][x] == ' ':
            return False
        return True

    # pinched from referee
    def checkMoves(self, piece):
        possibleMoves = []
        for xa, ya in self._squares_with_piece(piece):
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                # is the adjacent square unoccupied?
                xb, yb = xa + dx, ya + dy
                xc, yc = xa + 2*dx, ya + 2*dy
                if self._within_board(xb, yb) and self.board[yb][xb] == '-':
                    move = (yb, xb)
                elif self._within_board(xc, yc) and self.board[yc][xc] == '-':
                    move = (yc, xc)
                    print(move)
                possibleMoves.append(move)
        print([possibleMoves[i:i + 2] for i in range(0, len(possibleMoves), 2)])

    def _shrink_board(self):
        """
        Shrink the board, eliminating all pieces along the outermost layer,
        and replacing the corners.

        This method can be called up to two times only.
        """
        s = self.n_shrinks  # number of shrinks so far, or 's' for short
        # Remove edges
        for i in range(s, 8 - s):
            for square in [(i, s), (s, i), (i, 7 - s), (7 - s, i)]:
                x, y = square
                piece = self.board[y][x]
                if piece in self.pieces:
                    self.pieces[piece] -= 1
                self.board[y][x] = ' '

        # we have now shrunk the board once more!
        self.n_shrinks = s = s + 1

        # replace the corners (and perform corner elimination)
        for corner in [(s, s), (s, 7 - s), (7 - s, 7 - s), (7 - s, s)]:
            x, y = corner
            piece = self.board[y][x]
            if piece in self.pieces:
                self.pieces[piece] -= 1
            self.board[y][x] = 'X'
            self._eliminate_about(corner)

    def _eliminate_about(self, square):
        """
        A piece has entered this square: look around to eliminate adjacent
        (surrounded) enemy pieces, then possibly eliminate this piece too.

        :param square: the square to look around
        """
        x, y = square
        piece = self.board[y][x]
        targets = self._targets(piece)

        # Check if piece in square eliminates other pieces
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            target_x, target_y = x + dx, y + dy
            targetval = None
            if self._within_board(target_x, target_y):
                targetval = self.board[target_y][target_x]
            if targetval in targets:
                if self._surrounded(target_x, target_y, -dx, -dy):
                    self.board[target_y][target_x] = '-'
                    self.pieces[targetval] -= 1

        # Check if the current piece is surrounded and should be eliminated
        if piece in self.pieces:
            if self._surrounded(x, y, 1, 0) or self._surrounded(x, y, 0, 1):
                self.board[y][x] = '-'
                self.pieces[piece] -= 1

    def _surrounded(self, x, y, dx, dy):
        """
        Check if piece on (x, y) is surrounded on (x + dx, y + dy) and
        (x - dx, y - dy).

        :param x: column of the square to be checked
        :param y: row of the square to be checked
        :param dx: 1 if adjacent cols are to be checked (dy should be 0)
        :param dy: 1 if adjacent rows are to be checked (dx should be 0)
        :return: True iff the square is surrounded
        """
        xa, ya = x + dx, y + dy
        firstval = None
        if self._within_board(xa, ya):
            firstval = self.board[ya][xa]

        xb, yb = x - dx, y - dy
        secondval = None
        if self._within_board(xb, yb):
            secondval = self.board[yb][xb]

        # If both adjacent squares have enemies then this piece is surrounded!
        piece = self.board[y][x]
        enemies = self._enemies(piece)
        return firstval in enemies and secondval in enemies

    def _targets(self, piece):
        """
        Which pieces can a piece of this type eliminate?

        :param piece: the type of piece ('B', 'W', or 'X')
        :return: the set of piece types that a piece of this type can eliminate
        """
        if piece == 'B':
            return {'W'}
        elif piece == 'W':
            return {'B'}
        elif piece == 'X':
            return {'B', 'W'}
        return set()

    # checks if 2 boards are equivalent
    def __hash__(self):
        return hash(str(self))

    # adds a piece to the board, returns that piece
    def addPiece(self, team, row, col):
        if self.getPiece(row, col) == "-":
            self.board[row][col] = team

    # returns the piece at a position on the board
    def getPiece(self, row, col):
        return self.board[row][col]

    # returns total number of moves available
    def countMoves(self, team):
        moves = 0
        for piece in self.pieces[team]:
            moves += len(piece.getMoves(self))
        return moves

    # returns list of all moves available
    def getMoves(self, team):
        moves = []
        for piece in self.pieces[team]:
            for move in piece.getMoves(self):
                moves.append(move)
        return moves

    # returns a new Board object after move has been made
    def makeMove(self, move):
        newBoard = Board(self.size)
        for teamPieces in self.pieces.values():
            for p in teamPieces:
                newBoard.addPiece(p.team, p.loc[0], p.loc[1])
        # moves the piece
        pieceToMove = newBoard.board[move.old[0]][move.old[1]]
        newBoard.board[move.old[0]][move.old[1]] = None
        newBoard.board[move.new[0]][move.new[1]] = pieceToMove
        pieceToMove.loc = move.new

        # eliminates pieces
        for step in Move.oneStep(move.new):
            newBoard.eliminate(*step)
        newBoard.eliminate(*move.new)

        return newBoard

    # returns list of lists of coordinates that will eliminate a piece
    def killSpots(self, piece):
        steps = Move.oneStep(piece.loc)
        team = piece.team
        killspots = []
        # try N-S steps
        try:
            if (self.getPiece(*steps[0]) == None \
                or self.getPiece(*steps[0]).team != team) \
                    and (self.getPiece(*steps[2]) == None \
                         or self.getPiece(*steps[2]).team != team):

                pair = []

                if (self.getPiece(*steps[0]) == None \
                        or self.getPiece(*steps[0]).team != "X"):
                    pair.append(steps[0])
                if (self.getPiece(*steps[2]) == None \
                        or self.getPiece(*steps[2]).team != "X"):
                    pair.append(steps[2])
                killspots.append(pair)
        except:
            pass
        # try E-W steps
        try:
            if (self.getPiece(*steps[1]) == None \
                or self.getPiece(*steps[1]).team != team) \
                    and (self.getPiece(*steps[3]) == None \
                         or self.getPiece(*steps[3]).team != team):

                pair = []

                if (self.getPiece(*steps[1]) == None \
                        or self.getPiece(*steps[1]).team != "X"):
                    pair.append(steps[1])

                if (self.getPiece(*steps[3]) == None \
                        or self.getPiece(*steps[3]).team != "X"):
                    pair.append(steps[3])

                killspots.append(pair)
        except:
            pass
        return killspots

    # trys to eliminate a piece at a position
    def eliminate(self, row, col):
        try:
            piece = self.getPiece(row, col)
            if piece != None:
                steps = Move.oneStep((row, col))
                team = piece.team
                # check the N-S steps for enemies
                try:
                    if self.getPiece(*steps[0]).team != team \
                            and self.getPiece(*steps[2]).team != team:
                        self.board[row][col] = None
                        self.pieces[team].remove(piece)
                except:
                    pass
                # check the E-W steps for enemies
                try:
                    if self.getPiece(*steps[1]).team != team \
                            and self.getPiece(*steps[3]).team != team:
                        self.board[row][col] = None
                        self.pieces[team].remove(piece)
                except:
                    pass
        except:
            pass
