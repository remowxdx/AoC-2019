#!/usr/bin/env python3

from aoc import *
from computer import Computer
import random

pd = Debug(True)
DAY = 21

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [int(c) for c in lines[0].strip().split(',')]

def test1(data):
    return 0

def test2(data):
    return 0

def print_out(c):
    r = c.run()
    i = c.recv()
    while i is not None:
        if i > 127:
            return i
        print(chr(i), end='')
        i = c.recv()
    return None

def send(c, inp, mode='WALK'):
    for i in inp:
        c.send(ord(i))
    for i in f'\n{mode}\n':
        c.send(ord(i))

def build_instructions():
    instructions = ['STOP']
    for operation in ['AND', 'OR', 'NOT']:
        for op1 in ['A', 'B', 'C', 'D', 'T', 'J']:
            for op2 in ['T', 'J']:
                instructions.append(' '.join([operation, op1, op2]))
    return instructions

def p1(c):
    instructions = build_instructions()
    print(instructions)
    print(len(instructions))

    to_send = [
        'NOT C T',
        'AND D T',
        'NOT A J',
        'OR T J',
        'NOT A T',
        'NOT T T',
        'AND B T',
        'AND C T',
        'AND D T',
        'NOT T T',
        'AND T J',
        'NOT T T',
        'NOT T T',
        'NOT T T',
        'NOT T T',
        ]
    xxx = '''NOT C T
AND D T
NOT A J
OR T J
NOT A T
NOT T T
AND B T
AND C T
AND D T
NOT T T
AND T J
AND T J
AND J T
NOT D T
NOT T T
'''
# @
# ==========
#  ABCDEFGHI
# @---|---|
# ==..==.==.
#  ABCDEFGHI
# @---|---|
# ===.=..===
#  ABCDEFGHI
# j if .??? or (??.? and ???#)
# j if NOT A or ( NOT C and D)
# j if NOT A J (NOT C T AND D T)
        #OR T J
    for length in range(15 - len(to_send)):
        n = random.randint(0, len(instructions)-1)
        if n == 0:
            break
        to_send.append(instructions[n])
    print('\n'.join(to_send))
    send(c, '\n'.join(to_send))

def p2(c):
    to_send = [
        'NOT D T',
        'NOT T T',
        'AND H T',
        'NOT A J',
        'OR T J',
        'NOT A T',
        'NOT T T',
        'AND B T',
        'AND C T',
        'AND D T',
        'NOT T T',
        'AND T J',
        ]
# @
# ==========
#  ABCDEFGHI
# @---|---|
# ==..==.==.
#  ABCDEFGHI
# @---|---|
# ===.=..===
#  ABCDEFGHI
    print('\n'.join(to_send))
    send(c, '\n'.join(to_send), 'RUN')

def part1(data):
    c = Computer(data.copy())
    print_out(c)
    p1(c)
    r = print_out(c)
    return r

def part2(data):
    c = Computer(data)
    print_out(c)
    p2(c)
    r = print_out(c)
    return r

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
