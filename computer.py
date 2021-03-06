#!/usr/bin/env python3

from aoc import *

pd = Debug(False)

class Computer:
    def __init__(self, data, inp=[]):
        self.opcodes = {
                1: self.add,
                2: self.mul,
                3: self.input,
                4: self.output,
                5: self.jump_if_true,
                6: self.jump_if_false,
                7: self.less_than,
                8: self.equals,
                9: self.relative_base_offset,
                99: self.halt
                }

        self.memory = data
        self.input = inp
        self.output = []
        self.output_index = 0

        self.ip = 0
        self.rb = 0

    def step(self):
        instruction = self.get_addr(self.ip)
        opcode = instruction % 100 # last 2 digits
        pd('Opcode: ', opcode, 'at', self.ip)
        self.modes = ((instruction // 100) % 10, (instruction // 1000) % 10, (instruction // 10000) % 10, )

        if opcode not in self.opcodes:
            pd("Error at {}, instruction {} unknown.".format(self.ip, opcode))
            raise Exception("Error at {}, instruction {} unknown.".format(self.ip, opcode))
        return self.opcodes[opcode]()


    def run(self):

        r = self.step()
        while r == 'OK':
            r = self.step()

        if r == 'WAIT':
            pd('Waiting for input...')

        elif r == 'HALT':
            # print('Computer halted!')
            pd(r)

        else:
            raise Exception("Error at {}, abnormal halt.".format(self.ip))
        return r

    def send(self, value):
        self.input.append(value)

    def recv(self):
        if self.output_index < len(self.output):
            out = self.output[self.output_index]
            self.output_index += 1
            return out
        return None

    def get_param(self, param):
        if self.modes[param - 1] == 0:
            return self.get_ref(self.ip + param)
        elif self.modes[param - 1] == 1:
            return self.get_addr(self.ip + param)
        elif self.modes[param - 1] == 2:
            return self.get_rel(self.ip + param)
        else:
            raise Exception(f'Parameter mode unknown at {self.ip}')
            return None

    def set_param(self, param, val):
        pd('Set', val, 'mode', self.modes[param - 1], 'at', self.ip + param)
        if self.modes[param - 1] == 0:
            return self.set_ref(self.ip + param, val)
        elif self.modes[param - 1] == 1:
            return self.set_addr(self.ip + param, val)
        elif self.modes[param - 1] == 2:
            return self.set_rel(self.ip + param, val)
        else:
            raise Exception(f'Parameter mode unknown at {self.ip}')
            return None


    def add(self):
        op1 = self.get_param(1)
        op2 = self.get_param(2)
        self.set_param(3, op1 + op2)
        self.ip += 4
        return 'OK'

    def mul(self):
        op1 = self.get_param(1)
        op2 = self.get_param(2)
        self.set_param(3, op1 * op2)
        self.ip += 4
        return 'OK'
    
    def input(self):
        if len(self.input) > 0:
            self.set_param(1, self.input.pop(0))
            self.ip += 2
            return 'OK'
        return 'WAIT'

    def output(self):
        o = self.get_param(1)
        self.output.append(o)
        self.ip += 2
        return 'OK'

    def jump_if_true(self):
        op1 = self.get_param(1)
        op2 = self.get_param(2)
        if op1 != 0:
            self.ip = op2
            return 'OK'
        self.ip += 3
        return 'OK'

    def jump_if_false(self):
        op1 = self.get_param(1)
        op2 = self.get_param(2)
        if op1 == 0:
            self.ip = op2
            return 'OK'
        self.ip += 3
        return 'OK'

    def less_than(self):
        op1 = self.get_param(1)
        op2 = self.get_param(2)
        if op1 < op2:
            self.set_param(3, 1)
        else:
            self.set_param(3, 0)
        self.ip += 4
        return 'OK'

    def equals(self):
        op1 = self.get_param(1)
        op2 = self.get_param(2)
        if op1 == op2:
            self.set_param(3, 1)
        else:
            self.set_param(3, 0)
        self.ip += 4
        return 'OK'

    def relative_base_offset(self):
        op1 = self.get_param(1)
        self.rb += op1
        self.ip += 2
        return 'OK'

    def halt(self):
        return 'HALT'

    def get_addr(self, addr):
        if addr >= len(self.memory):
            # self.memory.extend([0 for _ in range(addr - len(self.memory))])
            return 0
        return self.memory[addr]

    def set_addr(self, addr, val):
        if addr >= len(self.memory):
            self.memory.extend([0 for _ in range(addr - len(self.memory) + 1)])
        self.memory[addr] = val

    def get_ref(self, addr):
        return self.get_addr(self.get_addr(addr))

    def set_ref(self, addr, val):
        self.set_addr(self.get_addr(addr), val)

    def get_rel(self, addr):
        return self.get_addr(self.rb + self.get_addr(addr))

    def set_rel(self, addr, val):
        self.set_addr(self.rb + self.get_addr(addr), val)

    def show(self):
        memory_str = []
        for i in range(len(self.memory)):
            if i == self.ip:
                memory_str.append('\x1b[1;41m {} \x1b[0m'.format(self.memory[i]))
            else:
                memory_str.append('{}'.format(self.memory[i]))
        print(' '.join(memory_str))

    def get_output(self):
        return self.output
