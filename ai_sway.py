#coding = utf8
#define 0 : no chess
#define 1 : another chess
#define 2 : my chess
losed = ["11111", "011110"]
#lose: if i don't stop it, i will lose
loses = ["01110", "011010", "010110", "01111", "11110", "11011", "10111", "11101"]
wined = ["22222"]

#when I am attacking, I will get all the values in the board and try the best
valuePatterns = [
    "02220", "022020", "020220", "02222", "22220", "22022", "20222", "22202",   #if another don't stop it i will win
    "002200","000221","122000", "002201", "102200", "02020", "122200","002221", "20022", "22002", "020221", "022021", "122020", "120220",
    "210000", "000012", "210002", "200012", "01210", "211000", "000112", "211002", "200112", "21102", "20112", "201102", "211120", "021112"]
value = [
        8, 8, 8, 11, 11, 11, 11, 11,
        2, 1, 1, 2, 2, 2, 3, 3, 2, 2, 3, 3, 3, 3,
        0.4, 0.4, 0.5, 0.5, 1.9, 1.7, 1.7, 1.5, 1.5, 1.4, 1.4, 1.5, 3.1, 3.1]
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
    def __init__(self, n, index, wordy=False, name="sway"):
        self.n = n
        self.index = index
        self.wordy = wordy
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
    #find the number of patterns in all board
    def find(self, patterns):
        total = 0
        for pattern in patterns:
            for str in self.horBoard:
                total += str.count(pattern)
            for str in self.verBoard:
                total += str.count(pattern)
            for str in self.addDigBoard:
                total += str.count(pattern)
            for str in self.subDigBoard:
                total += str.count(pattern)
        return total
    #find the normal value
    def findValue(self, x, y):
        total = 0
        for i in range(len(valuePatterns)):
            total += value[i] * (self.horBoard[x].count(valuePatterns[i]) + self.verBoard[y].count(valuePatterns[i]) + self.addDigBoard[x + y].count(valuePatterns[i]) + self.subDigBoard[x - y + self.n - 1].count(valuePatterns[i]))
        return total
    def changeBoard(self, x, y, type):
        self.horBoard[x] = strReplace(self.horBoard[x], y, type)
        self.verBoard[y] = strReplace(self.verBoard[y], x, type)
        self.addDigBoard[x + y] = strReplace(self.addDigBoard[x + y], norToAddDig(x, y, self.n), type)
        self.subDigBoard[x - y + self.n - 1] = strReplace(self.subDigBoard[x - y + self.n - 1], norToSubDig(x, y, self.n), type)
    def receive(self, x, y):
        self.changeBoard(x, y, '1')
        #find some places can win right away
        for i in range(self.n):
            for j in range(self.n):
                if self.horBoard[i][j] == '0':
                    self.changeBoard(i, j, '2')
                    if self.find(["22222"]) > 0:
                        return i,j
                    self.changeBoard(i, j, '0')
        #find some places can lose right away
        for i in range(self.n):
            for j in range(self.n):
                if self.horBoard[i][j] == '0':
                    self.changeBoard(i, j, '1')
                    if self.find(["11111"]) > 0:
                        self.changeBoard(i, j, '2')
                        return i, j
                    self.changeBoard(i, j, '0')
        #find some places can win with one step
        for i in range(self.n):
            for j in range(self.n):
                if self.horBoard[i][j] == '0':
                    self.changeBoard(i, j, '2')
                    if self.find(["022220"]) > 0:
                        return i, j
                    self.changeBoard(i, j, '0')
        #find some places can lose with one step
        for i in range(self.n):
            for j in range(self.n):
                if self.horBoard[i][j] == '0':
                    self.changeBoard(i, j, '1')
                    if self.find(["011110"]) > 0:
                        self.changeBoard(i, j, '2')
                        return i, j
                    self.changeBoard(i, j, '0')
        #find the max lose value
        max = maxValue(0, 0, 0)
        for i in range(self.n):
            for j in range(self.n):
                if self.horBoard[i][j] == '0':
                    self.changeBoard(i, j, '1')
                    new = maxValue(self.find(loses), i, j)
                    if new.v > max.v:
                        max = new
                    self.changeBoard(i, j, '0')
        #if the max lose value > 2, must stop it otherwise i will lose
        if max.v >= 2:
            self.changeBoard(max.x, max.y, '2')
            return max.x, max.y
        #find the max win value
        max = maxValue(0, 0, 0)
        for i in range(self.n):
            for j in range(self.n):
                if self.horBoard[i][j] == '0':
                    oldV = self.findValue(i, j)
                    self.changeBoard(i, j, '2')
                    newV = self.findValue(i, j)
                    new = maxValue(newV - oldV, i, j)
                    if new.v > max.v:
                        max = new
                    self.changeBoard(i, j, '0')
        self.changeBoard(max.x, max.y, '2')
        return max.x, max.y
    def start(self):
        self.changeBoard(self.n / 2, self.n / 2, '2')
        return self.n / 2, self.n / 2


