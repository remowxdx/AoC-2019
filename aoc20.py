#!/usr/bin/env python3

from aoc import *

pd = Debug(False)
DAY = 20

def get_input(filename):
    with open(filename, 'r') as f:
        return f.read()

class Node:
    def __init__(self, name):
        self.name = name
        self.links = []
        self.visited = False
        self.rec = 0
        self.prev = {}

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
        if self.rec != 0:
            return False

        if len(self.links) == 1:
            n1, d1 = self.links[0]
            n1.remove_link(self)
            self.links = []
            return True

        if len(self.links) != 2:
            return False

        n1, d1 = self.links[0]
        n2, d2 = self.links[1]

        n1.remove_link(self)
        n2.remove_link(self)
        self.links = []

        n1.link_to(n2, d1 + d2)

        return True
            
        

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
        return f'{self.name}{self.rec} -> {l}'

class Maze:
    def __init__(self, data):
        self.portals = {}
        self.nodes = {}
        self.maze = data
        self.width = data.index('\n') + 1
        self.height = len(data) // self.width
        self.build_graph()

    def get(self, x, y):
        if x < 0 or x >= self.width:
            return ' '
        if y < 0 or y >= self.height:
            return ' '
        return self.maze[y * self.width + x]

    def build_graph(self):
        # Create nodes
        for y in range(self.height):
            for x in range(self.width):
                t = self.get(x, y)
                if t == '.':
                    self.nodes[(x,y)] = Node(f'({x}, {y})')

        # Find portals and link nodes
        for y in range(self.height):
            for x in range(self.width):
                t = self.get(x, y)
                tl = self.get(x-1, y)
                tr = self.get(x+1, y)
                tu = self.get(x, y-1)
                td = self.get(x, y+1)

                if t == '.':
                    if tr == '.':
                        self.nodes[(x,y)].link_to(self.nodes[(x+1, y)], 1)
                    if td == '.':
                        self.nodes[(x,y)].link_to(self.nodes[(x, y+1)], 1)
                    continue

                if t.isupper():
                    if  tl == '.':
                        pp = (x-1,y)
                        t2 = tr
                    elif tr.isupper():
                        pp = (x+2, y)
                        t2 = tr
                    elif tu == '.':
                        pp = (x,y-1)
                        t2 = td
                    elif td.isupper():
                        pp = (x, y+2)
                        t2 = td
                    else:
                        continue

                    label = min(t, t2) + max(t,t2)

                    self.nodes[pp].name += label
                    if pp[0] == 2 or pp[1] == 2 or pp[0] == self.width - 4 or pp[1] == self.height - 3:
                        self.nodes[pp].rec = -1
                    else:
                        self.nodes[pp].rec = 1
                    # print(self.nodes[pp])

                    if label in self.portals:
                        self.nodes[pp].link_to(self.nodes[self.portals[label]], 1)
                    else:
                        self.portals[label] = pp
                    if label == 'AA':
                        self.start = self.nodes[pp]
                    if label == 'ZZ':
                        self.end = self.nodes[pp]

    def optimize(self):
        done = False
        while not done:
            done = True
            for pos in self.nodes:
                r = self.nodes[pos].optimize()
                if r:
                    done = False

    def sp(self, node):
        node.visited = True
        if node == self.end:
            return 0

        st = []
        for n, d in node.links:
            if n.visited:
                continue
            s = self.sp(n)
            if s is not None:
                st.append(s + d)
        if len(st) == 0:
            return None
        return min(st)

    def sp_rec(self):
        visited = []
        to_visit = [(self.start, 0, 0), ]
        while len(to_visit) > 0:
            # get nearest node
            m = (0, to_visit[0][1])
            for i, visiting in enumerate(to_visit):
                if visiting[1] < m[1]:
                    m = (i, visiting[1])

            node, cur_dist, level = to_visit.pop(m[0])

            if node == self.end and level == 0:
                pd(cur_dist)
                return cur_dist

            if level < 0:
                pd('Not visiting', node.name, 'L', level, 'dist', cur_dist)
                continue

            if (node == self.start or node==self.end) and level > 0:
                pd('Not visiting', node.name, 'L', level, 'dist', cur_dist)
                continue

            # print('Visiting', node.name, 'L', level, 'dist', cur_dist)
            visited.append((node, level))

            for link, d in node.links:
                if node.name[-2:] == link.name[-2:]:
                    lc = node.rec
                else:
                    lc = 0
                if (link, level + lc) in visited:
                    continue
                else:
                    for i, to_visit_candidate in enumerate(to_visit):
                        if link == to_visit_candidate[0] and level + lc == to_visit_candidate[2]:
                            if cur_dist + d < to_visit_candidate[1]:
                                to_visit[i] = (link, cur_dist + d, level + lc)
                                link.prev[level+lc] = f'{node.name}-L{level}'
                                break
                    else:
                        to_visit.append((link, cur_dist + d, level + lc))
                        link.prev[level+lc] = f'{node.name}-L{level}'
        # print('Visited:', [(n.name, l) for n, l in visited])
        return -1

    def __str__(self):
        l = [f'{self.width},{self.height}', ]
        for p in self.nodes:
            l.append(str(self.nodes[p]))
        return '\n'.join(l)


def test1(data):
    return 0

def test2(data):
    return 0

def part1(data):
    m = Maze(data)
    m.optimize()
    return m.sp(m.start)

def part2(data):
    pd(data)
    m = Maze(data)
    m.optimize()
    pd(m)
    r = m.sp_rec()
    pd(m.end.prev[0])
    return r

if __name__ == '__main__':

    test_input_1 = '''         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
'''
    test_input_2 = '''                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               
'''
    test_input_3 = '''             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     
'''
    print('Test Part 1:')
    test_eq('Test 1.1', part1, 23, test_input_1)
    test_eq('Test 1.2', part1, 58, test_input_2)
    print()

    test_input_2 = [4,5,6]
    print('Test Part 2:')
    test_eq('Test 2.1', part2, 396, test_input_3)
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
