#!/usr/bin/env python3

from aoc import *
from computer import Computer

pd = Debug(False)

def get_input(file_name):
    lines = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
    # return [int(d) for d in data]
    raw_data = lines[0].split(',')
    data = [int(d) for d in raw_data]
    return data

def part1(data):
    c = Computer(data.copy(), [1, ])
    c.run()
    r = c.recv()
    while r == 0:
        r = c.recv()
    return r

def part2(data):
    c = Computer(data.copy(), [5, ])
    c.run()
    return c.recv()

def test(data):
    c = Computer(data)
    c.run()
    r = c.memory
    return r

def test_in_out(inp):
    c = Computer([3,0,4,0,99], inp)
    c.run()
    r = c.recv()
    return r

def test_out(data, inp):
    c = Computer(data, inp)
    c.run()
    r = c.recv()
    return r

if __name__ == '__main__':
    print('Test InOut')
    test_eq('InOut1', test_in_out, 1, [1, ])
    test_eq('InOut4', test_in_out, 4, [4, ])
    print()

    print('Test param mode')
    test_eq('ParamMode', test, [1002, 4, 3, 4, 99], [1002, 4, 3, 4, 33])
    data = get_input('input5')

    r = part1(data)
    print(f'Part 1: {r}')

    print()
    print('Test Compare')
    test_eq('Pos 1 == 8', test_out, 0, [3,9,8,9,10,9,4,9,99,-1,8], [4, ])
    test_eq('Pos 8 == 8', test_out, 1, [3,9,8,9,10,9,4,9,99,-1,8], [8, ])
    test_eq('Pos 1 < 8', test_out, 1, [3,9,7,9,10,9,4,9,99,-1,8], [1, ])
    test_eq('Pos 8 < 8', test_out, 0, [3,9,7,9,10,9,4,9,99,-1,8], [8, ])
    test_eq('Pos 9 < 8', test_out, 0, [3,9,7,9,10,9,4,9,99,-1,8], [9, ])

    test_eq('Imm 1 == 8', test_out, 0, [3,3,1108,-1,8,3,4,3,99], [4, ])
    test_eq('Imm 8 == 8', test_out, 1, [3,3,1108,-1,8,3,4,3,99], [8, ])
    test_eq('Imm 1 < 8', test_out, 1, [3,3,1107,-1,8,3,4,3,99], [1, ])
    test_eq('Imm 8 < 8', test_out, 0, [3,3,1107,-1,8,3,4,3,99], [8, ])
    test_eq('Imm 9 < 8', test_out, 0, [3,3,1107,-1,8,3,4,3,99], [9, ])
    print()

    print('Test Jump')
    test_eq('PosJmp 0 is True', test_out, 0, [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0, ])
    test_eq('PosJmp 1 is True', test_out, 1, [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [1, ])
    test_eq('PosJmp -1 is True', test_out, 1, [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [-1, ])
    test_eq('PosJmp 8 is True', test_out, 1, [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [8, ])

    test_eq('ImmJmp 0 is True', test_out, 0, [3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0, ])
    test_eq('ImmJmp 1 is True', test_out, 1, [3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [1, ])
    test_eq('ImmJmp -1 is True', test_out, 1, [3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [-1, ])
    test_eq('ImmJmp 8 is True', test_out, 1, [3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [8, ])

    long_test = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    test_eq('LongTest 7 -> 999', test_out, 999, long_test, [7, ])
    test_eq('LongTest 8 -> 1000', test_out, 1000, long_test, [8, ])
    test_eq('LongTest 9 -> 1001', test_out, 1001, long_test, [9, ])
    print()

    r = part2(data)
    print(f'Part 2: {r}')
