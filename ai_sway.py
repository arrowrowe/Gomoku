#coding = utf8
#define 0 : no chess
#define 1 : another chess
#define 2 : my chess
losed = ["11111", "011110"]
#lose: if i don't stop it, i will lose
loses = ["01110", "011010", "010110", "01111", "11110", "11011", "10111", "11101"]
wined = ["22222"]
#wins: if another don't stop it i will win
wins = ["02220", "022020", "020220", "02222", "22220", "22022", "20222", "22202"]
#when I am attacking, I will get all the values in the board and try the best
patterns = ["122000", "02200", "002221", "20022", "210000", "210002", "01210","211000", "211002", "21102", "201102", "21112", "022220"]
value = [1, 2, 3, 2, 0.4, 0.4, 1.9, 1.7, 1.5, 1.5, 1.5, 4, 13]
def initDig(i, n):
    if i < n:
        return i + 1
    else:
        return 2 * n - i - 1 
# normal x,y to addDigBoard j
def norToAddDig(x, y, n):
    if x + y < n:
        return x
    else:
        return n - y - 1
def norToSubDig(x, y, n):
    if x - y >= 0:
        return y
    else: 
        return x
def strReplace(str, x, c):
    return str[0:x] + c + str[x+1:len(str)]
class maxValue:
    def __init__(self, v, x, y):
        self.v = v
        self.x = x
        self.y = y
class Gomoku:
    def __init__(self, n, index, name="sway"):
        self.n = n
        self.index = index
        self.name = name
        self.horBoard = [('0' * self.n) for i in xrange(self.n)]
        self.verBoard = [('0' * self.n) for i in xrange(self.n)]
        #x + y = i
        self.addDigBoard = [('0' * (initDig(i, n))) for i in xrange(n * 2 - 1)]
        #x - y + n - 1 = i
        self.subDigBoard = [('0' * (initDig(i, n))) for i in xrange(n * 2 - 1)]
    #find the number of the s in many strings
    def inside(self, x, y):
        if x >= 0 and x < self.n and y >= 0 and y < self.n:
            return True
        else:
            return False
    def find(self, strArray, s):
        total = 0
        for str in strArray:
            total += str.count(s)
        return total
    #find the normal value
    def findValue(self, x, y):
        total = 0
        for i in range(len(patterns)):
            total += value[i] * (self.horBoard[x].count(patterns[i]) + self.verBoard[y].count(patterns[i]) + self.addDigBoard[x + y].count(patterns[i]) + self.subDigBoard[x - y + self.n - 1].count(patterns[i]))
        return total
    def findWin(self):
        total = 0
        for win in wined:
            total += self.find(self.horBoard, win) + self.find(self.verBoard, win) + self.find(self.addDigBoard, win) + self.find(self.subDigBoard, win)
        return total
    def findLose(self):
        total = 0
        for lose in losed:
            total += self.find(self.horBoard, lose) + self.find(self.verBoard, lose) + self.find(self.addDigBoard, lose) + self.find(self.subDigBoard, lose)
        return total
    #to fine how many wins values in one string
    def findWinValue(self):
        total = 0
        for win in wins:
            total += self.find(self.horBoard, win) + self.find(self.verBoard, win) + self.find(self.addDigBoard, win) + self.find(self.subDigBoard, win)
        return total
    #to fine how many loses values in one string
    def findLoseValue(self):
        total = 0
        for lose in loses:
            total += self.find(self.horBoard, lose) + self.find(self.verBoard, lose) + self.find(self.addDigBoard, lose) + self.find(self.subDigBoard, lose)
        return total
    def changeBoard(self, x, y, type):
        self.horBoard[x] = strReplace(self.horBoard[x], y, type)
        self.verBoard[y] = strReplace(self.verBoard[y], x, type)
        self.addDigBoard[x + y] = strReplace(self.addDigBoard[x + y], norToAddDig(x, y, self.n), type)
        self.subDigBoard[x - y + self.n - 1] = strReplace(self.subDigBoard[x - y + self.n - 1], norToSubDig(x, y, self.n), type)
    def receive(self, x, y):
        self.changeBoard(x, y, '1')
        #find some where can win , ps: this one must only check 22222 cause may lost in other's 22222
        for i in range(self.n):
            for j in range(self.n):
                if self.horBoard[i][j] == '0':
                    self.changeBoard(i, j, '2')
                    if self.findWin() > 0:
                        return i,j
                    self.changeBoard(i, j, '0')
        #print('no where can win')
        #find some where can lose
        for i in range(self.n):
            for j in range(self.n):
                if self.horBoard[i][j] == '0':
                    self.changeBoard(i, j, '1')
                    if self.findLose() > 0:
                        self.changeBoard(i, j, '2')
                        return i, j
                    self.changeBoard(i, j, '0')
        #find the max lose value
        #print('no where can lose')
        max = maxValue(0, 0, 0)
        for i in range(self.n):
            for j in range(self.n):
                if self.horBoard[i][j] == '0':
                    self.changeBoard(i, j, '1')
                    new = maxValue(self.findLoseValue(), i, j)
                    if new.v > max.v:
                        max = new
                    self.changeBoard(i, j, '0')
        if max.v >= 2:
            self.changeBoard(max.x, max.y, '2')
            return max.x, max.y
        #find the max win value
        max = maxValue(0, 0, 0)
        for i in range(self.n):
            for j in range(self.n):
                if self.horBoard[i][j] == '0':
                    self.changeBoard(i, j, '2')
                    new = maxValue(6 * self.findWinValue() + self.findValue(i, j), i, j)
                    if new.v > max.v:
                        max = new
                    self.changeBoard(i, j, '0')
        self.changeBoard(max.x, max.y, '2')
        return max.x, max.y
    def start(self):
        self.changeBoard(self.n / 2, self.n / 2, '2')
        return self.n / 2, self.n / 2


