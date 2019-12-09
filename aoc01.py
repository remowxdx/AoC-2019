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

    print('Testing Part 1')
    test_eq('Ex1.1', calc_fuel, 2, 12)
    test_eq('Ex1.2', calc_fuel, 2, 14)
    test_eq('Ex1.3', calc_fuel, 654, 1969)
    test_eq('Ex1.4', calc_fuel, 33583, 100756)

    print()
    print('Testing Part 2')
    test_eq('Ex2.1', calc_fuel_fuel, 2, 14)
    test_eq('Ex2.2', calc_fuel_fuel, 966, 1969)
    test_eq('Ex2.3', calc_fuel_fuel, 50346, 100756)

    print()

    data = get_input('input1')

    sf = part1(data)
    print(f'Part 1: {sf}')
    check_solution(1, 1, sf)

    sff = part2(data)
    print(f'Part 2: {sff}')
    check_solution(1, 2, sf)

