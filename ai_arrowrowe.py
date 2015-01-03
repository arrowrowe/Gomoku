class Gomoku:
    def __init__(self, n, index, name='arrowrowe'):
        self.n = n
        self.index = index
        self.name = name

    def receive(self, x, y):
        if y < self.n - 1:
            return x, y + 1
        else:
            return None

    def start(self):
        return self.n / 2, self.n / 2