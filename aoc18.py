#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = 18

def get_input(filename):
    with open(filename, 'r') as f:
        return f.read()

class Node:
    def __init__(self, name, node_type):
        self.name = name
        self.type = node_type
        self.links = []

    def link_to(self, other, length=1):
        if other not in self:
            self.links.append((other, length))
        if self not in other:
            other.links.append((self, length))

    def remove_link(self, other):
        for i in range(len(self.links)):
            node, dist = self.links[i]
            if node == other:
                self.links.pop(i)
                break

    def optimize(self):
        t = self.type
        if t.isupper() or t.islower() or t == '@':
            return False

        if len(self.links) == 1:
            n1, d1 = self.links[0]
            n1.remove_link(self)
            self.links = []
            return True

        if len(self.links) == 2:
            n1, d1 = self.links[0]
            n2, d2 = self.links[1]

            n1.remove_link(self)
            n2.remove_link(self)
            self.links = []

            n1.link_to(n2, d1 + d2)
            return True
        return False
            
        

    def __add__(self, other):
        if other in self:
            for node, dist in self.links:
                if node == other:
                    return dist
            return None
    
    def __contains__(self, other):
        for node, dist in self.links:
                if node == other:
                    return True
        return False

    def __str__(self):
        l = ','.join([f'{n.name}-{d}' for n, d in self.links])
        return f'{self.name} -> {l}'

class Maze:
    def __init__(self, data):
        self.portals = {}
        self.nodes = {}
        self.maze = data
        self.starts = []
        self.num_keys = 0
        self.width = data.index('\n') + 1
        self.height = len(data) // self.width
        self.build_graph()

    def get(self, x, y):
        if x < 0 or x >= self.width:
            raise Exception(f'Out of x {(x, y)}')
        if y < 0 or y >= self.height:
            raise Exception(f'Out of y {(x, y)}')
        return self.maze[y * self.width + x]

    def get_pos(self, x, y):
        if (x,y) not in self.nodes:
            return '#'
        return self.nodes[(x,y)].type

    def build_graph(self):
        # Create nodes
        for y in range(self.height):
            for x in range(self.width):
                t = self.get(x, y)
                if t == '.' or t.isupper() or t.islower() or t == '@':
                    self.nodes[(x,y)] = Node(f'({x}, {y})', t)
                    if t.islower():
                        self.num_keys += 1
                    # pd('+', (x,y))
                    if t == '@':
                        self.starts.append(self.nodes[(x,y)])
        # pd(self)

        # Link nodes
        for y in range(self.height):
            for x in range(self.width):
                # pd('Node:', (x,y))
                t  = self.get_pos(x, y)
                tl = self.get_pos(x-1, y)
                tr = self.get_pos(x+1, y)
                tu = self.get_pos(x, y-1)
                td = self.get_pos(x, y+1)

                if t == '.' or t.isupper() or t.islower() or t == '@':
                    if tr == '.' or tr.isupper() or tr.islower() or tr == '@':
                        self.nodes[(x,y)].link_to(self.nodes[(x+1, y)], 1)
                    if td == '.' or td.isupper() or td.islower() or td == '@':
                        self.nodes[(x,y)].link_to(self.nodes[(x, y+1)], 1)
                    continue

    def optimize(self):
        done = False
        while not done:
            done = True
            for pos in self.nodes:
                if pos in self.starts:
                    continue
                r = self.nodes[pos].optimize()
                if r:
                    done = False

        to_remove = []
        for x, y in self.nodes:
            if len(self.nodes[(x,y)].links) == 0:
                to_remove.append((x,y))
        for p in to_remove:
            self.nodes.pop(p)

    def __str__(self):
        l = [f'W: {self.width}, L: {self.height}, NK: {self.num_keys}', ]
        for p in self.nodes:
            l.append(str(self.nodes[p]))
        return '\n'.join(l)

    def sp(self):
        to_visit = [(self.starts[0], 0, set()), ]
        visited = []
        while len(to_visit) > 0:
            m = to_visit[0]
            for mc in to_visit:
                if mc[1] < m[1]:
                    m = mc

            node, dist, keys = m
            to_visit.remove(m)
            pd(node.name, dist, keys)
            visited.append((node, keys))
            if len(keys) == self.num_keys:
                return dist

            for next_node, next_dist in node.links:
                t = next_node.type
                if t.isupper() and t.lower() not in keys:
                    continue
                next_keys = keys.copy()
                if t.islower() and t not in keys:
                    next_keys.add(t)
                visit = True
                for old_node, old_keys in visited:
                    if next_node == old_node and next_keys == old_keys:
                        visit = False
                        break
                for old_node, old_dist, old_keys in to_visit:
                    if next_node == old_node and next_keys == old_keys:
                        visit = False
                        break
                if visit:
                    to_visit.append((next_node, dist + next_dist, next_keys))

    def sp4(self):
        to_visit = []
        robots = []

        for start in self.starts:
            robots.append(start)

        to_visit.append((robots, 0, set()))
        visited = []
        while len(to_visit) > 0:
            m = to_visit[0]
            for mc in to_visit:
                if mc[1] < m[1]:
                    m = mc

            nodes, dist, keys = m
            to_visit.remove(m)
            pd(','.join([n.name for n in nodes]), dist, keys)
            if dist > 100 and dist / len(keys) > 100:
                continue
            visited.append((nodes, keys))
            if len(keys) == self.num_keys:
                return dist

            for r, node in enumerate(nodes):
                for next_node, next_dist in node.links:
                    t = next_node.type
                    if t.isupper() and t.lower() not in keys:
                        continue
                    next_keys = keys.copy()
                    next_nodes = nodes.copy()
                    next_nodes[r] = next_node
                    if t.islower() and t not in keys:
                        next_keys.add(t)
                    visit = True
                    for old_nodes, old_keys in visited:
                        if next_nodes == old_nodes and next_keys == old_keys:
                            visit = False
                            break
                    for old_nodes, old_dist, old_keys in to_visit:
                        if next_nodes == old_nodes and next_keys == old_keys:
                            visit = False
                            break
                    if visit:
                        to_visit.append((next_nodes, dist + next_dist, next_keys))
        return "Ahhh!"


