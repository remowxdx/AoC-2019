#!/usr/bin/env python3

from aoc import *
from computer_gen import Computer

from itertools import permutations

pd = Debug(False)

def get_input(file_name):
    lines = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
    # return [int(d) for d in data]
    raw_data = lines[0].split(',')
    data = [int(d) for d in raw_data]
    return data

def run_amp(program, phase, signal):
    c = Computer(program.copy())
    c.send(phase)
    c.send(signal)
    c.run()
    out = c.recv()
    return out

def run_serie(program, phases):
    signal = 0
    pd(phases, end=': ')
    out = []
    for phase in phases:
        signal = run_amp(program, phase, signal)
        out.append(str(signal))
    pd(" -> ".join(out))
    return signal

def part1(program):
    max = 0
    for phases in permutations([0,1,2,3,4]):
        r = run_serie(program, phases)
        if r > max:
            max = r
            max_phases = phases
    pd(max_phases)
    return max

def part2(data):
    max = 0
    for phases in permutations([5,6,7,8,9]):
        s = System(data, phases)
        r = s.run()
        if r > max:
            max = r
            max_phases = phases
    pd(max_phases)
    return max

def test_phases(program):
    max = 0
    for phases in permutations([0,1,2,3,4]):
        r = run_serie(program, phases)
        if r > max:
            max = r
            max_phases = phases
    pd(max_phases)
    return max

class System:
    def __init__(self, program, phases):
        self.phases = phases
        self.signal = 0
        self.amp = -1
        self.amps = [Computer(program.copy(), [phases[i], ]) for i in range(5)]
        for amp in self.amps:
            amp.run()

    def feed_signal(self):
        self.amp += 1
        self.amp = self.amp % 5
        amp = self.amps[self.amp]
        amp.send(self.signal)
        r = amp.run()
        self.signal = amp.recv()
        pd(self.signal, '->', end='')
        return r

    def run(self):
        r = 'OK'
        while True:
            r = self.feed_signal()
            if self.amp == 4 and r == 'HALT':
                pd(self.signal)
                return self.signal
        return ':-('

if __name__ == '__main__':
    test_program_1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    test_program_2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    test_program_3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    print('Test Amp')
    test_eq('Test 1.1', test_phases, 43210, test_program_1)
    test_eq('Test 1.2', test_phases, 54321, test_program_2)
    test_eq('Test 1.3', test_phases, 65210, test_program_3)
    print()

    print('Test cycling amps:')
    data = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    s = System(data, [9,8,7,6,5])
    test_eq('Test 2.1a', s.run, 139629729)
    test_eq('Test 2.1b', part2, 139629729, data)
    data = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
        -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
        53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    s = System(data, [9,7,8,5,6])
    test_eq('Test 2.2a', s.run, 18216)
    test_eq('Test 2.2b', part2, 18216, data)
    print()

    data = get_input('input7')

    r = part1(data)
    print(f'Part 1: {r}')

    print()
    r = part2(data)
    print(f'Part 2: {r}')

#    print('Test Compare')
#    test_eq('Pos 1 == 8', test_out, [0, ], [3,9,8,9,10,9,4,9,99,-1,8], echo(4))
#    print()
#
#    r = part2(data)
#    print(f'Part 2: {r}')
