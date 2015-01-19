import random

class Gomoku:
    def __init__(self, n, index, wordy=False, name='random'):
        self.n = n
        self.index = index
        self.wordy = wordy
        self.name = name

    def random(self):
        return random.randint(0, self.n - 1), random.randint(0, self.n - 1)

    def receive(self, x, y):
        return self.random()

    def start(self):
        return self.random()