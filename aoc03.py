#!/usr/bin/env python3

from aoc import *

pd = Debug(True)

def get_input(file_name):
    lines = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
    wire1 = lines[0].split(',')
    wire2 = lines[1].split(',')
    return (wire1, wire2)

def move(pos, direction):
    if direction == 'R':
        return (pos[0]+1, pos[1])

    if direction == 'L':
        return (pos[0]-1, pos[1])

    if direction == 'U':
        return (pos[0], pos[1]+1)

    if direction == 'D':
        return (pos[0], pos[1]-1)

    raise Exception('Direction unknown.')

def wire_path(data):
    pos = (0, 0)
    path = set()
    for d in data:
        direction = d[0]
        length = int(d[1:])
        for n in range(length):
            pos = move(pos, direction)
            path.add(pos)
    return path

def wire_path_with_steps(data):
    pos = (0, 0)
    path = {}
    steps = 0
    for d in data:
        direction = d[0]
        length = int(d[1:])
        for n in range(length):
            steps += 1
            pos = move(pos, direction)
            path[pos] = steps
    return path

def find_nearest_crossing(data):
    p1 = wire_path(data[0])
    print('-' * 40)
    pos = (0, 0)
    best_crossing = None
    for d in data[1]:
        # pd('*' * 3, d)
        direction = d[0]
        length = int(d[1:])
        for n in range(length):
            pos = move(pos, direction)
            if pos in p1:
                dist = abs(pos[0]) + abs(pos[1])
                if best_crossing is None or dist < best_crossing:
                    print('**********', dist, pos)
                    best_crossing = dist
    return best_crossing

def find_shortest_crossing(data):
    p1 = wire_path_with_steps(data[0])
    print('-' * 40)
    pos = (0, 0)
    best_crossing = None
    steps = 0
    for d in data[1]:
        # pd('*' * 3, d)
        direction = d[0]
        length = int(d[1:])
        for n in range(length):
            steps += 1
            pos = move(pos, direction)
            if pos in p1:
                dist = steps + p1[pos]
                if best_crossing is None or dist < best_crossing:
                    print('**********', dist, pos)
                    best_crossing = dist
    return best_crossing

def part1(data):
    return find_nearest_crossing(data)

def part2(data):
    return find_shortest_crossing(data)

def test1(data):
    return find_nearest_crossing(data)

def test2(data):
    return find_shortest_crossing(data)

if __name__ == '__main__':
    ex1 = (['R75','D30','R83','U83','L12','D49','R71','U7','L72'], ['U62','R66','U55','R34','D71','R55','D58','R83'])
    ex2 = (['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'], ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7'])
    test_eq('Ex1.1', test1, 159, ex1)
    test_eq('Ex1.2', test1, 135, ex2)
    print()
    test_eq('Ex2.1', test2, 610, ex1)
    test_eq('Ex2.2', test2, 410, ex2)
    print()

    #p = wire1_path((['L3', 'D4'],['R4','U3']))
    #print(p)

    data = get_input('input3')
    print(data)

    r = part1(data)

    print(f'Part 1: {r}')

    r = part2(data)
    print(f'Part 2: {r}')
