#!/usr/bin/env python3

from aoc import *

pd = Debug(False)

def get_input(file_name):
    data = []
    with open(file_name, 'r') as f:
        data = f.readlines()
    return [int(d) for d in data[0].strip()]

def layerize(data, width, length):
    layers = []
    n = width * length
    i = 0
    while i < len(data):
        layers.append(data[i:i+n])
        i += n
    return layers

def extract(layer):
    count = [0 for i in range(10)]
    for i in layer:
        count[i] += 1
    return count

def part1(data):
    layers = layerize(data, 25, 6)
    pd(len(layers))
    match = (25*6,0,0)
    for layer in layers:
        r = extract(layer)
        if r[0] < match[0]:
            match = (r[0], r[1], r[2])

    return match[1] * match[2]

def part2(data):
    final = [2 for i in range(25*6)]
    layers = layerize(data, 25, 6)
    pd(len(layers))
    match = (25*6,0,0)
    for layer in layers:
        for c in range(len(layer)):
            if final[c] == 2:
                final[c] = layer[c]
    return final

def draw(img):
    p = 0
    print()
    for i in img:
        if p % 25 == 0:
            print('\n ', end='')
        if i == 0:
            print(' ', end='')
        elif i == 1:
            print('\u2588', end='')
        else:
            raise Exception('Pixel not black nor white')
        p += 1
    print()

if __name__ == '__main__':

    print('Testing Part 1')
    # test_eq('Ex1.1', calc_fuel, 2, 12)

    print()
    print('Testing Part 2')
    # test_eq('Ex2.1', calc_fuel_fuel, 2, 14)
    # test_eq('Ex2.2', calc_fuel_fuel, 966, 1969)
    # test_eq('Ex2.3', calc_fuel_fuel, 50346, 100756)

    print()

    data = get_input('input8')

    r = part1(data)
    print(f'Part 1: {r}')

    img = part2(data)
    print(f'Part 2: {img}')
    draw(img)

