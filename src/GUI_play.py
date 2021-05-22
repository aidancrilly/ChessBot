import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as image
from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
	import Tkinter as Tk
else:
	import tkinter as Tk

import chess
import random

class RandomMove():

	def __init__(self,board):
		self.board = board

	def move(self):
		n_moves = self.board.legal_moves.count()
		i = random.randint(0,n_moves)
		for j,move in enumerate(self.board.legal_moves):
			if(i == j):
				break
		next_move = move
		return next_move

class Interface():

	def __init__(self,root,board,opp_type):

		self.board = board
		self.opponent = opp_type(self.board)

		self.root = root
		self.root.wm_title("ChessDisplay")

		self.f = Figure(figsize=(4, 4), dpi=100)
		self.ax1 = self.f.add_subplot(111)
		self.ax1.axis('off')

		self.dx = 56.5
		self.x_offset = 125.0
		self.dy = -56.0
		self.y_offset = 540.0

		img_dir = "../imgs/"

		img = image.imread(img_dir+'board.gif')
		self.ax1.imshow(img)
		self.pieces_plot_list = []

		self.white_p = image.imread(img_dir+'white_p.png')
		self.black_p = image.imread(img_dir+'black_p.png')
		self.white_r = image.imread(img_dir+'white_r.png')
		self.black_r = image.imread(img_dir+'black_r.png')
		self.white_n = image.imread(img_dir+'white_n.png')
		self.black_n = image.imread(img_dir+'black_n.png')
		self.white_b = image.imread(img_dir+'white_b.png')
		self.black_b = image.imread(img_dir+'black_b.png')
		self.white_q = image.imread(img_dir+'white_q.png')
		self.black_q = image.imread(img_dir+'black_q.png')
		self.white_k = image.imread(img_dir+'white_k.png')
		self.black_k = image.imread(img_dir+'black_k.png')

		self.piece_dict = {
		'P' : self.white_p,
		'p' : self.black_p,
		'R' : self.white_r,
		'r' : self.black_r,
		'N' : self.white_n,
		'n' : self.black_n,
		'B' : self.white_b,
		'b' : self.black_b,
		'Q' : self.white_q,
		'q' : self.black_q,
		'K' : self.white_k,
		'k' : self.black_k}

		self.canvas = FigureCanvasTkAgg(self.f, master=root)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

		self._update_plot()

		self.canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

		self.q_button = Tk.Button(master=self.root, text='Quit', command=self._quit, width = 10)
		self.q_button.pack(side=Tk.RIGHT, padx = 10, pady=10)

		self.m_label = Tk.Label(master=self.root, text='Your move:')
		self.m_label.pack(side=Tk.LEFT, padx = 5, pady=10)

		self.m_entry = Tk.Entry(master=self.root, width = 25)
		self.m_entry.pack(side=Tk.LEFT, padx = 5, pady=10)

		self.m_button = Tk.Button(master=self.root, text='Move', command=self._move, width = 10)
		self.m_button.pack(side=Tk.LEFT, padx = 5, pady=10)

		Tk.mainloop()

	def _update_plot(self):
		FEN_rep = self.board.fen()
		for piece in self.pieces_plot_list:
			piece.remove()
		ix = 0
		iy = 0
		self.pieces_plot_list = []
		for char in FEN_rep:
			# End of piece list
			if(char == ' '):
				break
			# Onto next rank
			if(char == '/'):
				iy += 1
				ix = 0
				continue
			# Empty squares
			if(char.isdigit()):
				ix += int(char)
			# There is a piece!
			else:
				ix += 1
				piece = self.f.figimage(self.piece_dict[char],self.dx*ix+self.x_offset,self.dy*iy+self.y_offset)
				self.pieces_plot_list.append(piece)
		self.canvas.draw()

	def _move(self):
		self.proposed_move = self.m_entry.get()
		try:
			self.board.push_san(self.proposed_move)
			legal_move = True
		except:
			legal_move = False
		if(legal_move):
			if(self.board.is_game_over()):
				self.ax1.text(0.5*self.ax1.get_xlim()[-1],0.5*self.ax1.get_ylim()[-1],"Game Over",ha='center',va='center')
			else:
				self.board.push(self.opponent.move())
			if(self.board.is_game_over()):
				self.ax1.text(0.5*self.ax1.get_xlim()[-1],0.5*self.ax1.get_ylim()[-1],"Game Over",ha='center',va='center')
		self.m_entry.delete(0, 'end')
		self._update_plot()

	def _quit(self):
		self.root.quit()	 # stops mainloop
		self.root.destroy()  # this is necessary on Windows to prevent
							 # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def main():
	board = chess.Board()
	root = Tk.Tk()
	root.resizable(width=False, height=False)
	root.geometry('800x800')
	app = Interface(root,board,RandomMove)
	root.mainloop()

if __name__ == '__main__':
	main()  