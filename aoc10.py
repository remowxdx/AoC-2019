#!/usr/bin/env python3

from aoc import *

import math

pd = Debug(False)
DAY = 10

def get_input(filename):
    with open(filename, 'r') as f:
        string = f.read()
    return get_asteroids(string)

def get_asteroids(string):
    lines = string.split('\n')
    asteroids = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] != '.':
                asteroids.append((x,y))
    return len(lines), len(lines[0]), asteroids

def get_asteroids_directions(pos, asteroids):
    view_directions = {}
    for asteroid in asteroids:
        vd = view_direction(pos, asteroid)
        if vd not in view_directions:
            view_directions[vd] = []
        view_directions[vd].append(asteroid)

    for direction in view_directions:
        view_directions[direction].sort(key=lambda a: distance_sq(pos, a))
    return view_directions

def direction_angle(direction):
    angle = math.atan2(direction[0], -direction[1])
    if angle < 0.0:
        angle += 2 * math.pi
    return angle

def distance_sq(pos, asteroid):
    dx = asteroid[0] - pos[0]
    dy = asteroid[1] - pos[1]
    return dx * dx + dy * dy

def get_visible_asteroids(pos, asteroids):
    view_directions = set()
    for asteroid in asteroids:
        view_directions.add(view_direction(pos, asteroid))
    return len(view_directions) - 1

def view_direction(fro, to):
    dx = to[0] - fro[0]
    dy = to[1] - fro[1]
    if dx == 0 and dy == 0:
        return (0, 0)
    if dx == 0:
        return (0, dy // abs(dy))
    if dy == 0:
        return (dx // abs(dx), 0)
    gcd = math.gcd(dx, dy)
    return (dx // gcd, dy // gcd)

def run_cannon(pos, asteroids):
    vaporized = []
    dirs = get_asteroids_directions(pos, asteroids)
    turn = 0
    sdirs = sorted(dirs.keys(), key=lambda k: direction_angle(k))
    while len(vaporized) < len(asteroids) - 1:
        for d in sdirs:
            if d == (0,0):
                continue
            if turn < len(dirs[d]):
                vaporized.append(dirs[d][turn])
        pd("*" * 10, turn)
        pd(vaporized)
        turn += 1
    return vaporized

def test1(data):
    width, length, asteroids = data
    max_vis = 0
    for asteroid in asteroids:
        r = get_visible_asteroids(asteroid, asteroids)
        if r > max_vis:
            max_vis = r
            pd(asteroid)
    return max_vis

def test2(data):
    width, length, asteroids = data
    r = run_cannon((11, 13), asteroids)
    pd(r)
    return r[200 - 1]

def part1(data):
    width, length, asteroids = data
    max_vis = 0
    for asteroid in asteroids:
        r = get_visible_asteroids(asteroid, asteroids)
        if r > max_vis:
            max_vis = r
    return max_vis

def part2(data):
    width, length, asteroids = data
    max_vis = (0, (0,0))
    for asteroid in asteroids:
        r = get_visible_asteroids(asteroid, asteroids)
        if r > max_vis[0]:
            max_vis = (r, asteroid)
    r = run_cannon(max_vis[1], asteroids)
    return 100 * r[200 - 1][0] + r[200 - 1][1]

if __name__ == '__main__':

    test_input_1 = get_asteroids('''.#..#
.....
#####
....#
...##''')
    test_input_2 = get_asteroids('''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####''')
    test_input_3 = get_asteroids('''#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.''')
    test_input_4 = get_asteroids('''.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..''')
    test_input_5 = get_asteroids('''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##''')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 8, test_input_1)
    test_eq('Test 1.2', test1, 33, test_input_2)
    test_eq('Test 1.3', test1, 35, test_input_3)
    test_eq('Test 1.4', test1, 41, test_input_4)
    test_eq('Test 1.5', test1, 210, test_input_5)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', test2, (8,2), test_input_5)
    print()

    data = get_input(f'input{DAY}')

    r = part1(data)
    if r is not None:
        print('Part 1:', r)
        check_solution(DAY, 1, r)

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        check_solution(DAY, 2, r)
