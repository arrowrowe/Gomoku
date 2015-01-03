# coding: utf-8

class Gomoku:
    def __init__(self, n, index, name='arrowrowe'):
        self.n = n
        self.index = index
        self.name = name
        # 实际落子
        self.board = [[None] * self.n for i in xrange(self.n)]
        # 对每个点的评分, 一方一套评分
        self.think = [
            [[0] * self.n for i in xrange(self.n)]
            for k in xrange(2)
        ]

    def put(self, x, y, index):
        self.board[x][y] = index
        for dx, dy in [(-1, 0), (-1, 1), (0, 1), (1, 1)]:
            tx = x + dx
            ty = y + dy
            self.think[index][tx][ty] += 2
            tx += dx
            ty += dy
            self.think[index][tx][ty] += 1

    def value(self, i, j):
        return self.think[self.index][i][j] * 2 + self.think[1 - self.index][i][j] * 1

    def find_max(self):
        m = 0
        mi, mj = -1, -1
        for i in xrange(self.n):
            for j in xrange(self.n):
                if self.board[i][j] is not None:
                    continue
                v = self.value(i, j)
                if v > m:
                    m = v
                    mi, mj = i, j
        return mi, mj

    def receive(self, x, y):
        self.put(x, y, 1 - self.index)
        i, j = self.find_max()
        self.put(i, j, self.index)
        return i, j

    def start(self):
        self.put(self.n / 2, self.n / 2, self.index)
        return self.n / 2, self.n / 2