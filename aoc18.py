#!/usr/bin/env python3

from aoc import *
import heapq

pd = Debug(True)
DAY = 18

def get_input(filename):
    with open(filename, 'r') as f:
        return f.read()

class Node:
    def __init__(self, name, node_type):
        self.links = {}
        self.type = node_type
        self.name = name

    def __add__(self, other):
        return self.add_link(other, 1)

    def add_link(self, other, dist):
        self.links[other] = dist
        other.links[self] = dist

    def remove_link(self, other):
        if other in self.links:
            self.links.pop(other)
        # else:
            # print(self.name, other.name)
        if self in other.links:
            other.links.pop(self)
        # else:
            # print(other.name, self.name)

    def __sub__(self, other):
        self.remove_link(other)

    def __contains__(self, other):
        return other in self.links

    def __lt__(self, other):
        return self.name < other.name

    def shortcut(self):
        if len(self.links) == 1:
            for l in self.links:
                pass
            l.remove_link(self)
            return

        to_remove = []
        to_add = []
        for n in self.links:
            for m in self.links:
                if n == m:
                    continue
                to_add.append((m, n, self.links[n] + self.links[m]))
            to_remove.append(n)

        for r in to_remove:
            self.remove_link(r)

        for m, n, d in to_add:
            if n not in m.links:
                m.add_link(n, d)
                # print(m.name, n.name, d)

    def __str__(self):
        s0 = f'{self.name:8} - {self.type} -> '
        s = []
        for link in self.links:
            s.append(f'{link.name:8} - {self.links[link]}')
        return s0 + ', '.join(s)

class Maze:
    def __init__(self, data):
        self.nodes = {}
        self.cut_nodes = {}
        self.num_keys = 0
        self.width = 0
        self.height = 0
        self.starts = []
        self.build_graph(data)

    def build_graph(self, data):
        # Create nodes
        x = 0
        y = 0
        nodes = {}
        for c in data:
            if c == '#':
                x += 1
                continue
            elif c == '\n':
                y += 1
                x = 0
            elif c == '.' or c.islower() or c.isupper() or c == '@':
                nodes[(x,y)] = Node(str((x,y)), c)
                if c == '@':
                    self.starts.append(nodes[(x,y)])
                if c.islower():
                    self.num_keys += 1
                x += 1
            else:
                raise 'Unknown node.'

        self.width = x - 1
        self.height = y

        # Link nodes
        for x, y in nodes:
            if (x - 1, y) in nodes:
                nodes[(x, y)] + nodes[(x - 1, y)]
            if (x, y - 1) in nodes:
                nodes[(x, y)] + nodes[(x, y - 1)]

        # Optimize graph
        for n in nodes:
            if nodes[n].type == '.':
                nodes[n].shortcut()

        for n in nodes:
            if len(nodes[n].links) > 0:
                self.nodes[n] = nodes[n]
                # print(nodes[n])
            else:
                self.cut_nodes[n] = nodes[n]

        # print(self)

    def bfs(self):
        visited = [set() for _ in self.starts]
        to_visit = [(0, 26, tuple(self.starts), ())]
        mkl = 0
        while len(to_visit) > 0:
            l, lk, nodes, keys = heapq.heappop(to_visit)
            
            if len(keys) == self.num_keys:
                return l
            if len(keys) > mkl:
                print(len(keys), len(to_visit))
                mkl = len(keys)
            # print(len(to_visit), [len(n) for n in visited])

            # print([node.name for node in nodes], l, keys)

            for i, n in enumerate(nodes):
                if (n, keys) in visited[i]:
                    continue
                visited[i].add((n, keys))
                for new_node in n.links:
                    key = new_node.type
                    d = n.links[new_node]
                    if (new_node, keys) in visited:
                        continue
                    if key.isupper() and key.lower() not in keys:
                        continue
                    elif key.islower() and key not in keys:
                        kl = list(keys)
                        kl.append(key)
                        kl.sort()
                        new_keys = tuple(kl)
                    else:
                        new_keys = keys

                    new_nodes = []
                    for j, nn in enumerate(nodes):
                        if i == j:
                            new_nodes.append(new_node)
                        else:
                            new_nodes.append(nn)
                    heapq.heappush(to_visit, (l + d, self.num_keys - len(new_keys), tuple(new_nodes), new_keys))


    def __str__(self):
        maze = []
        for y in range(self.height+1):
            row = []
            for x in range(self.width+1):
                if (x,y) in self.nodes:
                    row.append(self.nodes[(x,y)].type)
                elif (x,y) in self.cut_nodes:
                    # row.append(self.cut_nodes[(x,y)].type)
                    row.append(' ')
                else:
                    row.append('#')
            maze.append(''.join(row))
        return '\n'.join(maze)
def test1(data):
    return 0

def test2(data):
    return 0

def part1(data):
    m = Maze(data)

    r = m.bfs()
    return r

def part2(data):
    m = Maze(data)
#    for p in m.nodes:
#        if m.nodes[p].type.isupper():
#            m.nodes[p].shortcut()

    r = m.bfs()
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
    test_input_6 = '''#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############'''
    if True:
        print('Test Part 1:')
        test_eq('Test 1.1', part1, 8, test_input_1)
        test_eq('Test 1.2', part1, 86, test_input_2)
        test_eq('Test 1.3', part1, 132, test_input_3)
        test_eq('Test 1.4', part1, 136, test_input_4)
        test_eq('Test 1.5', part1, 81, test_input_5)
        print()

        test_input_2 = [4,5,6]
        print('Test Part 2:')
        test_eq('Test 2.1', part2, 396, test_input_3)
        test_eq('Test 2.2', part2, 72, test_input_6)
        print()

    data = get_input(f'input{DAY}')

    r = part1(data)
    if r is not None:
        print('Part 1:', r)
        check_solution(DAY, 1, r)

    data = get_input(f'input{DAY}-2')

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        check_solution(DAY, 2, r)
