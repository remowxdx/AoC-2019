#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = 18

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [l.strip() for l in lines]

class Maze:
    def __init__(self, data):
        self.maze = {}
        self.pos = (0, 0)
        self.keys = {}
        self.steps = 0
        self.visited = {}
        self.parse(data)

    def get_pos(self, pos):
        if pos in self.maze:
            return self.maze[pos]
        return '#'

    def set_pos(self, pos, typ):
        self.maze[pos] = typ

    def offset(self, pos, direction):
        if direction == 0:
            return (pos[0], pos[1]-1)
        elif direction == 1:
            return (pos[0]-1, pos[1])
        elif direction == 2:
            return (pos[0], pos[1]+1)
        elif direction == 3:
            return (pos[0]+1, pos[1])
        else:
            raise Exception('Unknown direction.')


    def peek(self, direction):
        return self.get_pos(self.offset(self.pos, direction))

    def move(self, direction):
        pos = self.offset(self.pos, direction)
        if self.get_pos(pos) == '#':
            raise Exception('Gone into wall.')
        self.pos = pos

    def parse(self, data):

        if type(data) == str:
            data = data.strip().split('\n')

        self.limits = (len(data[0]), len(data))
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                if cell == '#':
                    continue
                if cell == '@':
                    self.pos = (x, y)
                    self.maze[(x,y)] = '.'
                else:
                    self.maze[(x,y)] = cell

    def find_keys(self, pos, steps, visited, doors):
        if pos in visited:
            return {}

        new_visited = visited.copy()
        new_visited[pos] = steps

        keys_found = {}

        cell = self.get_pos(pos)

        # do we have to open a door?
        if cell.isupper():
            doors_found = doors.copy()
            doors_found.append(cell)
        else:
            doors_found = doors

        # did we find a key?
        if cell.islower():
            keys_found[cell] = (steps, doors_found)

        for direction in range(4):
            new_pos = self.offset(pos, direction)
            m = self.get_pos(new_pos)

            # it is a wall?
            if m == '#':
                continue

            keys = self.find_keys(new_pos, steps + 1, new_visited, doors_found)

            for k in keys:
                keys_found[k] = keys[k]

        # print(pos, steps, keys_found)
        return keys_found

    def find_path(self, pos, steps, with_keys):
        possible_keys = self.find_keys(pos, steps, {}, with_keys)
        # print(f'find_path: pos: {pos}, steps: {steps}, wk: {with_keys}, pos_keys: {possible_keys}')
        if len(possible_keys) == 0:
            return None


        paths = {}

        for k in possible_keys:
            new_pos, next_steps = possible_keys[k]
            new_keys = with_keys.copy()
            new_keys.append(k)
            new_paths = self.find_path(new_pos, next_steps, new_keys)
            # print(f'NP: {new_paths}, key: {k}, steps: {steps+next_steps}, da pos: {pos}, steps: {steps}, wk: {with_keys}')
            paths[k] = (next_steps, new_paths)
        # print(f'           {paths}')
        return paths

    def find_all_keys(self):
        self.keys = {}
        for c in self.maze:
            if self.maze[c].islower():
                self.keys[self.maze[c]] = c

    def find_distances(self):
        dists = {}
        all_keys = list(self.keys.keys())
        for k in all_keys:
            # print('Finding', k)
            dists[k] = self.find_keys(self.keys[k], 0, {}, [])
            # print(dists[k])
        return dists

    def calc_dist(self):
        pass

    def __str__(self):
        r = []
        for y in range(self.limits[1]):
            s = ''
            for x in range(self.limits[0]):
                if self.pos == (x,y):
                    s += '@'
                else:
                    s += self.get_pos((x,y))
            r.append(s)
        return '\n'.join(r)

def min_path(paths):
    mps = []
    for k in paths:
        # print(paths[k])
        if paths[k][1] is None:
            mps.append(paths[k][0])
        else:
            mps.append(min_path(paths[k][1]))
    return min(mps)

def test1(data):
    m = Maze(data)
    p = m.find_path(m.pos, 0, [])
    r = min_path(p)
    return r

def test2(data):
    return 0

minimal = 10000

def find_key_path(d, with_keys, steps):
    global minimal
    if steps >= minimal:
        return None
    if len(d)-1 == len(with_keys):
        if steps < minimal:
            minimal = steps
            print(minimal)
        print(with_keys, steps)
        return with_keys, steps

    paths = []
    last_key = with_keys[-1]
    key_possibilities = d[last_key]

    good_keys = {}
    for key in key_possibilities:
        # if already taken do nothing
        if key in with_keys:
            continue

        doors = key_possibilities[key][1]

        # check if we have all needed keys
        for door in doors:
            if door.lower() not in with_keys:
                break
        else:
            good_keys[key] = steps + key_possibilities[key][0]

    
    for key in sorted(good_keys, key=lambda it: good_keys[it]):
        n_k = with_keys.copy()
        n_k.append(key)
        r = find_key_path(d, n_k, steps + key_possibilities[key][0])
        if r is not None:
            paths.append(r)

    if len(paths) == 0:
        return None

    mini = paths[0]
    for ks, steps in paths:
        if steps < mini[1]:
            mini = ks, steps
    return mini
            

def find_path(d):
    global minimal
    minimal = 10000
    paths = []
    for key in d['@']:
        print('Exploring: ', key, d['@'][key])
        if len(d['@'][key][1]) == 0:
            paths.append(find_key_path(d, [key, ], d['@'][key][0]))
    mini = paths[0]
    print(paths)
    for kss in paths:
        if kss is None:
            continue
        ks, steps = kss
        if steps < mini[1]:
            mini = ks, steps
    return mini

def part1(data):
    m = Maze(data)
    m.find_all_keys()
    print(m)
    d = m.find_distances()
    d['@'] = m.find_keys(m.pos, 0, {}, [])
    print(d)
    r = find_path(d)
    print(r)
    #print('Dists:', m.find_distances())
    # p = m.find_path(m.pos, 0, [])
    # r = min_path(p)
    return r[1]

def part2(data):
    return None

if __name__ == '__main__':

    test_input_1 = '''#########
#b.A.@.a#
#########'''
    test_input_2 = '''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################'''
    test_input_3 = '''########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################'''
    test_input_4 = '''#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################'''
    test_input_5 = '''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################'''
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 8, test_input_1)
    test_eq('Test 1.2', part1, 86, test_input_2)
    test_eq('Test 1.3', part1, 132, test_input_3)
    # test_eq('Test 1.4', part1, 136, test_input_4)
    # test_eq('Test 1.5', part1, 81, test_input_5)
    print()

    test_input_2 = [4,5,6]
    print('Test Part 2:')
    test_eq('Test 2.1', test2, 42, test_input_1)
    print()

    data = get_input(f'input{DAY}')

    r = part1(data)
    # r = None
    if r is not None:
        print('Part 1:', r)
        save_solution(DAY, 1, r)

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        save_solution(DAY, 2, r)
