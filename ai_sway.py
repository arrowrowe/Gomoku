class Gomoku:
    def __init__(self, n, index, name='sway'):
        self.n = n
        self.index = index
        self.name = name
        self.board = [ [0] * n for i in xrange(n) ]
    def receive(self, x, y):
        self.board[x][y] = 1
        return 0, 0
    def start(self):
        return n / 2, n / 2
