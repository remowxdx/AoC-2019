#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = 18

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

class Maze:
    def __init__(self, data):
        self.maze = {}
        self.pos = (0, 0)
        self.keys = {}
        self.steps = 0
        self.visited = {}
        self.parse(data)

    def get_pos(self, pos):
        if pos in self.maze:
            return self.maze[pos]
        return '#'

    def set_pos(self, pos, typ):
        self.maze[pos] = typ

    def offset(self, pos, direction):
        if direction == 0:
            return (pos[0], pos[1]-1)
        elif direction == 1:
            return (pos[0]-1, pos[1])
        elif direction == 2:
            return (pos[0], pos[1]+1)
        elif direction == 3:
            return (pos[0]+1, pos[1])
        else:
            raise Exception('Unknown direction.')


    def peek(self, direction):
        return self.get_pos(self.offset(self.pos, direction))

    def move(self, direction):
        pos = self.offset(self.pos, direction)
        if self.get_pos(pos) == '#':
            raise Exception('Gone into wall.')
        self.pos = pos

    def parse(self, data):

        if type(data) == str:
            data = data.strip().split('\n')

        self.limits = (len(data[0]), len(data))
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                if cell == '#':
                    continue
                if cell == '@':
                    self.pos = (x, y)
                    self.maze[(x,y)] = '.'
                else:
                    self.maze[(x,y)] = cell

    def find_keys(self):
        if self.pos in self.visited:
            return 
        print(self)
        for direction in range(4):
            m = self.peek(direction)
            if m == '#':
                continue

            if m.isupper() and m.lower() not in self.keys:
                continue

            self.move(direction)
            self.steps += 1
            self.visited[self.pos] = self.steps

            if m.islower():
                if m not in self.keys:
                    self.keys[m] = (self.pos, self.steps)
                    tv = self.visited
                    self.visited = {}
                elif self.keys[m][1] > self.steps:
                    self.keys[m] = (self.pos, self.steps)
                    tv = self.visited
                    self.visited = {}
            self.find_keys()
            self.move((direction + 2) % 4)
            self.steps -= 1

            if m.islower():
                self.visited = tv

    def __str__(self):
        r = []
        for y in range(self.limits[1]):
            s = ''
            for x in range(self.limits[0]):
                if self.pos == (x,y):
                    s += '@'
                else:
                    s += self.get_pos((x,y))
            r.append(s)
        return '\n'.join(r)

def test1(data):
    print()
    m = Maze(data)
    print(m)
    m.find_keys()
    max_steps = 0
    for k in m.keys:
        max_steps = max(m.keys[k][1], max_steps)
    return max_steps

def test2(data):
    return 0

def part1(data):
    return None

def part2(data):
    return None

if __name__ == '__main__':

    test_input_1 = '''#########
#b.A.@.a#
#########'''
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 9, test_input_1)
    print()

    test_input_2 = [4,5,6]
    print('Test Part 2:')
    test_eq('Test 2.1', test2, 42, test_input_1)
    print()

    data = get_input(f'input{DAY}')

    r = part1(data)
    if r is not None:
        print('Part 1:', r)
        save_solution(DAY, 1, r)

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        save_solution(DAY, 2, r)
