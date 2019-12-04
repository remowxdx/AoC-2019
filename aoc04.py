#!/usr/bin/env python3

from aoc import *

pd = Debug(False)

def get_input(file_name):
    data = []
    with open(file_name, 'r') as f:
        data = f.readlines()
    return [int(d) for d in data[0].split('-')]

def get_digits(n):
    digits = []
    i = n
    while i > 0:
        digits.append(i % 10)
        i = i // 10
    digits.reverse()
    return digits

def check_part_1(i):
    digits = get_digits(i)
    l = 0
    adj = False
    for d in digits:

        # digits should be in ascending order
        if d < l:
            return False

        # At least 2 equal adjacent digits
        if d == l:
            adj = True

        l = d
    return adj

def check_part_2(i):

    digits = get_digits(i)
    l = 0
    adj = 1
    runs = []
    for d in digits: # 67999

        # digits should be in ascending order
        if d < l:
            return False

        # At least 1 run of lenght 2
        elif d == l:
            adj += 1

        else:
            runs.append(adj)
            adj = 1
        l = d
    runs.append(adj)
    return 2 in runs

def count_valid_passwords(data, check):
    return len(list(filter(check, range(data[0], data[1] + 1))))
#    valid = []
#    for i in range(data[0], data[1] + 1):
#        if check(i):
#            valid.append(i)
#    return len(valid)

def part1(data):
    return count_valid_passwords(data, check_part_1)

def part2(data):
    return count_valid_passwords(data, check_part_2)

if __name__ == '__main__':

    print('Testing Part 1')
    test_eq('Ex1.1', check_part_1, True, 111111)
    test_eq('Ex1.2', check_part_1, False, 223450)
    test_eq('Ex1.3', check_part_1, False, 123789)

    print()
    print('Testing Part 2')
    test_eq('Ex2.1', check_part_2, True, 112233)
    test_eq('Ex2.2', check_part_2, False, 123444)
    test_eq('Ex2.3', check_part_2, True, 111122)

    print()

    data = get_input('input4')

    p1 = part1(data)
    print(f'Part 1: {p1}')

    p2 = part2(data)
    print(f'Part 2: {p2}')