def test1(data):
    return 0

def test2(data):
    return 0

def part1(data):
    m = Maze(data)
    m.optimize()
    pd(m)
    return m.sp()

def part2(data):
    nd = data.split('\n')
    nd[39] = nd[39][:39] + '@#@' + nd[39][42:]
    nd[40] = nd[40][:39] + '###' + nd[40][42:]
    nd[41] = nd[41][:39] + '@#@' + nd[41][42:]

    print('\n'.join(nd))
    m = Maze('\n'.join(nd))
    m.optimize()
    pd(m)
    print([n.name for n in m.starts])
    r = m.sp4()
    print(r)
    return r

if __name__ == '__main__':

    test_input_1 = '''#########
#b.A.@.a#
#########'''
    test_input_2 = '''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
'''
    test_input_3 = '''########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
'''
    test_input_4 = '''#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
'''
    test_input_5 = '''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
'''
    if False:
        print('Test Part 1:')
        test_eq('Test 1.1', part1, 8, test_input_1)
        test_eq('Test 1.2', part1, 86, test_input_2)
        test_eq('Test 1.3', part1, 132, test_input_3)
        test_eq('Test 1.4', part1, 136, test_input_4)
        test_eq('Test 1.6', part1, 81, test_input_5)
        print()

        test_input_2 = [4,5,6]
        print('Test Part 2:')
        test_eq('Test 2.1', part2, 396, test_input_3)
        print()

    data = get_input(f'input{DAY}')

    # r = part1(data)
    r = None
    if r is not None:
        print('Part 1:', r)
        check_solution(DAY, 1, r)

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        save_solution(DAY, 2, r)
