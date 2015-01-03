from optparse import OptionParser
import ai_arrowrowe as ai0
import ai_sway as ai1
import ai_user as ai2
import colorama

def contest():
    contest_once(17, ai0, ai0)
    contest_once(17, ai1, ai0)

def contest_once(n, ai_black, ai_white):
    print(colorama.Fore.YELLOW + colorama.Style.DIM + '=' * ((n + 1) * 4) + colorama.Style.RESET_ALL)
    colors = [colorama.Fore.BLUE + colorama.Style.BRIGHT, colorama.Fore.RED + colorama.Style.BRIGHT]
    colors_bg = [colorama.Back.CYAN, colorama.Back.YELLOW]
    players = [
        ai_black.Gomoku(n=n, index=0),
        ai_white.Gomoku(n=n, index=1)
    ]
    titles = ['Player %s%s%s' % (c, colorama.Style.BRIGHT, p.name) + colorama.Style.RESET_ALL for p, c in zip(players, colors)]
    board = Chessboard(
        n=n,
        color_black=colors[0],
        color_black_bg=colors_bg[0],
        color_white=colors[1],
        color_white_bg=colors_bg[1]
    )
    result = players[0].start()
    result_by_index = 0
    while True:
        if result is None:
            judge = None
            break
        x, y = result
        judge = board.move(x, y, result_by_index)
        if judge is not None:
            break
        # print('Player [%s] moves (%2d,%2d).' % (players[result_by_index].name, x, y))
        result_by_index = 1 - result_by_index
        result = players[result_by_index].receive(x, y)
    print(str(board))
    if judge == 0:
        print('%s fouls when trying (%2d,%2d).' % (titles[result_by_index], x, y))
        return 1 - result_by_index
    elif judge == 1:
        print('%s wins with (%2d,%2d)!' % (titles[result_by_index], x, y))
        return result_by_index
    elif judge == -1:
        print('Draw after %s moving (%2d,%2d).' % (titles[result_by_index], x, y))
        return -1
    else:
        print('%s throws in the towel.' % titles[result_by_index])
        return 1 - result_by_index

class Chessboard:
    def __init__(self, n, color_black, color_black_bg, color_white, color_white_bg):
        self.colors = [color_black, color_white]
        self.colors_bg = [color_black_bg, color_white_bg]
        self.n = n
        self.data = [[None] * self.n for i in xrange(self.n)]
        self.step_count = 0

    def __str__(self):
        return self.history(self.step_count)

    def history(self, step_count):
        return ('    ' + colorama.Fore.YELLOW + colorama.Style.DIM + '|'.join('%3d' % i for i in xrange(self.n)) + '\n') +\
            '\n'.join(
                (
                    colorama.Fore.YELLOW + colorama.Style.DIM + '%3d|' % row_index + colorama.Style.RESET_ALL +
                    '|'.join(
                        '   '
                        if (grid is None or grid.step > step_count) else
                        grid.str(self.colors_bg[grid.index] if grid.step == step_count else '')
                        for grid in row
                    )
                ) for row_index, row in enumerate(self.data)
            )

    def move(self, x, y, index):
        self.step_count += 1
        if not (0 <= x < self.n and 0 <= y < self.n and self.data[x][y] is None):
            return 0
        self.data[x][y] = Grid(self.step_count, index, self.colors[index])
        for dx, dy in [(-1, 0), (-1, 1), (0, 1), (1, 1)]:
            if self.direction_test(x, y, dx, dy) + self.direction_test(x, y, -dx, -dy) >= 4:
                self.data[x][y].active = True
                self.direction_test(x, y, dx, dy, True)
                self.direction_test(x, y, -dx, -dy, True)
                return 1
        if self.step_count >= self.n ** 2:
            return -1
        else:
            return None

    def direction_test(self, x, y, dx, dy, active=None):
        tx, ty = x + dx, y + dy
        tn = 0
        while 0 <= tx < self.n and 0 <= ty < self.n and self.data[tx][ty] is not None:
            if self.data[tx][ty].index == self.data[x][y].index:
                if active is not None:
                    self.data[tx][ty].active = active
                tn += 1
            else:
                break
            tx += dx
            ty += dy
        return tn

class Grid:
    def __init__(self, step, index, color):
        self.step = step
        self.index = index
        self.color = color
        self.active = False

    def __str__(self):
        return self.str()

    def str(self, bg=''):
        return '%s%s%3d%s' % (self.color, bg, self.step, colorama.Style.RESET_ALL)


colorama.init()

if __name__ == '__main__':
    args = OptionParser().parse_args()[1]
    if len(args) == 0:
        contest()
    elif len(args) == 1:
        if args[0] in ['0', '1']:
            aix = eval('ai%s' % args[0])
            contest_once(17, aix, aix)
        else:
            print('Wrong Input.')
    elif len(args) == 2:
        if args[0] in ['0', '1', '2'] and args[1] in ['0', '1', '2']:
            aix = eval('ai%s' % args[0])
            aiy = eval('ai%s' % args[1])
            contest_once(17, aix, aiy)
        else:
            print('Wrong Input.')