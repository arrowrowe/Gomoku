import gomoku_platform
import colorama

class Gomoku:
    def __init__(self, n, index, wordy=False, name='arrowrowe'):
        self.n = n
        self.index = index
        self.wordy = wordy
        self.name = name
        colors = [colorama.Fore.BLUE + colorama.Style.BRIGHT, colorama.Fore.RED + colorama.Style.BRIGHT]
        colors_bg = [colorama.Back.CYAN, colorama.Back.YELLOW]
        self.board = gomoku_platform.Chessboard(
            n=self.n,
            color_black=colors[0],
            color_black_bg=colors_bg[0],
            color_white=colors[1],
            color_white_bg=colors_bg[1]
        )

    def ask(self, text):
        result = input(text + ': ')
        if result is not None:
            i, j = result
            self.board.move(i, j, self.index)
            print(str(self.board))
        return result

    def receive(self, x, y):
        self.board.move(x, y, 1 - self.index)
        print(str(self.board))
        return self.ask('Your turn after (%d, %d)' % (x, y))

    def start(self):
        return self.ask('Init')