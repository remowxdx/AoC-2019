#!/usr/bin/env python3

from aoc import *

from computer import Computer

SHOW_MAZE_WALKING = False

pd = Debug(False)
DAY = 15

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [int(c) for c in lines[0].split(',')]

class Maze:
    def __init__(self):
        self.maze = {(0,0): 1}
        self.pos = (0,0)
        self.limits = [0, 0, 0, 0]
        self.move_command = [
            (0,0), # Stay
            (0,-1), # North
            (0,1), # South
            (-1,0), # West
            (1,0), # East
            ]

    def get_pos(self, pos):
        if pos == self.pos:
            return 4
        if pos in self.maze:
            return self.maze[pos]
        return 3

    def peek_dir(self, direction):
        next = (self.pos[0]+self.move_command[direction][0],
            self.pos[1]+self.move_command[direction][1])
        return self.get_pos(next)

    def set_pos(self, pos, pos_type):
        if pos[0] < self.limits[0]:
            self.limits[0] = pos[0]
        if pos[0] > self.limits[1]:
            self.limits[1] = pos[0]
        if pos[1] < self.limits[2]:
            self.limits[2] = pos[1]
        if pos[1] > self.limits[3]:
            self.limits[3] = pos[1]
        self.maze[pos] = pos_type

    def move(self, direction, status):
        next = (self.pos[0]+self.move_command[direction][0],
            self.pos[1]+self.move_command[direction][1])

        self.set_pos(next, status)
        if status != 0:
            self.pos = next

    def __str__(self):
        pr = ['\u2588', ' ', 'X', '?', 'R', 'O']
        s = []
        for y in range(self.limits[2], self.limits[3]+1):
            row = []
            for x in range(self.limits[0], self.limits[1]+1):
                row.append(pr[self.get_pos((x,y))])
            s.append(''.join(row))
        return '\n'.join(s)

class Robot():
    def __init__(self, data):
        self.c = Computer(data)
        self.maze = Maze()
        self.moves = 0
        self.found = 0
        if SHOW_MAZE_WALKING:
            print('\x1b[2J')

    def move(self, direction):
        self.c.send(direction)
        r = self.c.run()
        r = self.c.recv()
        self.maze.move(direction, r)
        return r

    def explore(self):
        if SHOW_MAZE_WALKING:
            print('\x1b[1;1H')
            print(self.maze)
        back = [2,1,4,3]
        for d in [1,2,3,4]:
            if self.maze.peek_dir(d) == 3:
                r = self.move(d)
                if r != 0:
                    self.moves += 1
                    if r == 2:
                        self.found = self.moves
                    self.explore()
                    self.move(back[d-1])
                    self.moves -= 1
        return self.found

class Oxygen():
    def __init__(self, maze):
        self.maze = maze
        self.oxygen = self.find_oxygen()
        self.maze.pos = self.oxygen
        self.max_moves = 0
        self.moves = 0
        if SHOW_MAZE_WALKING:
            print('\x1b[2J')

    def find_oxygen(self):
        for p in self.maze.maze:
            if self.maze.maze[p] == 2:
                return p
        raise Exception('Cannot find oxygen.')

    def flood(self):
        if SHOW_MAZE_WALKING:
            print('\x1b[1;1H')
            print(self.maze)
        back = [2,1,4,3]
        for d in [1,2,3,4]:
            r = self.maze.peek_dir(d)
            if r == 1:
                r = self.maze.move(d, 5)
                self.moves += 1
                if self.moves > self.max_moves:
                    self.max_moves = self.moves
                self.flood()
                self.maze.move(back[d-1], 5)
                self.moves -= 1
        return self.max_moves
        
def test1(data):
    return 0

def test2(data):
    return 0

def part1(data):
    r = Robot(data)

    m = r.explore()

    pd(r.maze)
    pd(m)
    return m

def part2(data):
    r = Robot(data)

    m = r.explore()

    o = Oxygen(r.maze)
    m = o.flood()
    pd(r.maze)
    pd(m)
    return m

if __name__ == '__main__':

#    test_input_1 = [1,2,3]
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
