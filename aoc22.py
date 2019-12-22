#!/usr/bin/env python3

from aoc import *
from math import gcd

pd = Debug(True)
DAY = 22

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

class Deck:
    def __init__(self, num_cards):
        self.stack = [c for c in range(num_cards)]

    def deal_into_new_stack(self):
        self.stack.reverse()

    def cut(self, n):
        n = self.stack[n:] + self.stack[:n]
        self.stack = n

    def deal_with_increment(self, inc):
        n = [0] * len(self.stack)
        i = 0
        for c in self.stack:
            n[i] = c
            i = (i + inc) % len(self.stack)
        self.stack = n

    def get_position(self, pos):
        return self.stack[pos]

    def get_card_position(self, card):
        return self.stack.index(card)

    def __str__(self):
        return 'Deck: ' + ' '.join([str(c) for c in self.stack])

    def do_move(self, move):
        move = move.strip()
        if move == 'deal into new stack':
            # print('deal into new stack')
            self.deal_into_new_stack()
        else:
            s = move.split(' ')
            if s[0] == 'cut':
                # print('cut', int(s[1]))
                self.cut(int(s[1]))
            else:
                # print('deal with increment', int(s[3]))
                self.deal_with_increment(int(s[3]))

class FollowCard:
    def __init__(self, num_cards, card):
        self.n = num_cards
        self.card = card
        self.pos = card

    def deal_into_new_stack(self):
        self.pos = self.n - self.pos - 1

    def cut(self, p):
        self.pos = (self.pos - p) % self.n

    def deal_with_increment(self, inc):
        self.pos = (self.pos * inc) % self.n

    def do_move(self, move):
        move = move.strip()
        if move == 'deal into new stack':
            self.deal_into_new_stack()
        else:
            s = move.split(' ')
            if s[0] == 'cut':
                self.cut(int(s[1]))
            else:
                self.deal_with_increment(int(s[3]))

class Shuffler:
    def __init__(self, num_cards):
        self.n = num_cards
        self.a = 1
        self.b = 0

    def deal_into_new_stack(self):
        # y = ax + b   x->n-(ax+b)  => y = -ax + n-b   => a = -a, b=an+b
        self.b = self.n - 1 - self.b
        self.a = -self.a

    def cut(self, p):
        # y =  x-p  ax+b-p
        self.b -= p

    def deal_with_increment(self, inc):
        # y = inc*x  inc*(ax+b)   inc*a*x + inc*b
        self.a *= inc
        self.b *= inc

    def shrink(self):
        self.a = self.a % self.n
        self.b = self.b % self.n

    def do_move(self, move):
        move = move.strip()
        if move == 'deal into new stack':
            self.deal_into_new_stack()
        else:
            s = move.split(' ')
            if s[0] == 'cut':
                self.cut(int(s[1]))
            else:
                self.deal_with_increment(int(s[3]))

    def end_move(self):
        # y = ax+b   ax%n=(y-b)%n   x%n = ia*x-ia*b
        self.a = self.a % self.n
        self.b = self.b % self.n
        self.ia = findModInverse(self.a, self.n)
        self.ib = (-self.ia * self.b) % self.n
        self.a_s = {1: self.a}
        self.b_s = {1: self.b}
        self.ia_s = {1: self.ia}
        self.ib_s = {1: self.ib}
    
    def shuffle(self, card):
        return (self.a * card + self.b) % (self.n)

    def unshuffle(self, card):
        return (self.ia * card + self.ib) % (self.n)

    def nshuffle(self, card, n):
        # a(ax+b)+b = a^2x+ab+b
        if n not in self.a_s or n not in self.b_s:
            self.a_s[n] = (self.a_s[n//2] * self.a_s[n//2]) % self.n
            self.b_s[n] = ((self.a_s[n//2] + 1) * self.b_s[n//2]) % self.n
        return (self.a_s[n] * card + self.b_s[n]) % self.n

    def nunshuffle(self, card, n):
        # a(ax+b)+b = a^2x+ab+b
        if n not in self.ia_s or n not in self.ib_s:
            self.ia_s[n] = (self.ia_s[n//2] * self.ia_s[n//2]) % self.n
            self.ib_s[n] = ((self.ia_s[n//2] + 1) * self.ib_s[n//2]) % self.n
        return (self.ia_s[n] * card + self.ib_s[n]) % self.n

def findModInverse(a, m):
    # Returns the modular inverse of a % m, which is
    # the number x such that a*x % m = 1

    if gcd(a, m) != 1:
        return None # no mod inverse if a & m aren't relatively prime

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def test1(data, num_cards):
    d = Deck(num_cards)
    for move in data:
        d.do_move(move)
        # print(d)
    return str(d)

def test2(data, num_cards, card, repetitions):
    s = Shuffler(num_cards)
    for move in data:
        s.do_move(move)
    s.end_move()

    r = 0
    n = 1
    c = card
    while r < num_cards-1:
        if r + n <= num_cards-1:
            c = s.nshuffle(c, n)
            r += n
        if r + n <= num_cards-1:
            n *= 2
        else:
            if n > 1:
                n = n // 2
    return c

def part1(data, num_cards):
    d = Deck(num_cards)
    for move in data:
        d.do_move(move)
    return d.get_card_position(2019)

# ax+b -> a(ax+b)+b  -> a^2*x + a*b + b
# a(a^2x+ab+b)+b ->  a^3x+a^2b+ab+b

def part2(data, num_cards, card, repetitions):
    s = Shuffler(num_cards)
    for move in data:
        s.do_move(move)
    s.end_move()

    r = 0
    n = 1
    c = card
    while r < repetitions:
        # print(r, n, c)
        if r + n <= repetitions:
            c = s.nunshuffle(c, n)
            r += n
            if r + n < repetitions:
                n *= 2
        else:
            if n > 1:
                n = n // 2
    # print(r, n, c)
    return c

if __name__ == '__main__':

    test_input_1 = ['deal with increment 7',
        'deal into new stack',
        'deal into new stack',
        ]
    test_input_2 = '''deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1'''.split('\n')
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 'Deck: 0 3 6 9 2 5 8 1 4 7', test_input_1, 10)
    test_eq('Test 1.2', test1, 'Deck: 9 2 5 8 1 4 7 0 3 6', test_input_2, 10)
    print()

    print('Test Part 2:')
    test_eq('Test 2.1', test2, 6, test_input_1, 10, 8, 100)
    test_eq('Test 2.2', test2, 3, test_input_2, 10, 8, 1)
    print()

    data = get_input(f'input{DAY}')

    r = part1(data, 10007)
    if r is not None:
        print('Part 1:', r)
        check_solution(DAY, 1, r)

    r = part2(data, 119315717514047, 2020, 101741582076661)
    if r is not None:
        print('Part 2:', r)
        check_solution(DAY, 2, r)
