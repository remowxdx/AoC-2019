#!/usr/bin/env python3

from aoc import *

pd = Debug(False)
DAY = 24

def get_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data

class Levels:
    def __init__(self, data):
        self.boards = {0: Board(data)}
        self.empty = '.....\n.....\n..?..\n.....\n.....'
        self.adjs = {
            (0,0): [(-1, 2, 1), (-1, 1, 2), (0, 1, 0), (0, 0, 1)],
            (1,0): [(-1, 2, 1), (0, 0, 0), (0, 2, 0), (0, 1, 1)],
            (2,0): [(-1, 2, 1), (0, 1, 0), (0, 3, 0), (0, 2, 1)],
            (3,0): [(-1, 2, 1), (0, 2, 0), (0, 4, 0), (0, 3, 1)],
            (4,0): [(-1, 2, 1), (0, 3, 0), (-1, 3, 2), (0, 4, 1)],

            (0,1): [(0, 0, 0), (-1, 1, 2), (0, 1, 1), (0, 0, 2)],
            (1,1): [(0, 1, 0), (0, 0, 1), (0, 2, 1), (0, 1, 2)],
            (2,1): [(0, 2, 0), (0, 1, 1), (0, 3, 1), (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0)],
            (3,1): [(0, 3, 0), (0, 2, 1), (0, 4, 1), (0, 3, 2)],
            (4,1): [(0, 4, 0), (0, 3, 1), (-1, 3, 2), (0, 4, 2)],

            (0,2): [(0, 0, 1), (-1, 1, 2), (0, 1, 2), (0, 0, 3)],
            (1,2): [(0, 1, 1), (0, 0, 2), (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 0, 3), (1, 0, 4), (0, 1, 3)],
            (2,2): [],
            (3,2): [(0, 3, 1), (1, 4, 0), (1, 4, 1), (1, 4, 2), (1, 4, 3), (1, 4, 4), (0, 4, 2), (0, 3, 3)],
            (4,2): [(0, 4, 1), (0, 3, 2), (-1, 3, 2), (0, 4, 3)],

            (0,3): [(0, 0, 2), (-1, 1, 2), (0, 1, 3), (0, 0, 4)],
            (1,3): [(0, 1, 2), (0, 0, 3), (0, 2, 3), (0, 1, 4)],
            (2,3): [(1, 0, 4), (1, 1, 4), (1, 2, 4), (1, 3, 4), (1, 4, 4), (0, 1, 3), (0, 3, 3), (0, 2, 4)],
            (3,3): [(0, 3, 2), (0, 2, 3), (0, 4, 3), (0, 3, 4)],
            (4,3): [(0, 4, 2), (0, 3, 3), (-1, 3, 2), (0, 4, 4)],

            (0,4): [(0, 0, 3), (-1, 1, 2),  (0, 1, 4), (-1, 2, 3)],
            (1,4): [(0, 1, 3),  (0, 0, 4),  (0, 2, 4), (-1, 2, 3)],
            (2,4): [(0, 2, 3),  (0, 1, 4),  (0, 3, 4), (-1, 2, 3)],
            (3,4): [(0, 3, 3),  (0, 2, 4),  (0, 4, 4), (-1, 2, 3)],
            (4,4): [(0, 4, 3),  (0, 3, 4), (-1, 3, 2), (-1, 2, 3)],
            }

    def get_bug_in(self, l, x, y):
        if l not in self.boards:
            return 0
        c = self.boards[l].cells[y][x]
        if c == '#':
            return 1
        return 0

    def set_cell(self, l, x, y, cell):
        if l not in self.boards and cell == '#':
            self.boards[l] = Board(self.empty)
        self.boards[l].cells[y][x] = cell

    def adjacent(self, l, x, y):
        b = 0
        if x == 2 and y == 2:
            return 0
        for cell in self.adjs[(x,y)]:
            b += self.get_bug_in(l + cell[0], cell[1], cell[2])
        return b

    def step(self):
        updates = []
        low = min(self.boards) - 1
        self.boards[low] = Board(self.empty)
        hi = max(self.boards) + 1
        self.boards[hi] = Board(self.empty)
        for l in range(low, hi + 1):
            for j, row in enumerate(self.boards[l].cells):
                for i, cell in enumerate(row):
                    a = self.adjacent(l, i, j)
                    if cell == '#' and a != 1:
                        updates.append((l, i, j, '.'))
                    elif cell == '.' and (a == 1 or a == 2):
                        updates.append((l, i, j, '#'))

        for l, i, j, cell in updates:
            self.set_cell(l, i, j, cell)

    def count_bugs(self):
        low = min(self.boards)
        hi = max(self.boards)
        s = 0
        for level in range(low, hi + 1):
            for j, row in enumerate(self.boards[level].cells):
                for i, cell in enumerate(row):
                    s += self.get_bug_in(level, i, j)
        return s

    def __str__(self):
        low = min(self.boards)
        hi = max(self.boards)
        s = []
        for level in range(low, hi + 1):
            s.append(f'Level {level}:\n{self.boards[level]}')
        return '\n'.join(s)

class Board:
    def __init__(self, data):
        self.cells = [[cell for cell in line] for line in data.split('\n')]

    def rating(self):
        r = 0
        f = 1
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if cell == '#':
                    r += f
                f *= 2
        return r

    def adjacent(self, x, y):
        a = 0
        # left
        if x - 1 >= 0:
            if self.cells[y][x-1] == '#':
                a += 1
        # right
        if x + 1 < 5:
            if self.cells[y][x+1] == '#':
                a += 1
        # up
        if y - 1 >= 0:
            if self.cells[y-1][x] == '#':
                a += 1
        # down
        if y + 1 < 5:
            if self.cells[y+1][x] == '#':
                a += 1
        return a

    def step(self):
        cells = [row.copy() for row in self.cells.copy()]
        for j, row in enumerate(cells):
            for i, cell in enumerate(row):
                a = self.adjacent(i, j)
                if cell == '#' and a != 1:
                    cells[j][i] = '.'
                elif cell == '.' and (a == 1 or a == 2):
                    cells[j][i] = '#'
        self.cells = cells

    def __str__(self):
        return '\n'.join([''.join([cell for cell in row]) for row in self.cells])

def test1(data, steps=0):
    b = Board(data)
    for i in range(steps):
        b.step()
    return b.rating()

def test2(data):
    return 0

def part1(data):
    b = Board(data)
    ratings = []
    found = False
    while not found:
        b.step()
        r = b.rating()
        if r in ratings:
            return r
        ratings.append(r)
    return None

def part2(data, steps):
    l = Levels(data)

    for s in range(steps):
        l.step()

    pd('Levels:', len(l.boards))
    pd(l)
    return l.count_bugs()

if __name__ == '__main__':

    test_input_1 = '''.....
.....
.....
#....
.#...'''
    test_input_2 = '''....#
#..#.
#..##
..#..
#....'''
    print('Test Part 1:')
    test_eq('Test 1.1 (rating)', test1, 2129920, test_input_1)
    test_eq('Test 1.2 (steps)', test1, 3165711, test_input_2, 4)
    print()

    print('Test Part 2:')
    test_input_2 = '''....#
#..#.
#.?##
..#..
#....'''
    test_eq('Test 2.1', part2, 99, test_input_2, 10)
    print()

    data = get_input(f'input{DAY}')

    r = part1(data)
    if r is not None:
        print('Part 1:', r)
        check_solution(DAY, 1, r)

    r = part2(data, 200)
    if r is not None:
        print('Part 2:', r)
        check_solution(DAY, 2, r)
