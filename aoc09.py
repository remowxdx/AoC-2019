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

def test1(program):
    c = Computer(program.copy())
    r = c.run()
    while r  != 'HALT':
        r = c.run()
    return c.get_output()

def test2(program):
    c = Computer(program.copy())
    r = c.run()
    while r  != 'HALT':
        r = c.run()
    return len(str(c.recv()))

def part1(program, test_mode):
    c = Computer(program.copy(), [test_mode, ])
    r = c.run()
    while r  != 'HALT':
        r = c.run()
    res = c.get_output()
    if len(res) > 1:
        return r
    return res[0]

def part2(program, test_mode):
    c = Computer(program.copy(), [test_mode, ])
    r = c.run()
    while r  != 'HALT':
        r = c.run()
    res = c.get_output()
    if len(res) > 1:
        return r
    return res[0]

if __name__ == '__main__':
    test_program_1 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    test_program_2 = [1102,34915192,34915192,7,4,7,99,0]
    test_program_3 = [104,1125899906842624,99]
    print('Test Intcode new features')
    test_eq('Test 1.1', test1, test_program_1, test_program_1)
    test_eq('Test 1.2', test2, 16, test_program_2)
    test_eq('Test 1.3', test1, [1125899906842624, ], test_program_3)
    print()

    data = get_input('input9')

    r = part1(data, 1)
    print(f'Part 1: {r}')
    check_solution(9, 1, r)

    print()
    r = part2(data, 2)
    print(f'Part 2: {r}')
    check_solution(9, 2, r)
