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

def search(data, val):
    for noun in range(100):
        for verb in range(100):
            c = Computer(data.copy())
            c.set_addr(1, noun)
            c.set_addr(2, verb)
            c.run()
            if c.get_addr(0) == val:
                pd('Found:', noun, verb)
                pd('Result:', 100 * noun + verb)
                c.show()
                return (noun, verb)
    return False

def part1(data):
    c = Computer(data.copy())
    c.set_addr(1, 12)
    c.set_addr(2, 2)
    c.run()
    return c.get_addr(0)

def part2(data, val):
    noun, verb =  search(data, val)
    return 100 * noun + verb

if __name__ == '__main__':
    # rd = ['1', '0', '0', '0', '99']
    # rd = ['2', '3', '0', '3', '99']
    # rd = ['2', '4', '4', '5', '99', '0']
    # rd = ['1', '1', '1', '4', '99', '5', '6', '0', '99']
    data = get_input('input2')

    r = part1(data)
    print(f'Part 1: {r}')

    r = part2(data, 19690720)
    print(f'Part 2: {r}')
