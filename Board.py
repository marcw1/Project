from Piece import Piece
from Move import Move


class Board:

	size = None


# makes an empty board
	def __init__(self, size):
		self.whitePieces = []
		self.blackPieces = []
		self.cornerPieces = []
		self.pieces = {"O": self.whitePieces, "@": self.blackPieces, \
						"X": self.cornerPieces}
		self.board = [[None] * size for i in range(size)]
		self.size = size


# returns formatted string of current board state
	def __str__(self):
		string = ""
		for i in range(self.size):
			for j in range(self.size):
				piece = self.board[i][j]
				if piece == None:
					string += '-'
				else:
					string += str(piece)
				if j < self.size - 1:
					string += " "
				else:
					string += "\n"
		return string


# checks if 2 boards are equivalent
	def __hash__(self):
		return hash(str(self))


# adds a piece to the board, returns that piece
	def addPiece(self, team, row, col):
		newPiece = Piece(team, (row, col))
		self.board[row][col] = newPiece
		self.pieces[team].append(newPiece)
		return newPiece


# returns the piece at a position on the board
	def getPiece(self, row, col):
		if row < 0 or row >= self.size or col < 0 or col >= self.size:
			raise Exception("Not valid board locaton")
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
		#moves the piece
		pieceToMove = newBoard.board[move.old[0]][move.old[1]]
		newBoard.board[move.old[0]][move.old[1]] = None
		newBoard.board[move.new[0]][move.new[1]] = pieceToMove
		pieceToMove.loc = move.new

		#eliminates pieces
		for step in Move.oneStep(move.new):
			newBoard.eliminate(*step)
		newBoard.eliminate(*move.new)

		return newBoard

# returns manhattan distance between 2 coordinates
	def distance(self, a, b):
		return abs(a[0]-b[0]) + abs(a[1]-b[1])


# returns (nearest piece, dist to location) given a set of pieces and location
	def nearestPiece(self, pieces, row, col):
		dist = self.size*2
		nearest = None
		for piece in pieces:
			pieceDist = self.distance(piece.loc, (row, col))
			if pieceDist <= dist:
				dist = pieceDist
				nearest = piece
		return (nearest, dist)

# returns list of lists of coordinates that will eliminate a piece
	def killSpots(self, piece):
		steps = Move.oneStep(piece.loc)
		team = piece.team
		killspots = []
		# try N-S steps
		try:
			if (self.getPiece(*steps[0]) == None \
			or self.getPiece(*steps[0]).team != team ) \
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
