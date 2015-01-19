import re
from random import choice

class Gomoku:
    def __init__(self, n, index, wordy=False, name='arrowrowe'):
        self.n = n
        self.index = index
        self.wordy = wordy
        self.name = name
        self.datas = {i + 1: ['0' * self.n] * self.n for i in xrange(2)}
        raw_matchers = [
            # 0, 4=>5 To win
            ['x2222', '2x222', '22x22'],
            # 1, 3=>4 Kill
            ['0x2220', '02x220'],
            # 2, 3=>4 Check
            [
                '0x222($|1)', '02x22($|1)', '022x2($|1)', '0222x($|1)',
                'x0222', '20x22', '202x2', '2022x',
                'x2022', '2x022'
            ],
            # 3, 2=>3 To kill
            [
                '00x2200', '00x220($|1)', '002x200', '002x20($|1)',
                '0x0220', '020x20', '0202x0'
            ],
            # 4, 2=>3 To check
            [
                '00x22($|1)', '002x2($|1)', '0022x($|1)',
                '0x022($|1)', '020x2($|1)', '0202x($|1)',
                '0x202($|1)', '02x02($|1)', '0220x($|1)',
                '0x220($|1)', '02x20($|1)', '022x0($|1)',
                'x0022', '200x2', '2002x',
                'x0202', '20x02',
                'x0220', '20x20', '202x0'
            ],
            # 5, 1=>2 Drop
            [
                '2x', '20x', '200x', '2000x'
            ]
        ]
        self.matchers = [[re.compile(p.replace('x', '(?P<x>0)')) for p in m] for m in raw_matchers]

    def echo(self, text):
        if self.wordy:
            print(text)

    def receive(self, x, y):
        self.put(1, (x, y))
        my_to_win, my_kill, my_double_check, my_check_to_kill, my_check_for_future_check, my_check_for_future_to_kill, my_to_kill_for_future_check, my_double_to_kill, my_to_kill_for_future_to_kill, my_check, my_to_kill, my_to_check, my_drop = self.get_valued_matched(2)
        his_to_win, his_kill, his_double_check, his_check_to_kill, his_check_for_future_check, his_check_for_future_to_kill, his_to_kill_for_future_check, his_double_to_kill, his_to_kill_for_future_to_kill, his_check, his_to_kill, his_to_check, his_drop = self.get_valued_matched(1)
        pos = None
        for poses in [
            'my_to_win',
            'his_to_win',
            'my_double_check', 'my_kill', 'my_check_to_kill',
            'his_double_check', 'his_check_to_kill',
            'my_check_for_future_check',
            'his_check_for_future_check',
            'his_kill',
            'my_check_for_future_to_kill',
            'his_check_for_future_to_kill',
            'my_double_to_kill',
            'his_double_to_kill',
            'my_to_kill_for_future_check',
            'his_to_kill_for_future_check',
            'my_to_kill_for_future_to_kill',
            'his_to_kill_for_future_to_kill',
            'my_to_kill',
            'his_to_kill',
            'my_check',
            'his_check',
            'my_to_check',
            'his_to_check',
            'my_drop',
            'his_drop'
        ]:
            if eval(poses):
                self.echo('Take ' + poses)
                # pos = choice(poses)
                pos = eval(poses)[0]
                break
        if pos:
            self.put(2, pos)
        return pos

    def start(self):
        i = self.n / 2
        self.put(2, (i, i))
        return i, i

    def put(self, index, pos):
        x, y = pos
        self.datas[2][x] = splice(self.datas[2][x], y, 1, str(index))
        self.datas[1][x] = splice(self.datas[1][x], y, 1, str(3 - index))

    def remove(self, pos):
        x, y = pos
        self.datas[2][x] = splice(self.datas[2][x], y, 1, '0')
        self.datas[1][x] = splice(self.datas[1][x], y, 1, '0')

    def get_valued_matched(self, index):
        pos_to_win, pos_kill, pos_double_check, pos_check_to_kill, pos_double_to_kill, pos_check, pos_to_kill, pos_to_check, pos_drop = self.get_seen_matched(index)

        pos_check_for_future_check = []
        pos_check_for_future_to_kill = []
        for pos in pos_check:
            self.echo('Testing (%d, %d)' % pos)
            self.put(index, pos)
            future_pos_to_win, future_pos_kill, future_pos_double_check, future_pos_check_to_kill, future_pos_double_to_kill, future_pos_check, future_pos_to_kill, future_pos_to_check, future_pos_drop = self.get_seen_matched(index)
            if len(future_pos_double_check) + len(future_pos_check_to_kill):
                pos_check_for_future_check.append(pos)
            if len(future_pos_double_to_kill):
                pos_check_for_future_to_kill.append(pos)
            self.remove(pos)

        pos_to_kill_for_future_check = []
        pos_to_kill_for_future_to_kill = []
        for pos in pos_to_kill:
            self.echo('Testing (%d, %d)' % pos)
            self.put(index, pos)
            future_pos_to_win, future_pos_kill, future_pos_double_check, future_pos_check_to_kill, future_pos_double_to_kill, future_pos_check, future_pos_to_kill, future_pos_to_check, future_pos_drop = self.get_seen_matched(index)
            if len(future_pos_double_check) + len(future_pos_check_to_kill):
                pos_to_kill_for_future_check.append(pos)
            if len(future_pos_double_to_kill):
                pos_to_kill_for_future_to_kill.append(pos)
            self.remove(pos)

        return pos_to_win, pos_kill, pos_double_check, pos_check_to_kill, pos_check_for_future_check, pos_check_for_future_to_kill, pos_to_kill_for_future_check, pos_double_to_kill, pos_to_kill_for_future_to_kill, pos_check, pos_to_kill, pos_to_check, pos_drop

    def get_seen_matched(self, index):
        pos_to_win, pos_kill, pos_check, pos_to_kill, pos_to_check, pos_drop = self.get_all_matched(index)
        pos_double_check = pick_double(pos_check)
        pos_check_to_kill = pick_both(pos_check, pos_to_kill)
        pos_double_to_kill = pick_double(pos_to_kill)
        return pos_to_win, pos_kill, pos_double_check, pos_check_to_kill, pos_double_to_kill, pos_check, pos_to_kill, pos_to_check, pos_drop

    def get_all_matched(self, index):
        matched = [[] for i in xrange(len(self.matchers))]
        data = self.datas[index]
        back_fn_for_backslash = lambda (x, y): (y, x - y) if x < self.n else (x + y - self.n + 1, self.n - 1 - y)
        back_fn_for_mirror = lambda (x, y): (x, self.n - 1 - y)
        for transformed_data, back_fn in [
            (
                data,
                lambda pos: pos
            ),
            (
                transpose(data),
                lambda (x, y): (y, x)
            ),
            (
                backslash(data),
                back_fn_for_backslash
            ),
            (
                backslash(mirror(data)),
                lambda pos: back_fn_for_mirror(back_fn_for_backslash(pos))
            )
        ]:
            for matcher_index, poses in enumerate(get_matched(transformed_data, self.matchers)):
                matched[matcher_index].extend(map(back_fn, poses))
        if self.wordy:
            show_matched(self.n, matched)
        return matched


