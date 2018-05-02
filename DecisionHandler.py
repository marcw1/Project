from Node import Node
from Board import Board
from heapq import *

class DecisionHandler:

	team = None
	maxDepth = None

	def __init__(self, team, maxDepth):
		self.team = team
		self.maxDepth = maxDepth

	# heuristic function h(n), currently no. of black pieces
	def estCostToGoal(self, node):
		blackPieces = node.board.blackPieces
		return len(blackPieces)


	#returns list of moves needed to massacre black team
	def massacre(self, board):

		fringe = []
		expanded = {}
		moves = []
		done = False
		start = Node(None, 0, 0, board, None)
		start.total = self.estCostToGoal(start)
		heappush(fringe, start)


		while len(fringe) > 0 and not done:

			current = heappop(fringe)
			children = current.expand()

			for child in children:
				if hash(child) in expanded or child.cost > self.maxDepth:
					pass
				else:
					# checks if we have reached the goal
					if self.estCostToGoal(child) == 0:
						done = True
						moves = self.getMovesList(child)
						break
					child.total = self.estCostToGoal(child) + child.cost
					expanded[hash(child)] = 1
					heappush(fringe, child)

		return moves


	# returns list of moves to reach goal
	def getMovesList(self, goal):
		moves = []
		current = goal
		while current.pred != None:
			moves.append(current.move)
			current = current.pred
		return reversed(moves)
