#!/usr/bin/env python3

from aoc import *
from computer import *

import time

pd = Debug(False)
SHOW_TO_HUMAN = False
DAY = 13

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [int(c) for c in lines[0].strip().split(',')]

def test1(data):
    return 0

def test2(data):
    return 0

class Game:
    def __init__(self, show=False):
        self.tiles = {}
        self.tile_ids = [' ', '\u2588', '\u25a1', '=', '\u25cb']
        self.limits = [0, 0, 0, 0]
        self.bt = 0
        self.score = 0
        self.ball = (0, 0)
        self.paddle = (0, 0)
        self.show = show
        if show:
            self.clear()

    def display(self, x, y, tile_id):
        if x == -1 and y == 0:
            self.score = tile_id
            if self.show:
                self.print_score(tile_id)
            return

        if x < self.limits[0]:
            self.limits[0] = x
        if x > self.limits[1]:
            self.limits[1] = x
        if y < self.limits[2]:
            self.limits[2] = y
        if y > self.limits[3]:
            self.limits[3] = y

        if tile_id == 3:
            self.paddle = (x, y)

        if tile_id == 4:
            self.ball = (x, y)

        if tile_id == 2:
            if (x,y) in self.tiles:
                if self.tiles[(x,y)] != 2:
                    self.bt += 1
            else:
                self.bt += 1
        else:
            if (x,y) in self.tiles:
                if self.tiles[(x,y)] == 2:
                    self.bt -= 1

        self.tiles[(x,y)] = tile_id
        if self.show:
            self.print_tile_at(x, y, self.tile_ids[tile_id])

    def print_tile_at(self, x, y, t):
        sx = x - self.limits[0] + 1
        sy = y - self.limits[2] + 1
        print(f'\x1b[{sy};{sx}H{t}') #, end='')

    def print_score(self, score):
        l = len(str(score))
        x = (self.limits[1] - self.limits[0] - l) // 2 + 1
        print(f'\x1b[1;{x}H{score}', end='')

    def clear(self):
        print(f'\x1b[1;1H\x1b[J', end='')

    def get_direction(self):
        if SHOW_TO_HUMAN:
            time.sleep(0.02)
        if self.paddle[0] < self.ball[0]:
            return 1
        if self.paddle[0] > self.ball[0]:
            return -1
        return 0
        
def part1(data):
    c = Computer(data)
    g = Game()

    steps = 0

    r = c.run()
    x = c.recv()
    y = c.recv()
    tile_id = c.recv()
    while x is not None:
        g.display(x, y, tile_id)
        steps += 1
        x = c.recv()
        y = c.recv()
        tile_id = c.recv()

    pd('Limits:', g.limits)
    return g.bt

def part2(data):
    c = Computer(data)
    g = Game()

    # Insert coin
    c.memory[0] = 2

    r = c.run()

    while True:
        x = c.recv()
        if x is None:
            if r == 'WAIT':
                j = g.get_direction()
                c.send(j)
                r = c.run()
                x = c.recv()
            else:
                break
        y = c.recv()
        tile_id = c.recv()
        g.display(x, y, tile_id)

    pd(f'\x1b[{g.limits[3]+1};1H{g.limits}')
    pd('Ball:', g.ball)
    pd('Paddle:', g.paddle)
    pd('Blocks:', g.bt)
    return g.score

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

    # x = input('Play')

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        check_solution(DAY, 2, r)
