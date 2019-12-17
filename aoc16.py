#!/usr/bin/env python3

from aoc import *

pd = Debug(False)
DAY = 16

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [int(i) for i in lines[0].strip()]

def fft_phase_1(data):
    r = []
    for n, i in enumerate(data):
        s = 0
        rl = n + 1
        i = n
        while i < len(data):
            s += sum(data[i:i+rl])
            i += 4 * rl
        i = n + 2 * rl 
        while i < len(data):
            s -= sum(data[i:i+rl])
            i += 4 * rl
        r.append(abs(s) % 10)
    return r

def fft_phase_2(data, offset):
    r = []
    s = 0
    for i in range(len(data) - offset):
        n = len(data) - i - 1
        s += data[n]
        r.append(s)
    t = [abs(s) % 10 for s in r]
    t.extend([0] * offset)
    t.reverse()
    return t

def fft_1(data, phases):
    r = data.copy()
    for i in range(phases):
        pd(f'Phase {i}...   ')
        r = fft_phase_1(r)
        pd('\x1b[2A')
    return r

def fft_2(data, phases, offset):
    r = data.copy()
    for i in range(phases):
        pd(f'Phase {i}...   ')
        r = fft_phase_2(r, offset)
        pd('\x1b[2A')
    return r

def test1(data, phases):
    a = [int(i) for i in data]
    return ''.join([str(c) for c in fft_1(a, phases)[:8]])

def test2(data):
    a = [int(i) for i in data]
    real_data = a * 10_000
    offset = int(data[:7])
    pd(offset)
    r = fft_2(real_data, 100, 0)
    # print(r)
    return ''.join([str(c) for c in r])[offset:offset+8]

def part1(data, phases):
    return ''.join([str(c) for c in fft_1(data, phases)[:8]])

def part2(data):
    real_data = data * 10_000
    offset = 0
    for i in data[:7]:
        offset = offset * 10 + i
    pd(offset)
    r = fft_2(real_data, 100, offset)
    pd(r)
    return ''.join([str(c) for c in r])[offset:offset+8]

if __name__ == '__main__':

    print('Test Part 1:')
    test_eq('Test 1.1.1', test1, '48226158', '12345678', 1)
    test_eq('Test 1.1.2', test1, '34040438', '12345678', 2)
    test_eq('Test 1.1.3', test1, '03415518', '12345678', 3)
    test_eq('Test 1.1.4', test1, '01029498', '12345678', 4)
    test_eq('Test 1.2', test1, '24176176', '80871224585914546619083218645595', 100)
    test_eq('Test 1.3', test1, '73745418', '19617804207202209144916044189917', 100)
    test_eq('Test 1.4', test1, '52432133', '69317163492948606335995924319873', 100)
    print()

    print('Test Part 2:')
    # test_eq('Test 2.1', test2, '84462026', '03036732577212944063491565474664')
    print()

    data = get_input(f'input{DAY}')

    r = part1(data, 100)
    if r is not None:
        print('Part 1:', r)
        check_solution(DAY, 1, r)

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        check_solution(DAY, 2, r)
