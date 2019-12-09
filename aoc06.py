#!/usr/bin/env python3

from aoc import *

pd = Debug(False)

def get_input(file_name):
    data = []
    with open(file_name, 'r') as f:
        data = f.readlines()
    return [d.strip().split(')') for d in data]

def create_graph(data):
    pd(data)
    graph = dict([(d[1], d[0]) for d in data])
    pd(graph)
    return graph

def count_node_orbits(node, graph):
    if node == 'COM':
        return 0
    return 1 + count_node_orbits(graph[node], graph)

def count_graph_orbits(graph):
    tot = 0
    for node in graph:
        tot += count_node_orbits(node, graph)
    return tot

def path_to_com(node, graph):
#    if node == 'COM':
#        return []
#    return path_to_com(graph[node], graph).append(node)
    path = []
    cur = graph[node]
    while cur != 'COM':
        path.append(cur)
        cur = graph[cur]
    return path

def part1(data):
    return count_graph_orbits(create_graph(data))

def part2(data, fro, to):
    graph = create_graph(data)
    path1 = path_to_com(fro, graph)
    path2 = path_to_com(to, graph)
    path1.reverse()
    path2.reverse()
    for i in range(min(len(path1), len(path2))):
        if path1[i] != path2[i]:
            return len(path1) - i + len(path2) - i
    return False

if __name__ == '__main__':

    test_raw_data = [
        'COM)B',
        'B)C',
        'C)D',
        'D)E',
        'E)F',
        'B)G',
        'G)H',
        'D)I',
        'E)J',
        'J)K',
        'K)L',
        ]
    test_data = [d.strip().split(')') for d in test_raw_data]

    test_raw_data_2 = [
        'COM)B',
        'B)C',
        'C)D',
        'D)E',
        'E)F',
        'B)G',
        'G)H',
        'D)I',
        'E)J',
        'J)K',
        'K)L',
        'K)YOU',
        'I)SAN',
        ]
    test_data_2 = [d.strip().split(')') for d in test_raw_data_2]

    print('Testing Part 1')
    test_eq('Test Count Orbits', part1, 42, test_data)

    print()
    print('Testing Part 2')
    test_eq('Test Number of Orbital Transfers', part2, 4, test_data_2, 'YOU', 'SAN')

    print()

    data = get_input('input6')

    r = part1(data)
    print(f'Part 1: {r}')
    check_solution(6, 1, r)

    r = part2(data, 'YOU', 'SAN')
    print(f'Part 2: {r}')
    check_solution(6, 2, r)

