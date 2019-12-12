#!/usr/bin/env python3

from aoc import *

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
        self.states = set()
        self.states.add(str(self))

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

    def sign(self, m, n):
        if m < n : return 1
        if m == n : return 0
        return -1

    def solve(self, c, xs, vs, ac):
        a = (ac[c[0]] - ac[c[1]]) / 2
        b = vs[c[0]] - vs[c[1]] + a
        c = xs[c[0]] - xs[c[1]]
        det = math.sqrt(b*b - 4 * a * c)
        if det < 0:
            raise Exception('Det < 0!')
        return [(-b+det)/2/a, (-b-det)/2/a]


    def advance(self, i):
        xs = [m.p[i] for m in self.moons]
        vs = [m.v[i] for m in self.moons]
        ac = [sum([self.sign(m,n) for n in xs]) for m in xs]
        s = []
        for c in [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]:
            s.extend(self.solve(c, xs, vs, ac))
        t = min([t for t in s if t >= 0])

        xs = []

    def next(self):
        self.gravity()
        self.velocity()
        self.step += 1
        if str(self) in self.states:
            return self.step
        self.states.add(str(self))
        return 0

    def __str__(self):
        # l = [f'After {self.step} steps:\n', ]
        l = []
        for m in self.moons:
            l.append(str(m))
        return '\n'.join(l)


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
    s = System(data)
    r = 0
    while r == 0:
        r = s.next()
    return r

def part1(data):
    s = System(data)
    for i in range(1000):
        s.next()
        print(s)
    return s.energy()

def part2(data):
    s = System(data)
    r = 0
    while r == 0:
        r = s.next()
    return r

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
    # test_eq('Test 2.2', test2, 4686774924, test_input_2)
    print()

    data = get_input(f'input{DAY}')

    r = part1(data)
    if r is not None:
        print('Part 1:', r)
        check_solution(DAY, 1, r)

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        save_solution(DAY, 2, r)
