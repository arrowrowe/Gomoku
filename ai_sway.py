# coding = utf8

def isOwn(p):
    if (p.value == 1):
        return True
    else:
        return False
def isOpp(p):
    if (p.value == -1):
        return True
    else:
        return False

class point:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
    def setSite(self, x, y):
        self.x = x
        self.y = y
    def setVaule(self, value):
        self.value = value
    def display(self):
        print self.value 

class Gomoku:
    
    def __init__(self, n, index, name='sway'):
        self.n = n
        self.index = index
        self.name = name
        self.board = [ [point(0, 0, 0) for j in xrange(self.n)] for i in xrange(self.n) ]
        for i in range(self.n):
            for j in range(self.n):
                self.board[i][j].setSite(i, j)
    
        self.back = [] 
        self.final = point(0, 0, 1)

    # True indicates has found the final point

    def checkOppRow(self, row):
        i = 0
        maxLength = 0
        maxStart = 0
        maxEnd = 0
        while (i < len(row)):
            
            while (i < len(row)) and (not isOpp(row[i])):
                i += 1
            start = i
            
            if (start < len(row)):
                
                while (i < len(row)) and (isOpp(row[i])):
                    i += 1
            
                if (i - start > maxLength) and (i < len(row)):
                    maxLength = i - start
                    maxStart = start
                    maxEnd = i - 1

        if (maxLength == 3):
            if maxStart == 0 and not isOwn(row[maxEnd + 1]):
                self.back.append(row[maxEnd + 1])
            elif maxEnd == len(row) - 1 and not isOwn(row[maxStart - 1]):
                self.back.append(row[maxStart - 1])
            elif maxStart != 0 and maxEnd == len(row)-1 and not isOwn(row[maxEnd + 1]) and not isOwn(row[maxStart - 1]):
                self.final.setSite(row[maxEnd + 1].x, row[maxEnd + 1].y)
                return True

        if (maxLength == 4):
            if maxStart ==  0 and not isOwn(row[maxEnd + 1]):
                self.final.setSite(row[maxEnd + 1].x, row[maxEnd + 1].y)
                return True
            elif maxEnd == len(row) - 1 and not isOwn(row[maxStart - 1]):
                self.final.setSite(row[maxStart - 1].x, row[maxStart - 1].y)
                return True
            elif maxStart != 0 and maxEnd != len(row) - 1:
                if not isOwn(row[maxEnd + 1]):
                    self.final.setSite(row[maxEnd + 1].x, row[maxEnd + 1].y)
                    return True
                elif not isOwn(row[maxStart - 1]):
                    self.final.setSite(row[maxStart -1].x, row[maxStart - 1].y)
                    return True


        return False
    def checkOwnRow(self, row):
        i = 0
        maxLength = 0
        maxStart = 0
        maxEnd = 0
        while (i < len(row)):
            
            while (i < len(row)) and (not isOwn(row[i])):
                i += 1
            start = i
            
            if (start < len(row)):
                
                while (i < len(row)) and (isOwn(row[i])):
                    i += 1
            
                if (i - start > maxLength) and (i < len(row)):
                    maxLength = i - start
                    maxStart = start
                    maxEnd = i - 1

        if maxLength >= 3:
            if maxStart == 0 and not isOpp(row[maxEnd + 1]):
                self.final.setSite(row[maxEnd + 1].x, row[maxEnd + 1].y)
                return True
            elif maxEnd == len(row) -1 and not isOpp(row[maxStart - 1]):
                self.final.setSite(row[maxStart - 1].x, row[maxStart - 1].y)
                return True
            if maxStart != 0 and maxEnd != len(row) - 1:
                if not isOpp(row[maxStart - 1]):
                    self.final.setSite(row[maxStart - 1].x, row[maxStart - 1].y)
                    return True
                elif not isOpp(row[maxEnd + 1]):
                    self.final.setSite(row[maxEnd + 1].x, row[maxEnd + 1].y)
                    return True

        return False
    def receive(self, x, y):
        self.board[x][y].setVaule(-1)
        for i in range(self.n):
            row = []
            for j in range(self.n):
                row.append(self.board[i][j])
            if self.checkOppRow(row) == True:
                print 1
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y

        for j in range(self.n):
            row = []
            for i in range(self.n):
                row.append(self.board[i][j])
            if self.checkOppRow(row) == True:
                print 2
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y

        for k in range(self.n):
            i = 0
            j = k
            row = []
            while i < self.n and j < self.n:
                row.append(self.board[i][j])
                i += 1
                j += 1
            if self.checkOppRow(row) ==  True:
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y
        for k in range(self.n):
            i = k
            j = 0
            row = []
            while i < self.n and j < self.n:
                row.append(self.board[i][j])
                i += 1
                j += 1
            
            if self.checkOppRow(row) ==  True:
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y

        for k in range(self.n):
            i = 0
            j = k
            row = []
            while i >= 0 and j >= 0 and i < self.n and j < self.n:
                row.append(self.board[i][j])
                i -= 1
                j += 1
            if self.checkOppRow(row) ==  True:
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y

        if k in range(self.n):
            i = k
            j = self.n - 1
            row = []
            while i >= 0 and j >= 0 and i < self.n and j < self.n:
                row.append(self.board[i][j])
                i -= 1
                j += 1
            if self.checkOppRow(row) ==  True:
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y




        #check the own
        for i in range(self.n):
            row = []
            for j in range(self.n):
                row.append(self.board[i][j])
            if self.checkOwnRow(row) == True:
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y

        for j in range(self.n):
            row = []
            for i in range(self.n):
                row.append(self.board[i][j])
            if self.checkOwnRow(row) == True:
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y

        for k in range(self.n):
            i = 0
            j = k
            row = []
            while i < self.n and j < self.n:
                row.append(self.board[i][j])
                i += 1
                j += 1
            if self.checkOwnRow(row) ==  True:
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y
        for k in range(self.n):
            i = k
            j = 0
            row = []
            while i < self.n and j < self.n:
                row.append(self.board[i][j])
                i += 1
                j += 1
            
            if self.checkOwnRow(row) ==  True:
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y

        for k in range(self.n):
            i = 0
            j = k
            row = []
            while i >= 0 and j >= 0 and i < self.n and j < self.n:
                row.append(self.board[i][j])
                i -= 1
                j += 1
            if self.checkOwnRow(row) ==  True:
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y

        if k in range(self.n):
            i = k
            j = self.n - 1
            row = []
            while i >= 0 and j >= 0 and i < self.n and j < self.n:
                row.append(self.board[i][j])
                i -= 1
                j += 1
            if self.checkOwnRow(row) ==  True:
                self.board[self.final.x][self.final.y].setVaule(1)
                return self.final.x, self.final.y


        for i in range(self.n):
            for j in range(self.n):
                if not isOwn(self.board[i][j]) and not isOpp(self.board[i][j]):
                    self.board[i][j].setVaule(1)
                    return i, j
        return 0, 0
    def start(self):
        self.board[self.n / 2][self.n / 2].setVaule(1)
        return self.n / 2, self.n / 2
