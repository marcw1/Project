from Move import Move

class Piece:
	team = None
	loc = ()

	def __init__(self, team, loc):
		self.team = team
		self.loc = loc
		
	def __str__(self):
		return self.team

	# returns list of possible moves
	def getMoves(self, board):
		moveFrom = self.loc
		moves = []
		oneSteps = Move.oneStep(self.loc)
		for step in oneSteps:
		#try moving one step in every direction
			try:
				piece = board.getPiece(*step)
				if piece == None:
					moves.append(Move(moveFrom, step))
				else:
					step = Move.oneStep(step, oneSteps.index(step))
					try:
						piece = board.getPiece(*step)
						if piece == None:
							moves.append(Move(moveFrom, step))
					except:
						pass
			except:
				pass
		return moves
