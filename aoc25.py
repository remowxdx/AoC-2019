#!/usr/bin/env python3

from aoc import *
from computer import Computer

pd = Debug(True)
DAY = 25

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [int(c) for c in lines[0].strip().split(',')]

def test1(data):
    return 0

def test2(data):
    return 0

class History:
    def __init__(self, filename):
        self.filename = filename

    def replay(self, c):
        with open(self.filename, 'r') as f:
            r = c.run()
            while r == 'WAIT':
                q = []
                o = c.recv()
                if o > 127:
                    return o
                while o is not None:
                    q.append(chr(o))
                    o = c.recv()
                print(''.join(q))
                a = f.readline()
                if a == '':
                    break
                print(a, end='')
                for i in a:
                    c.send(ord(i))
                r = c.run()
        print(r)
        return None

    def save(self, line):
        if not line.endswith('\n'):
            line += '\n'
        with open(self.filename, 'a') as f:
            f.write(line)
            
def repl(c):
    h = History('hist.txt')
    r = c.run()
    while r == 'WAIT':
        q = []
        o = c.recv()
        while o is not None:
            if o > 127:
                return o
            q.append(chr(o))
            o = c.recv()
        a = input(''.join(q))
        for i in a:
            c.send(ord(i))
        c.send(10)
        h.save(a)
        r = c.run()
    print(r)
    return None

def part1(data):
    c = Computer(data)
    h = History('hist.txt')
    h.replay(c)
    r = repl(c)
    q = []
    o = c.recv()
    while o is not None:
        if o > 127:
            return o
        q.append(chr(o))
        o = c.recv()
    print(''.join(q))
    return ''.join(q[335:343])

def part2(data):
    return None

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
        save_solution(DAY, 2, r)
