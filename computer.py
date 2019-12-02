#!/usr/bin/env python3

from aoc import *

pd = Debug(False)

class Computer:
    def __init__(self, data):
        self.memory = data
        self.ip = 0
        self.opcodes = {
                1: self.add,
                2: self.mul,
                99: self.halt
                }

    def step(self):
        opcode = self.memory[self.ip]
        if opcode not in self.opcodes:
            pd("Error at {}, instruction {} unknown.".format(self.ip, opcode))
            raise Exception("Error at {}, instruction {} unknown.".format(self.ip, opcode))
        return self.opcodes[opcode]()


    def run(self):

        r = self.step()
        while r == 'OK':
            r = self.step()

        if r != 'HALT':
            raise Exception("Error at {}, abnormal halt.".format(self.ip))
        else:
            pd(r)

    def add(self):
        op1 = self.get_ref(self.ip + 1)
        op2 = self.get_ref(self.ip + 2)
        self.set_ref(self.ip + 3, op1 + op2)
        self.ip += 4
        return 'OK'

    def mul(self):
        op1 = self.get_ref(self.ip + 1)
        op2 = self.get_ref(self.ip + 2)
        self.set_ref(self.ip + 3, op1 * op2)
        self.ip += 4
        return 'OK'
    
    def halt(self):
        return 'HALT'

    def get_addr(self, addr):
        return self.memory[addr]

    def set_addr(self, addr, val):
        self.memory[addr] = val

    def get_ref(self, addr):
        return self.memory[self.memory[addr]]

    def set_ref(self, addr, val):
        self.memory[self.memory[addr]] = val

    def show(self):
        memory_str = []
        for i in range(len(self.memory)):
            if i == self.ip:
                memory_str.append('\x1b[1;41m {} \x1b[0m'.format(self.memory[i]))
            else:
                memory_str.append('{}'.format(self.memory[i]))
        print(' '.join(memory_str))

