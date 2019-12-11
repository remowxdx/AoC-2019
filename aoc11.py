#!/usr/bin/env python3

from aoc import *
from computer import Computer

pd = Debug(False)
DAY = 11

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    s = lines[0].strip().split(',')
    return [int(i) for i in s]

def test1(data):
    return 0

def test2(data):
    return 0

def move(pos, dir):
    if dir == '^':
        return (pos[0], pos[1]+1)
    elif dir == 'v':
        return (pos[0], pos[1]-1)
    elif dir == '>':
        return (pos[0]+1, pos[1])
    elif dir == '<':
        return (pos[0]-1, pos[1])
    else:
        raise Exception('Unknown direction')

def part1(data):
    turns = ['^', '>', 'v', '<']
    painted = {}
    c = Computer(data, [0, ])
    pos = (0,0)
    dir = 0
    while (r := c.run()):
        if r == 'HALT':
            return len(painted)
        painted[pos] = c.recv()
        turn = c.recv()
        if turn == 0:
            dir = (dir - 1) % 4
        elif turn == 1:
            dir = (dir + 1) % 4
        else:
            raise Exception(f'Unknown turn: {turn}.')
        pos = move(pos, turns[dir])
        if pos in painted:
            c.send(painted[pos])
        else:
            c.send(0)
        
    return None

def part2(data):
    turns = ['^', '>', 'v', '<']
    painted = {}
    c = Computer(data, [1, ])
    pos = (0,0)
    dir = 0
    while (r := c.run()):
        if r == 'HALT':
            break
        painted[pos] = c.recv()
        turn = c.recv()
        if turn == 0:
            dir = (dir - 1) % 4
        elif turn == 1:
            dir = (dir + 1) % 4
        else:
            raise Exception(f'Unknown turn: {turn}.')
        pos = move(pos, turns[dir])
        if pos in painted:
            c.send(painted[pos])
        else:
            c.send(0)

    m = [0, 0, 0, 0]
    for p in painted:
        if p[0] < m[0]:
            m[0] = p[0]
        if p[0] > m[1]:
            m[1] = p[0]
        if p[1] < m[2]:
            m[2] = p[1]
        if p[1] > m[3]:
            m[3] = p[1]

    pd(m)
    panels = [ [' ' for x in range(m[1] - m[0] + 1)] for y in range(m[3] - m[2] + 1)]

    for p in painted:
        if painted[p] == 1:
            pd(p, p[0]-m[0], p[1]-m[2])
            panels[p[1]-m[2]][p[0]-m[0]] = '#'

    s = '\n'.join([''.join(line) for line in reversed(panels)])
    return s

if __name__ == '__main__':

    test_input_1 = [1,2,3]
    print('Test Part 1:')
    # test_eq('Test 1.1', test1, 42, test_input_1)
    print()

    test_input_2 = [4,5,6]
    print('Test Part 2:')
    # test_eq('Test 2.1', test2, 42, test_input_1)
    print()

    data = get_input(f'input{DAY}')

    r = part1(data)
    if r is not None:
        print('Part 1:', r)
        check_solution(DAY, 1, r)

    r = part2(data)
    if r is not None:
        print('Part 2:')
        print(r)
        check_solution(DAY, 2, r)
