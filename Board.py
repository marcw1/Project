from itertools import cycle

class Board:
    
    DISPLAY = {'black': '@', 'white': 'O', 'X': 'X'}
    colours = ('white', 'black')

    # makes an empty board
    def __init__(self):
        
        self.n_shrinks = 0
        self.pieces = {'@': 0, 'O': 0}
        self.phase = 'placing'
        self.turns = 0
        # makes an iterator to cycle through teams
        self.team_iterator = cycle(Board.colours)
        self.current_team = next(self.team_iterator)
        
        self.board = [['-' for _ in range(8)] for _ in range(8)]
        for square in [(0, 0), (7, 0), (7, 7), (0, 7)]:
            x, y = square
            self.board[y][x] = 'X'
     
    # finds all possible actions for a colour       
    def checkActions(self, colour):
        if self.phase == 'placing':
            possibleActions = self.checkPiecePlaces(colour)
        elif self.phase == 'moving':
            possibleActions = self.checkMoves(colour)
        return possibleActions


    # returns a list of possible moves for a colour
    def checkMoves(self, colour):
        possibleMoves = []
        for xa, ya in self._squares_with_piece(self.DISPLAY[colour]):
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                # is the adjacent square unoccupied?
                xb, yb = xa + dx, ya + dy
                xc, yc = xa + 2*dx, ya + 2*dy
                if self._within_board(xb, yb) and self.board[yb][xb] == '-':
                    move = ((xa, ya), (xb, yb))
                    possibleMoves.append(move)
                elif self._within_board(xc, yc) and self.board[yc][xc] == '-':
                    move = ((xa, ya), (xc, yc))
                    possibleMoves.append(move)
        return possibleMoves
    
        # finds all locations where a piece can be placed
    def checkPiecePlaces(self, colour):
        possiblePlaces = []
        if colour == "white":
            yMin = 0 + self.n_shrinks
            yMax = 6
        elif colour == "black":
            yMin = 3
            yMax = 8 - self.n_shrinks
        for x in range(0 + self.n_shrinks, 8 - self.n_shrinks):
            for y in range(yMin, yMax):
                if self.board[y][x] == "-":
                    possiblePlaces.append((x, y))
        return possiblePlaces
    
    # does an action on the board, whether its a move or a placement
    def doAction(self, colour, action):
        
        # checks if action is piece placement
        if isinstance(action[0], int):
            self.addPiece(colour, *action)
        # otherwise move the piece
        else:
            self.movePiece(*action)
        # cycles to next team
        self.current_team = next(self.team_iterator)
       
    # adds a piece to the board
    def addPiece(self, colour, x, y):
        if self.board[y][x] == "-":
            self.board[y][x] = self.DISPLAY[colour]
            self._eliminate_about(x, y)

    # moves a piece
    def movePiece(self, moveFrom, moveTo):      
        piece = self.board[moveFrom[1]][moveFrom[0]]      
        self.board[moveFrom[1]][moveFrom[0]] = '-'
        self.board[moveTo[1]][moveTo[0]] = piece
        #eliminate
        self._eliminate_about(moveTo[0], moveTo[1])      

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
        string = "" 
        for i in range(8):
            for j in range(8):
                string += self.board[i][j]
                if j < 7:
                    string += " "
                else:
                    string += "\n"
        return string


    def _within_board(self, x, y):
        """
        Check if a given pair of coordinates is 'on the board'.

        :param x: column value
        :param y: row value
        :return: True iff the coordinate is on the board
        """
        for coord in [y, x]:
            if coord < 0 + self.n_shrinks or coord > 7 - self.n_shrinks:
                return False
        if self.board[y][x] == ' ':
            return False
        return True



    def shrink_board(self):
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
            self._eliminate_about(x, y)

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

    # checks if 2 boards are equivalent
    def __hash__(self):
        return hash(self.board)


    # Used for scoring
    def loopThrough(self, method):
        count = 0
        for x in range(0 + self.n_shrinks, 8 - self.n_shrinks):
            for y in range(0 + self.n_shrinks, 8 - self.n_shrinks):
               a, b = method(x, y)
               count += (a + b)
        return count

    def _eliminate_about(self, x, y):
        """
        A piece has entered this square: look around to eliminate adjacent
        (surrounded) enemy pieces, then possibly eliminate this piece too.

        :param square: the square to look around
        """
        piece = self.board[y][x]
        targets = self._targets(piece)
        gotKill = 0

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
                    gotKill = 1

        gotKilled = 0
        # Check if the current piece is surrounded and should be eliminated
        if piece in self.pieces:
            if self._surrounded(x, y, 1, 0) or self._surrounded(x, y, 0, 1):
                self.board[y][x] = '-'
                self.pieces[piece] -= 1
                gotKilled = 1
        return gotKill, gotKilled

    def _enemies(self, piece):
        """
        Which pieces can eliminate a piece of this type?

        :param piece: the type of piece ('B', 'W', or 'X')
        :return: set of piece types that can eliminate a piece of this type
        """
        if piece == '@':
            return {'O', 'X'}
        elif piece == 'O':
            return {'@', 'X'}
        return set()

    def _targets(self, piece):
        """
        Which pieces can a piece of this type eliminate?

        :param piece: the type of piece ('B', 'W', or 'X')
        :return: the set of piece types that a piece of this type can eliminate
        """
        if piece == '@':
            return {'O'}
        elif piece == 'O':
            return {'@'}
        elif piece == 'X':
            return {'@', 'O'}
        return set()

