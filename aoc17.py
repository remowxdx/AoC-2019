#!/usr/bin/env python3

from aoc import *

from computer import Computer

pd = Debug(False)
DAY = 17

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [int(c) for c in lines[0].split(',')]

class Camera:
    def __init__(self, computer):
        self.computer = computer
        self.view = []

    def get_view(self):
        r = self.computer.run()
        self.view = self.computer.get_output()
        return self.view

    def __str__(self):
        return ''.join([chr(c) for c in self.view])

class Maze:
    def __init__(self, camera):
        x = 0
        y = 0
        self.maze = {}
        self.limits = [0, 0]
        self.directions = ['^', '<', 'v', '>']
        self.direction = 0
        self.path = []
        self.pos = (0,0)
        for p in camera.view:
            if x > self.limits[0]: self.limits[0] = x
            if y > self.limits[1]: self.limits[1] = y
            if chr(p) == '#':
                self.maze[(x,y)] = '#'
            elif chr(p) in self.directions:
                pd('Robot found.')
                self.maze[(x,y)] = '#'
                self.pos = (x,y)
                self.direction = self.directions.index(chr(p))
            elif chr(p) == '\n':
                y += 1
                x = -1
            x += 1

    def get_pos(self, p):
        if p in self.maze:
            return self.maze[p]
        return ' '

    def turn(self, direction):
        if direction == 'L':
            self.direction = (self.direction + 1) % 4
        elif direction == 'R':
            self.direction = (self.direction - 1) % 4
        else:
            raise Exception('Unknown direction.')

    def step(self):
        if self.direction == 0:
            pos = (self.pos[0], self.pos[1]-1)
        elif self.direction == 1:
            pos = (self.pos[0]-1, self.pos[1])
        elif self.direction == 2:
            pos = (self.pos[0], self.pos[1]+1)
        elif self.direction == 3:
            pos = (self.pos[0]+1, self.pos[1])

        if pos not in self.maze:
            raise Exception('Falled off.')

        self.maze[pos] = '\u2588'

        self.pos = pos

    def move(self, steps):
        for s in range(steps):
            self.step()

    def align(self):
        a = 0
        for p in self.maze:
            if (p[0]+1, p[1]) in self.maze and \
                    (p[0]-1, p[1]) in self.maze and \
                    (p[0], p[1]+1) in self.maze and \
                    (p[0], p[1]-1) in self.maze:
                a += p[0] * p[1]
        return a

    def follow_path(self, path):
        for d, steps in path:
            self.turn(d)
            self.move(steps)
            pd(self)

    def set_routines(self, routines):
        self.routines = routines

    def follow_routines(self, routines):
        for r in routines:
            self.follow_path(self.routines[r])

    def __str__(self):
        s = []
        for y in range(self.limits[1]+1):
            row = ''
            for x in range(self.limits[0]+1):
                if (x,y) == self.pos:
                    row += self.directions[self.direction]
                    continue
                c = self.get_pos((x,y))
                row += c
            s.append(row)
        return '\n'.join(s)

def test1(data):
    return 0

def test2(data):
    return 0

def part1(data):
    c = Computer(data.copy())
    cam = Camera(c)
    cam.get_view()
    m = Maze(cam)
    return m.align()

def part2(data):

    routine_seq = ['A', 'B', 'A', 'C', 'B', 'C', 'B', 'C', 'A', 'B']
    routine_def = {'A': [('L', 6), ('L', 4), ('R', 8)], # A
        'B': [('R', 8), ('L', 6), ('L', 4), ('L', 10), ('R', 8)], # B
        'C': [('L', 4), ('R', 4), ('L', 4), ('R', 8)],} # C

    c = Computer(data.copy())
    c.memory[0] = 2
    r = c.run()
    r = c.recv()
    while r is not None:
        print(chr(r), end='')
        r = c.recv()

    # send routine sequence
    first = True
    for r in routine_seq:
        if not first:
            c.send(44)
        else:
            first = False
        c.send(ord(r))
    c.send(10)

    r = c.recv()
    while r is not None:
        print(chr(r), end='')
        r = c.recv()

    r = c.run()
    pd(r)
    # send routine definitions
    for r in ['A', 'B', 'C']:
        first = True
        for d, step in routine_def[r]:
            if not first:
                c.send(44)
            else:
                first = False
            c.send(ord(d))
            c.send(44)
            if step < 10:
                c.send(step + ord('0'))
            else:
                c.send(ord('1'))
                c.send(ord('0'))
        c.send(10)
        r = c.run()
        r = c.recv()
        while r is not None:
            print(chr(r), end='')
            r = c.recv()

    # no feedback
    c.send(ord('n'))
    c.send(10)

    r = c.run()
    pd(r)
    r = c.recv()
    while r is not None and r < 128:
        print(chr(r), end='')
        r = c.recv()

    # print( ''.join([chr(c) for c in r if c < 128]))
    return r

if __name__ == '__main__':

#    test_input_1 = get_input(f'input{DAY}')
#    print('Test Part 1:')
#    test_eq('Test 1.1', test1, 42, test_input_1)
#    print()
#
#    test_input_2 = [4,5,6]
#    print('Test Part 2:')
#    test_eq('Test 2.1', test2, 42, test_input_1)
#    print()

    data = get_input(f'input{DAY}')

    r = part1(data)
    if r is not None:
        print('Part 1:', r)
        check_solution(DAY, 1, r)

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        check_solution(DAY, 2, r)
