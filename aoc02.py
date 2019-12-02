#!/usr/bin/env python3

def get_input(file_name):
    data = []
    with open(file_name, 'r') as f:
        data = f.readlines()
    # return [int(d) for d in data]
    return data[0].split(',')

class Machine:
    def __init__(self, data):
        self.memory = data
        self.ip = 0
        self.opcodes = {
                1: self.add,
                2: self.mul,
                99: self.halt
                }

    def exec_one(self):
        opcode = self.memory[self.ip]
        if opcode in self.opcodes:
            return self.opcodes[opcode]()
        print("Error at {}, instruction {} unknown.".format(self.ip, opcode))
        return 'ERROR'


    def run(self):
        r = self.exec_one()
        while r == 'OK':
            r = self.exec_one()
        print(r)

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

    def res(self):
        return self.memory[0]

    def show(self):
        print(self.memory)
        print(self.ip)

def search(data, val):
    for noun in range(100):
        for verb in range(100):
            m = Machine(data.copy())
            m.set_addr(1, noun)
            m.set_addr(2, verb)
            m.run()
            if m.res() == val:
                print('Found:', noun, verb)
                print('Result:', 100 * noun + verb)
                return (noun, verb)
    return False

if __name__ == '__main__':
    # rd = ['1', '0', '0', '0', '99']
    # rd = ['2', '3', '0', '3', '99']
    # rd = ['2', '4', '4', '5', '99', '0']
    # rd = ['1', '1', '1', '4', '99', '5', '6', '0', '99']
    rd = get_input('input2')
    orig = [int(d) for d in rd]
    search(orig, 19690720)
