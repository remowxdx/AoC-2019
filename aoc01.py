#!/usr/bin/env python3

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
        print(f)
        f = calc_fuel(f)
    return sf

if __name__ == '__main__':
    data = get_input('input1')
    fuel = [calc_fuel_fuel(mass) for mass in data]
    sf = sum(fuel)
    print(sf)
