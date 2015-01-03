class Gomoku:
	def __init__(self, n, index, name='sway'):
		self.n = n
		self.index = index
		self.name = name
		self.k = -1

	def receive(self, x, y):
		self.k += 1
		return self.k, 0

	def start(self):
		self.k = 0
		return 0, 0