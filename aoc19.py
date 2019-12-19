#!/usr/bin/env python3

from aoc import *
from computer import Computer

pd = Debug(False)
DAY = 19

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [int(i) for i in lines[0].strip().split(',')]

def test1(data):
    return 0

def test2(data):
    return 0

def part1(data):
    f = {}
    c = Computer(data)
    m = c.memory
    for y in range(50):
        for x in range(50):
            c.memory = m.copy()
            c.ip = 0
            c.rb = 0
            c.send(x)
            c.send(y)
            c.run()
            f[(x,y)] = c.recv()
    c.run()
    r = c.recv()
    while r != None:
        pd(r, end='-')
        r = c.recv()
    s = 0
    for y in range(50):
        for x in range(50):
            c = f[(x,y)]
            s += c
            pd(c, end='')
        pd()
    return s

def get_xy(c, m, x, y):
    c.memory = m.copy()
    c.ip = 0
    c.rb = 0
    c.send(x)
    c.send(y)
    c.run()
    return c.recv()

def get_diagonal(c, m, x, y):
    r = get_xy(c, m, x, y)
    if r == 0:
        raise Exception('Not good.')
    while r != 0:
        y -= 1
        r = get_xy(c, m, x, y)
    y += 1
    count = 0
    r = get_xy(c, m, x, y)
    while r != 0:
        y += 1
        x -= 1
        r = get_xy(c, m, x, y)
        count += 1
    return (x, y, count)

def part2(data):
    c = Computer(data.copy())
    m = c.memory
    x = 20
    y = x * 11 // 10
    r = get_diagonal(c, m, x, y)
    # Double x while there is a diagonal of length 100
    while r[2] < 100:
        x *= 2
        y = x * 11 // 10
        r = get_diagonal(c, m, x, y)
        pd(r)
    # Binary search to find the limit
    x_l = x // 2
    y_l = x_l * 11 // 10
    x_h = x
    y_h = x_h * 11 // 10
    while x_l < x_h - 1:
        x = (x_l + x_h) // 2
        y = x * 11 // 10
        r = get_diagonal(c, m, x, y)
        pd(r)
        if r[2] < 100:
            x_l = x
        else:
            x_h = x
    pd(r[0],r[1]-100)

    # Scan around to find the smallest (nearest to origin) place
    oks = []
    for x in range(r[0]-5, r[0]+5):
        for y in range(r[1]-105, r[1]-95):
            ok = True
            pd(x,y)
            if get_xy(c, m, x+99, y) == 0:
                ok = False
            if get_xy(c, m, x, y+99) == 0:
                ok = False
            if ok:
                oks.append((x,y))
    x, y = oks[0]
    mini = (x*x + y*y, x, y)
    for x,y in oks:
        d = x*x + y*y
        if d < mini[0]:
            mini = (d, x, y)
    return mini[1] * 10000 + mini[2]

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