def show_matched(n, matched):
    print
    data = [("." * n + '  ') * len(matched)] * n
    for matcher_index, poses in enumerate(matched):
        for x, y in poses:
            data[x] = splice(data[x], (n + 2) * matcher_index + y, 1, str(int(data[x][(n + 2) * matcher_index + y]) + 1 if data[x][(n + 2) * matcher_index + y] != '.' else 1))
    print '\n'.join(data)


def get_lower(patterns):
    result = []
    for p in patterns:
        p = p.replace('x', '0')
        i = p.find('2')
        while i > -1:
            q = splice(p, i, 1, 'x')
            if q not in result and q[::-1] not in result:
                result.append(q)
            i = p.find('2', i + 1)
    return result


def splice(string, index, length=None, needle=''):
    return string[:index] + needle + string[index + (length or len(needle)):]


def mirror(data):
    return map(lambda s: s[::-1], data)


def transpose(data):
    return map(lambda i: ''.join(row[i] for row in data), xrange(len(data)))


def backslash(data):
    n = len(data)
    return map(
        lambda i: ''.join(
            data[p][i - p] for p in xrange(i + 1)
        ), xrange(n)
    ) + map(
        lambda i: ''.join(
            data[p][n - 1 + i - p] for p in xrange(i, n)
        ), xrange(1, n)
    )


def get_matched(data, matchers):
    mirror_data = mirror(data)
    matched = [[] for i in xrange(len(matchers))]
    for matcher_index, matcher in enumerate(matchers):
        for pattern in matcher:
            poses = filter_double(search_all(data, pattern))
            matched[matcher_index].extend(poses)
            mirror_poses = [
                (pos[0], len(data[pos[0]]) - 1 - pos[1])
                for pos in search_all(mirror_data, pattern)
            ]
            matched[matcher_index].extend(list_minus(mirror_poses, poses))
    matched[3] = filter_double(matched[3])
    return matched


def search_all(data, pattern):
    poses = []
    for row_index, row in enumerate(data):
        i = 0
        r = pattern.search(row)
        while r:
            poses.append((row_index, i + r.start('x')))
            i += r.end()
            row = row[r.end():]
            r = pattern.search(row, i + 1)
    return poses


def pick_double(a):
    return [p for i, p in enumerate(a) if p in a[i + 1:]]


def filter_double(a):
    return [p for i, p in enumerate(a) if p not in a[i + 1:]]


def pick_both(a, b):
    return [p for p in a if p in b]


def list_minus(a, b):
    return [p for p in a if p not in b]