#!/usr/bin/env python3

from aoc import *

pd = Debug(False)
DAY = 14

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

class Factory:

    def __init__(self, reactions):
        self.parse_reactions(reactions)
        self.stock = {}

    def parse_reactions(self, lines):
        self.reactions = {}
        for line in lines:
            if line.strip() == '':
                continue
            reaction = self.parse_reaction(line)
            self.reactions[reaction[0]] = (reaction[1], reaction[2])
        return self.reactions

    @staticmethod
    def parse_reaction(line):
        # pd('Line:', line)
        react = line.strip().split('=>')
        if len(react) != 2:
            raise Exception(f'This is no reaction (no "=>"): {line}.')
        res = react[1].strip().split(' ')
        reagents = {}
        reag = react[0].strip().split(', ')
        for r in reag:
            rr = r.strip().split(' ')
            reagents[rr[1]] = int(rr[0])
        return res[1], int(res[0]), reagents

    def produce(self, chem, qty):

        if chem not in self.stock:
            self.stock[chem] = 0

        # self.stock[chem] -= qty
        rest = self.stock[chem] - qty

        if rest >= 0:
            return qty

        if chem not in self.reactions:
            raise Exception(f'Cannot produce {chem}.')

        (qty_per_reaction, reagents) = self.reactions[chem]

        n, r = divmod(rest, qty_per_reaction)

        for rc in reagents:
            rq = self.produce(rc, reagents[rc] * (-n))
            self.stock[rc] -= rq

        self.stock[chem] -= rest - r

        return qty

    def remove_from_stock(self, chem, qty=None):

        if chem not in self.stock:
            self.stock[chem] = 0

        if qty is None:
            qty = self.stock[chem]

        ret = min(qty, self.stock[chem])
        self.stock[chem] -= ret
        return ret

    def add_to_stock(self, chem, qty=1):
        if chem not in self.stock:
            self.stock[chem] = 0
        self.stock[chem] += qty
        
    
def test1(data):
    stocked = 10000000
    f = Factory(data)
    f.add_to_stock('ORE', stocked)
    fuel = f.produce('FUEL', 1)
    # pd(f.stock)
    return stocked - f.stock['ORE']

def test2(data):

    MAX = 1000000000000

    f = Factory(data)
    f.add_to_stock('ORE', MAX)

    fuel = f.produce('FUEL', 1)
    f.remove_from_stock('FUEL', 1)
    base = MAX - f.stock['ORE']

    n = f.stock['ORE'] // base
    while n > 0:
        f.produce('FUEL', n)
        fuel += f.remove_from_stock('FUEL')
        n = f.stock['ORE'] // base
        pd('Rest:', f.stock['ORE'], base, n)

    return fuel

def part1(data):
    stocked = 10000000
    f = Factory(data)
    f.add_to_stock('ORE', stocked)
    fuel = f.produce('FUEL', 1)
    return stocked - f.stock['ORE']

def part2(data):
    MAX = 1000000000000

    f = Factory(data)
    f.add_to_stock('ORE', MAX)

    f.produce('FUEL', 1)
    fuel = f.remove_from_stock('FUEL')
    base = MAX - f.stock['ORE']

    n = f.stock['ORE'] // base
    while n > 0:
        f.produce('FUEL', n)
        fuel += f.remove_from_stock('FUEL')
        n = f.stock['ORE'] // base
        pd('Rest:', f.stock['ORE'], base, n)

    return fuel

if __name__ == '__main__':

    test_input_1 = '''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
'''.split('\n')
    test_input_2 = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
'''.split('\n')
    test_input_3 = '''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
'''.split('\n')
    test_input_4 = '''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
'''.split('\n')
    test_input_5 = '''171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX

'''.split('\n')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 31, test_input_1)
    test_eq('Test 1.2', test1, 165, test_input_2)
    test_eq('Test 1.3', test1, 13312, test_input_3)
    test_eq('Test 1.4', test1, 180697, test_input_4)
    test_eq('Test 1.5', test1, 2210736, test_input_5)
    print()

    test_input_2 = [4,5,6]
    print('Test Part 2:')
    test_eq('Test 2.3', test2, 82892753, test_input_3)
    test_eq('Test 2.4', test2, 5586022, test_input_4)
    test_eq('Test 2.5', test2, 460664, test_input_5)
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
