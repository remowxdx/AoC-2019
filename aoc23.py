#!/usr/bin/env python3

from aoc import *
from computer import Computer

pd = Debug(True)
DAY = 23

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [int(c) for c in lines[0].strip().split(',')]

def test1(data):
    return 0

def test2(data):
    return 0

class Packet:
    def __init__(self, address, x, y):
        self.address = address
        self.x = x
        self.y = y

class Network:
    def __init__(self, data, part=1):
        self.solution = None
        self.part = part
        self.idle = 0
        self.loops = 0
        self.nat_last_sent = None
        self.cs = [[Computer(data.copy()), 'WAIT'] for i in range(50)]
        for i, c in enumerate(self.cs):
            print(f'Initializing computer {i}.')
            c[0].send(i)
            c[1] = c[0].run()
        self.nat = (None, None)

    def loop(self):
        self.loops += 1
        while self.solution is None:
            self.process_packets()
        return self.solution

    def process_packets(self):
        self.idle = 0
        for i in range(len(self.cs)):
            p = self.get_packet(i)
            if p is None:
                self.send_empty(i)
                self.idle += 1
            else:
                self.send_packet(p)
        if self.idle == len(self.cs):
            if self.nat[0] is not None:
                if self.nat_last_sent == self.nat[1] and self.solution is None:
                    self.solution = self.nat[1]
                self.send_packet(Packet(0, self.nat[0], self.nat[1]))
                self.nat_last_sent = self.nat[1]

    def get_packet(self, i):
        c, status = self.cs[i]
        # print(f'Reading from {i}.', end='')
        address = c.recv()
        if address is None:
            # print('No message.')
            return None
        x = c.recv()
        if x is None:
            raise Exception('Computer sent address but not x.')
        y = c.recv()
        if y is None:
            raise Exception('Computer sent address and x, but not y.')
        p = Packet(address, x, y)
        print(f'Message {i} -> {address}: ({x}, {y}).')
        return p
        
    def send_packet(self, packet):
        if packet.address == 255:
            if self.part == 1 and self.solution is None:
                self.solution = packet.y
            else:
                self.nat = (packet.x, packet.y)
        else:
            i = packet.address
            if i >= 0 and i < 50:
                self.cs[i][0].send(packet.x)
                self.cs[i][0].send(packet.y)
                if self.cs[i][1] == 'WAIT':
                    self.cs[0][1] = self.cs[i][0].run()

    def send_empty(self, i):
        c, status = self.cs[i]
        if status == 'WAIT':
            c.send(-1)
            self.cs[i][1] = c.run()

def part1(data):
    n = Network(data)
    r = n.loop()
    return r

def part2(data):
    n = Network(data, 2)
    r = n.loop()
    return r

if __name__ == '__main__':

#    test_input_1 = [1,2,3]
#    print('Test Part 1:')
#    test_eq('Test 1.1', test1, 42, test_input_1)
#    print()
#
#    test_input_2 = [4,5,6]
#    print('Test Part 2:')
#    test_eq('Test 2.1', test2, 42, test_input_1)
#    print()
#
    data = get_input(f'input{DAY}')

    r = part1(data)
    if r is not None:
        print('Part 1:', r)
        check_solution(DAY, 1, r)

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        check_solution(DAY, 2, r)
