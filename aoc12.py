#!/usr/bin/env python3

from aoc import *

import math

pd = Debug(False)
DAY = 12

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

class Moon:
    def __init__(self, position):
        self.parse_position(position)
        self.v = [0,0,0]  # Initial velocity

    def parse_position(self, position):
        s = position.strip('<>\n')
        coords = [c.strip() for c in s.split(',')]
        self.p = [int(c.split('=')[1]) for c in coords]

    def gravity(self, other):
        for i in range(3):
            if self.p[i] > other.p[i]:
                self.v[i] -= 1
            elif self.p[i] < other.p[i]:
                self.v[i] += 1

    def velocity(self):
        for i in range(3):
            self.p[i] += self.v[i]

    def energy(self):
        pot = 0
        kin = 0
        for i in range(3):
            pot += abs(self.p[i])
            kin += abs(self.v[i])
        return pot * kin

    def __str__(self):
        return f'pos=<x= {self.p[0]}, y= {self.p[1]}, z= {self.p[2]}>, vel=<x= {self.v[0]}, y= {self.v[1]}, z= {self.v[2]}>'


class System:
    def __init__(self, positions):
        self.moons = []
        for pos in positions:
            self.moons.append(Moon(pos))
        self.step = 0

    def gravity(self):
        for m in self.moons:
            for n in self.moons:
                if m == n:
                    continue
                m.gravity(n)

    def velocity(self):
        for m in self.moons:
            m.velocity()

    def energy(self):
        e = 0
        for m in self.moons:
            e += m.energy()
        return e

    def next(self):
        self.gravity()
        self.velocity()
        self.step += 1
        return 0

    def __str__(self):
        l = [f'After {self.step} steps:\n', ]
        l = []
        for m in self.moons:
            l.append(str(m))
        return '\n'.join(l)

class System2:
    def __init__(self, positions):
        self.status = [[0 for _ in range(len(positions) * 2)] for _ in range(3)]
        self.step = [ 0 for c in range(3)]
        for i in range(len(positions)):
            self.parse_position(i, positions[i])
        self.history = [ [self.status[c].copy(), ] for c in range(3)]
        self.intro = [ 0 for c in range(3)]
        self.period = [ 0 for c in range(3)]

    def parse_position(self, i, position):
        s = position.strip('<>\n')
        coords = [c.strip() for c in s.split(',')]
        p = [int(c.split('=')[1]) for c in coords]
        for c in range(3):
            self.status[c][i] = p[c]

    def next(self, c):
        self.step[c] += 1
        status = self.status[c]
        n = len(status) // 2
        for i in range(n):
            for j in range(i + 1, n):
                if status[i] < status[j]:
                    status[i+n] += 1
                    status[j+n] -= 1
                elif status[i] > status[j]:
                    status[i+n] -= 1
                    status[j+n] += 1

        for i in range(n):
            status[i] += status[i+n]

        if status in self.history[c]:
            print('F:', c, self.step[c], status)
            intro = self.history[c].index(status)
            self.intro[c] = intro
            self.period[c] = self.step[c] - intro
            return False
        self.history[c].append(status.copy())
        if self.step[c] % 1000 == 0:
            print('E:', c, self.step[c], status)
        return True

    def find_period(self, c):
        r = True
        while r:
            r = self.next(c)

    def find_periods(self):
        for c in [2,1]:
            self.find_period(c)

    def find_repeat(self):
        i = max(self.intro)
        def lcm(a, b):
            g = math.gcd(a, b)
            return a // g * b
        return i + lcm(lcm(self.period[0], self.period[1]), self.period[2])

def test1(data, steps):
    s = System(data)
    pd(s)
    for i in range(steps):
        s.next()
        if steps <=0 or (i+1) % 10 == 0:
            pd(s)
    pd(s.energy())
    return s.energy()

def test2(data):
    s = System2(data)
    s.find_periods()
    return s.find_repeat()

def part1(data):
    s = System(data)
    for i in range(1000):
        s.next()
        pd(s)
    return s.energy()

def part2(data):
    s = System2(data)
    s.find_periods()
    print(s.intro)
    print(s.period)
    return s.find_repeat()

if __name__ == '__main__':

    test_input_1 = '''<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>'''.split('\n')
    test_input_2 = '''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''.split('\n')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 179, test_input_1, 10)
    test_eq('Test 1.2', test1, 1940, test_input_2, 100)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', test2, 2772, test_input_1)
    test_eq('Test 2.2', test2, 4686774924, test_input_2)
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

# F: 2 193052 [4, -8, 9, -2, 0, 0, 0, 0]
# F: 1 96236 [1, -10, 4, 6, 0, 0, 0, 0]
# F: 0 286332 [-15, 1, -5, 4, 0, 0, 0, 0]
