#!/usr/bin/env python3

import random

#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############

# a < b < c < d < f < g
# e < d < f
# e < h
# b < c < i < j < l
# l < k < n < m < o
# n < m
# g < k < j
# h < i
# 
# a:
# b: a
# c: b a
# d: e c b a
# e:
# f: e d c b a
# g: f d c b a
# h: e
# i: h c b
# j: i h c b
# k: l g
# l: j i c b
# m: n k l
# n: k l
# o: m n k l
# 
# after: 'a': []
#         'b': ['a']
#         'c': ['b', 'a']
#         'd': ['e', 'c', 'b', 'a']
#         'e': []
# 
# paths: []

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
        self.paths = []
        self.starts = []
        self.after = {}
        self.dists = {}
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
                if c.islower():
                    self.after[c] = []
                nodes[(x,y)] = Node(str((x,y)), c)
                if c == '@':
                    self.starts.append(nodes[(x,y)])
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

        # for node in self.nodes:
            # print(nodes[node].name, '->', ', '.join([f'{l.name}-{nodes[node].links[l]}' for l in nodes[node].links]))

        # print(self)

    def explore(self, node, keys):
        if node in self.order_visited:
            return
        self.order_visited.append(node)
        if node.type.islower():
            nk = node.type.lower()
            for k in keys:
                if nk not in self.after[k]:
                    self.after[nk].append(k)
            new_keys = keys.copy()
            if node.type.islower():
                new_keys.append(nk)
        elif node.type.isupper():
            nk = node.type.lower()
            new_keys = keys.copy()
            new_keys.append(nk)
        else:
            new_keys = keys
        for l in node.links:
            self.explore(l, new_keys)

    def order(self):
        self.order_visited = []
        for n in self.starts:
            self.explore(n, [])

        # for k in self.after:
            # print(k + ': ', self.after[k])
        del(self.order_visited)

    def build_paths(self):
        to_insert = list(self.after.keys())

        for k in self.after:
            if len(self.after[k]) == 0:
                self.paths.append([k])
                to_insert.remove(k)
                break
        # print(to_insert)
        # print(self.paths)

        i = 0
        while len(to_insert) > 0:
            for k in to_insert:
                r = self.insert(k)
                if r:
                    to_insert.remove(k)
                # print(f'Path for {k}:', self.paths)
                i += 1
                if i % 10 == 0 or i > 120:
                    print(i, len(self.paths), to_insert)
        # print(to_insert)
        # print(self.paths, len(self.paths))

    def insert(self, k):
        if k in self.paths[0]:
            return False

        for path in self.paths:
            for n in self.after[k]:
                if n not in path:
                    # print(f'Key {k} is missing {n}.')
                    return False

        new_paths = []
        for path in self.paths:
            for i in range(len(path) - 1, -1, -1):
                if path[i] not in self.after[k]:
                    np = path.copy()
                    np.insert(i, k)
                    new_paths.append(np)
                else:
                    break
            path.append(k)
        self.paths.extend(new_paths)
        return True

    def dist(self, starts, b):
        tstarts = tuple(starts)
        if (tstarts,b) in self.dists:
            return self.dists[(tstarts,b)]

        to_visit = []
        visited = []
        to_visit.append((starts, 0))

        while len(to_visit) > 0:
            #print(len(to_visit))
            nodes, dist = to_visit[0]
            for nns, dd in to_visit[1:]:
                if dd < dist:
                    nodes = nns
                    dist = dd

            to_visit.remove((nodes, dist))

            if nodes in visited:
                continue

            visited.append(nodes)
            # print('\n'.join([', '.join([ns.name for ns in vs]) for vs in visited]) + '\n')

            for node in nodes:
                # print(f'Found {node.type} {node.name}.')
                if node.type == b:
                    self.dists[(tstarts,b)] = (nodes, dist)
                    return nodes, dist

            for node in nodes:
                for l in node.links:
                    nns = []
                    for nn in nodes:
                        if nn == node:
                            nns.append(l)
                        else:
                            nns.append(nn)
                    if nns not in visited:
                        for i, (ons, od) in enumerate(to_visit):
                            if nns == ons:
                                if dist + node.links[l] < od:
                                    to_visit[i] = (nns, dist + node.links[l])
                                    break
                        else:
                            to_visit.append((nns, dist + node.links[l]))
        s = ', '.join([node.name for node in starts])
        raise Exception(f'No path from {s} to {b}')

    def calc_length(self, path):
        robots = self.starts.copy()
        pk = '@'
        l = 0
        for k in path:
            # print(f'{pk} -> {k} = ', end='')
            robots, d = self.dist(robots, k)
            # print(d)
            l += d
            if l >= 1728:
                return l
            pk = k
        return l

    def min_length(self):
        ml = self.calc_length(self.paths[0])
        i = 0
        n = len(self.paths)
        for p in self.paths[1:]:
            l = self.calc_length(p)
            print(l, p, i, n, ml)
            i += 1
            if l < ml:
                ml = l
        return ml

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

    def rand_path(self):
        to_insert = list(self.after.keys())

        path = []

        while len(to_insert) > 0:
            candidates = []
            for c in to_insert:
                for k in self.after[c]:
                    if k not in path:
                        break
                else:
                    candidates.append(c)

            r = random.randint(0,len(candidates)-1)
            path.append(candidates[r])
            to_insert.remove(candidates[r])
        return path


if __name__ == '__main__':
    input_1 = '''#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############'''

    with open('input18-2', 'r') as f:
        input_2 = f.read().strip()
    print(input_2)
    m = Maze(input_2)
    m.order()
    for p in m.nodes:
        if m.nodes[p].type.isupper():
            m.nodes[p].shortcut()
    p = m.rand_path()
    print(p)
    ml = m.calc_length(p)
    print(ml)
    while ml >= 1728:
        p = m.rand_path()
        print(p)
        l = m.calc_length(p)
        print(l)
        if l < ml:
            ml = l
    # m.build_paths()
    # r = m.min_length()
    print(ml)
