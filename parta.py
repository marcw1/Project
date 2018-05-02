from Board import Board
from Move import Move
from Node import Node
from DecisionHandler import DecisionHandler
BOARDSIZE = 8


def initialise(input):
    mode = input.split("\n")[-1]
    board = createBoard(input)
    if mode == "Moves":
        print(board.countMoves("O"))
        print(board.countMoves("@"))
    elif mode == "Massacre":
        player = DecisionHandler("O", 5)
        killMoves = player.massacre(board)
        for move in killMoves:
            print(move)
    return board

# creates a Board object from the input
def createBoard(input):
	input = input.replace(" ", "")
	input = input.replace("\n", "")
	board = Board(BOARDSIZE)
	boardArray = [list(input[i:i+8]) for i in range(0,64,8)]
	for rowIndex, row in enumerate(boardArray):
		for colIndex, col in enumerate(row):
			if (col != "-"):
			    board.addPiece(col, rowIndex, colIndex)
	return board


# Read input line by line until EOF
lines = []
while True:
    try:
        line = input()
    except EOFError:
        break
    lines.append(line)
boardConfig = '\n'.join(lines)

# Initialise the program based on board configuration
initialise(boardConfig)
