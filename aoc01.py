#!/usr/bin/env python3

from aoc import *

pd = Debug(False)

def get_input(file_name):
    data = []
    with open(file_name, 'r') as f:
        data = f.readlines()
    return [int(d) for d in data]

def calc_fuel(mass):
    return (mass // 3) - 2

def calc_fuel_fuel(mass):
    sf = 0
    f = calc_fuel(mass)
    while f > 0:
        sf += f
        pd(f)
        f = calc_fuel(f)
    return sf

def part1(data):
    fuel = [calc_fuel(mass) for mass in data]
    sf = sum(fuel)
    return sf

def part2(data):
    fuel = [calc_fuel_fuel(mass) for mass in data]
    sf = sum(fuel)
    return sf # 5041680

if __name__ == '__main__':

    data = get_input('input1')

    sf = part1(data)
    print(f'Part 1: {sf}')

    sff = part2(data)
    print(f'Part 2: {sff}')

