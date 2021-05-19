import chess
import random

class RandomMove():

	def __init__(self,board):
		self.board = board

	def move(self):
		n_moves = board.legal_moves.count()
		i = random.randint(0,n_moves)
		for j,move in enumerate(board.legal_moves):
			if(i == j):
				break
		next_move = move
		return next_move

board = chess.Board()

opponent = RandomMove(board)

while True:
	print(board)
	print("Make a move...")
	legal_move = False
	while not legal_move:
		next_move = input()
		try:
			board.push_san(next_move)
			legal_move = True
		except:
			print("Illegal move, try again...")
	print("Opponent's move")
	board.push(opponent.move())