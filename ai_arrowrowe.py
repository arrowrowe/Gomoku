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
        # 记录落子即胜的点
        self.has_four = [[], []]
        # 记录落子就会产生 has_four 的点
        self.has_three = [[], []]
        # 评分常数
        self.value_constants = [0, 1, 2, 12, 32, 64, 128]

    def echo(self, text):
        pass
        # print(text)

    def board_get(self, i, j):
        if 0 <= i < self.n and 0 <= j < self.n:
            return self.board[i][j]
        else:
            return -1

    def move_to_last(self, x, y, dx, dy):
        tx = x + dx
        ty = y + dy
        tn = 0
        while 0 <= tx < self.n and 0 <= ty < self.n:
            if self.board[tx][ty] != self.board[x][y]:
                return tn, tx, ty, self.board[tx][ty] is None and self.board_get(tx + dx, ty + dy) == self.board[x][y]
            tx += dx
            ty += dy
            tn += 1
        return tn, None, None, None

    def put(self, x, y, index):
        self.board[x][y] = index
        self.clean(x, y, index)
        fit = lambda p1, p2: p1 == True and p2 != True
        for dx, dy in [(-1, 0), (-1, 1), (0, 1), (1, 1)]:
            un, ux, uy, up = self.move_to_last(x, y, dx, dy)
            vn, vx, vy, vp = self.move_to_last(x, y, -dx, -dy)
            s = un + vn + 1
            if ux is not None:
                self.think[index][ux][uy] += self.value_constants[s]
            if vx is not None:
                self.think[index][vx][vy] += self.value_constants[s]
            if fit(up, vp):
                self.think[index][ux][uy] += self.value_constants[s + 1] - self.value_constants[s]
            if fit(vp, up):
                self.think[index][vx][vy] += self.value_constants[s + 1] - self.value_constants[s]
            if s >= 4:
                if self.board_get(ux, uy) is None:
                    self.echo('Find kill for u at (%d, %d)' % (ux, uy))
                    self.has_four[index].append((ux, uy))
                if self.board_get(vx, vy) is None:
                    self.echo('Find kill for v at (%d, %d)' % (vx, vy))
                    self.has_four[index].append((vx, vy))
            elif s == 3:
                if self.board_get(ux, uy) is None and self.board_get(vx, vy) is None:
                    self.has_three[index].append(
                        (
                            (ux, uy), (vx, vy)
                        )
                    )
                if fit(up, vp):
                    self.echo('Find kill for u jump at (%d, %d)' % (ux, uy))
                    self.has_four[index].append((ux, uy))
                if fit(vp, up):
                    self.echo('Find kill for v jump at (%d, %d)' % (vx, vy))
                    self.has_four[index].append((vx, vy))
        self.clean(x, y, 1 - index)

    def clean(self, x, y, index):
        if (x, y) in self.has_four[index]:
            self.has_four[index].remove((x, y))
        self.has_three[index] = filter(lambda three: three[0] != (x, y) and three[1] != (x, y), self.has_three[index])

    def value(self, i, j):
        return self.think[self.index][i][j] * 1 + self.think[1 - self.index][i][j] * 2

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
        if len(self.has_four[self.index]) > 0:
            i, j = self.has_four[self.index][0]
            self.echo('I win at (%d, %d)!' % (i, j))
        elif len(self.has_four[1 - self.index]) > 1:
            return None
        elif len(self.has_four[1 - self.index]) == 1:
            i, j = self.has_four[1 - self.index][0]
            self.echo('Defend at (%d, %d)!' % (i, j))
        elif len(self.has_three[self.index]) > 0:
            i, j = self.has_three[self.index][0][0]
            self.echo('Check at (%d, %d)!' % (i, j))
        else:
            i, j = self.find_max()
        self.put(i, j, self.index)
        return i, j

    def start(self):
        self.put(self.n / 2, self.n / 2, self.index)
        return self.n / 2, self.n / 2