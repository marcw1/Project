from itertools import cycle

class Board:

    teams = ('W', 'B')
    direc = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # makes an empty board
    def __init__(self, size):
        
        self.n_shrinks = 0
        self.pieces = {'W': 0, 'B': 0}
        self.pieceMoves = {'W':{}, 'B':{}}
        self.phase = 'placing'
        self.turns = 0
        self.enemy_team = 'B'
        # makes an iterator to cycle through teams
        self.team_iterator = cycle(Board.teams)
        self.current_team = next(self.team_iterator)
        
        self.board = [['-' for _ in range(8)] for _ in range(8)]
        for square in [(0, 0), (7, 0), (7, 7), (0, 7)]:
            x, y = square
            self.board[y][x] = 'X'
  
  
    # finds all possible actions for current team     
    def checkActions(self):
        if self.phase == 'placing':
            possibleActions = self.getPossiblePiecePlaces()
        elif self.phase == 'moving':
            possibleActions = self.checkMoves()
            #possibleActions = self.getAllPieceMovesForTeam(self.current_team)
        return possibleActions  
    
    
    # returns a list of possible moves for current team
    def checkMoves(self, piece=None):
        
        if piece is None:
            piece = self.current_team
            
        possibleMoves = []
        for xa, ya in self._squares_with_piece(piece):
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


    
    def updateMovesAt(self, x, y, dir=None):
        ''' updates the moves of a piece at (x, y)
            optionally only in direction dir
        '''
        if self._within_board(x, y) and (self.board[y][x] in Board.teams):
            piece = self.board[y][x]
            #print(self.current_team)
            #str(self)
            #print((x,y))
            
            # update moves in 4 directions    
            if dir is None:
                possibleMoves = []
                for dx, dy in Board.direc:
                    # is the adjacent square unoccupied?
                    xb, yb = x + dx, y + dy
                    xc, yc = x + 2 * dx, y + 2 * dy
                    if self._within_board(xb, yb) and self.board[yb][xb] == '-':
                        move = (xb, yb)
                        possibleMoves.append(move)
                    elif self._within_board(xc, yc) and self.board[yc][xc] == '-':
                        move = (xc, yc)
                        possibleMoves.append(move)
                        
                self.pieceMoves[piece][(x,y)] = possibleMoves
                #print(self.pieceMoves[piece][(x,y)])
                        
            # or update in just 1 direction
            '''else:
                (dx, dy) = dir
                 # is the adjacent square unoccupied?
                xb, yb = x + dx, y + dy
                xc, yc = x + 2 * dx, y + 2 * dy    
                moves = self.pieceMoves[piece][(x,y)]
                #delete first
                if (xb, yb) in moves:
                    moves.remove((xb, yb))
                if (xc, yc) in moves:
                    moves.remove((xc, yc))
                #print(moves)               
                    
                if self._within_board(xb, yb) and self.board[yb][xb] == '-':
                    moves.append((xb, yb))
                    #print(str(dir) + str((x,y) )+ str((xb, yb)))
                elif self._within_board(xc, yc) and self.board[yc][xc] == '-':
                    moves.append((xc, yc))
                    #print((xc, yc))'''

        
    def updateMovesAround(self, x, y):
        ''' updates the moves of (x,y) and
            updates the moves of pieces around (x,y)
            but only in the direction of (x,y)
        '''
        self.updateMovesAt(x, y)
        for dx, dy in Board.direc:
            xb, yb = x + dx, y + dy
            xc, yc = x + 2 * dx, y + 2 * dy
           # dir = (x-xb,y-yb)
            self.updateMovesAt(xb, yb)
            self.updateMovesAt(xc, yc)

    def removePieceMoves(self, piece, x, y):
        del self.pieceMoves[piece][(x, y)]

    def getAllPieceMovesForTeam(self, team=None):
        moveList = []
        for moveFrom in self.pieceMoves[team]:
            for moveTo in self.pieceMoves[team][moveFrom]:
                moveList.append((moveFrom, moveTo))
        return moveList
               
    def getPossiblePiecePlaces(self, team=None):
        if team is None:
            team = self.current_team
        possiblePlaces = []
        if team== 'W':
            yMin = 0
            yMax = 6
        elif team == 'B':
            yMin = 2
            yMax = 8
        for x in range(0, 8):
            for y in range(yMin, yMax):
                if self.board[y][x] == "-":
                    possiblePlaces.append((x, y))
        return possiblePlaces   
    
    # does an action on the board, whether its a move or a placement
    def doAction(self, action):
        
        # checks for pass
        if action is None:
            pass
        # checks if action is piece placement
        elif isinstance(action[0], int):
            self.addPiece(*action)
        # otherwise move the piece
        else:
            self.movePiece(*action)
        # cycles to next team
        self.enemy_team = self.current_team
        self.current_team = next(self.team_iterator)
        self.turns += 1
        # checks for phase change
        if self.turns == 24 and self.phase == 'placing':
            self.phase = 'moving'
            self.turns = 0
        # checks for board shrink
        elif self.turns in [128, 192]:
            self._shrink_board()
        #print(self.current_team)
        #str(self)
               
    # adds a piece to the board
    def addPiece(self, x, y, piece=None):
        if piece is None:
            piece = self.current_team
            
        kills, killed = 0, 0
        if self.board[y][x] == "-":
            self.board[y][x] = piece
            self.pieces[piece] += 1
            #self.pieces2.get(piece).append((x, y))
            self.updateMovesAround(x, y)
            kills, killed = self._eliminate_about(x, y)
            self.updateMovesAround(x, y)
        return kills, killed   
    
    # moves a piece
    def movePiece(self, moveFrom, moveTo):
        piece = self.board[moveFrom[1]][moveFrom[0]]

        #self.pieces2.get(piece).remove((moveFrom[0], moveFrom[1]))
        #self.pieces2.get(piece).append((moveTo[0], moveTo[1]))
        self.board[moveFrom[1]][moveFrom[0]] = '-'
        self.board[moveTo[1]][moveTo[0]] = piece
        
        self.updateMovesAround(*moveFrom)
        self.updateMovesAround(*moveTo)
        # eliminate
        self._eliminate_about(moveTo[0], moveTo[1])
        # update around
        self.removePieceMoves(piece, *moveFrom)
        self.updateMovesAround(*moveFrom)
        self.updateMovesAround(*moveTo)
    
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
        return 'eh'


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
                if piece in Board.teams:
                    self.removePieceMoves(piece, x, y)
                    self.pieces[piece] -= 1
                    #self.pieces2.get(piece).remove((x, y))
                self.board[y][x] = ' '

        # we have now shrunk the board once more!
        self.n_shrinks = s = s + 1

        # replace the corners (and perform corner elimination)
        for corner in [(s, s), (s, 7 - s), (7 - s, 7 - s), (7 - s, s)]:
            x, y = corner
            piece = self.board[y][x]
            if piece in Board.teams:
                self.removePieceMoves(piece, x, y)
                #self.pieces2.get(piece).remove((x, y))
                self.pieces[piece] -= 1
            self.board[y][x] = 'X'
            self.updateMovesAround(x, y)
            self._eliminate_about(x, y)
            
        # redo all piece moves
        for team in Board.teams:
            for piece in self.pieceMoves[team]:
                self.updateMovesAt(x, y)

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
        return hash(str(self))


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
                    # remove their moves and update around
                    self.board[target_y][target_x] = '-'
                    self.removePieceMoves(targetval,target_x, target_y)
                    self.updateMovesAround(target_x, target_y)
                    self.pieces[targetval] -= 1
                    #update around here
                    #self.pieces2.get(targetval).remove((target_x, target_y))
                    gotKill = 1

        gotKilled = 0
        # Check if the current piece is surrounded and should be eliminated
        if piece in Board.teams:
            if self._surrounded(x, y, 1, 0) or self._surrounded(x, y, 0, 1):
                # remove its moves and update around
                self.board[y][x] = '-'
                self.updateMovesAround(x, y)
                self.removePieceMoves(piece, x, y)
                #self.pieces2.get(piece).remove((x, y))
                self.pieces[piece] -= 1
                gotKilled = 1
            else:
                # or just update its moves
                self.updateMovesAround(x, y)

        return gotKill, gotKilled

    def find_traps(self, piece):
        traps = 0
        for square in self._squares_with_piece(piece):
            for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                ax = square[0] + 2*dx
                bx = square[1] + 2*dy

                cx = square[0] + dx
                dx = square[1] + dy
                # include corners for ally traps
                if self._within_board(ax, bx) and \
                        (self.board[bx][ax] == piece or self.board[bx][ax] == 'X') and self.board[dx][cx] == "-":
                    if self.board[bx][ax] == piece:
                        traps += 0.5
                    else:
                        traps+= 1
        return traps

    def count_kill_positions(self, piece):
        killPositions = 0

        for square in self._squares_with_piece(piece):
            x = square[0]
            y = square[1]
            for direction in [(1, 0), (0, 1)]:
                dx = direction[0]
                dy = direction[1]
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

                surroundedSides = 0

                if firstval in enemies:
                    surroundedSides += 1
                if secondval in enemies:
                    surroundedSides += 1
                if surroundedSides == 1 and (firstval == "-" or secondval == "-"):
                    killPositions += 1

        return killPositions

    def evaluateBoard(self, playerPiece):
        player = playerPiece
        enemy = None
        score = 0

        if player == "W":
            enemy = "B"
        elif player == "B":
            enemy = "W"

        # Our traps
        score += self.find_traps(player)

        # Enemy traps
        score -= self.find_traps(enemy)

        # Positions to kill player
        score -= self.count_kill_positions(player)

        # Positions to kill enemy
        score += self.count_kill_positions(enemy)

        for square in self.pieceMoves[player]:
            # value squares as close to the middle as possible
            score -= (abs(4-square[0]) + abs(4-square[1]))
            # if square[0] in badSquares or square[1] in badSquares:
            #     score -= 3
            # if square[0] in goodSquares or square[1] in goodSquares:
            #     score += 4


        # Player pieces
        score += sum(4 for square in self._squares_with_piece(player))

        # Enemy piece
        score -= sum(3 for square in self._squares_with_piece(enemy))

        return score


    def _enemies(self, piece):
        """
        Which pieces can eliminate a piece of this type?

        :param piece: the type of piece ('B', 'W', or 'X')
        :return: set of piece types that can eliminate a piece of this type
        """
        if piece == 'B':
            return {'W', 'X'}
        elif piece == 'W':
            return {'B', 'X'}
        return set()

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

    def check_winner(self):
        """
        Check the board to see if the game has concluded.

        Count the number of pieces remaining for each player: if either player 
        has run out of pieces, decide the winner and transition to the 
        'completed' state
        """
        n_whites = self.pieces['W']
        n_blacks = self.pieces['B']
        winner = None
        if self.phase == 'moving':
            if n_whites >= 2 and n_blacks >= 2:
                winner = None
            elif n_whites < 2 and n_blacks >= 2:
                winner = 'B'
            elif n_blacks < 2 and n_whites >= 2:
                winner = 'W'
            elif n_whites < 2 and n_blacks < 2:
                winner = 'draw'
        return winner
