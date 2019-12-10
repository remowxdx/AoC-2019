#!/usr/bin/env python3

import os.path

class Debug():
    def __init__(self, enable=True):
        self.enabled = enable

    def enable(self, enabled = True):
        self.enabled = enabled

    def disaable(self, disabled = True):
        self.enabled = disabled

    def __call__(self, *args, **kwargs):
        if self.enabled:
            print(*args, **kwargs)

def test_eq(name, func, result, *args, **kwargs):
    print(f' * Testing {name}...', end=' ')
    r = func(*args, **kwargs)
    if r == result:
        print(f'\x1b[1;32mOK!\x1b[0m ☺ ')
    else:
        print(f'\x1b[1;41mNOT OK\x1b[0m ☹ ')
        print(f'\tExpected {result}, found {r}')
    

def save_solution(day, part, solution):
    filename =  f'solutions/solution{day}_{part}'
    with open(filename, 'w') as f:
        f.write(str(solution))

def check_solution(day, part, candidate):
    filename =  f'solutions/solution{day}_{part}'
    if not os.path.isfile(filename):
        print(f'Day {day}, part {part} solution not present.')
        return
    with open(filename, 'r') as f:
        solution = f.read()

    if str(candidate) == solution:
        print(f'Day {day}, part {part} \x1b[1;32mOK!\x1b[0m ☺ ')
    else:
        print(f'Day {day}, part {part} \x1b[1;41mNOT OK\x1b[0m ☹ ')
        print(f'\tExpected {solution}, found {candidate}')

def retrieve_input(day):
    url = 'https://adventofcode.com/2019/day/{}/input'
    cookie = 'session=53616c7465645f5fa19b27d6da38447d4c5e3497d395321a717272e8216f40a40301ebae38cfd12b021e5004a47483e4'
    req = urllib.request.Request(url.format(day))
    req.add_header('Cookie', cookie)
    r = urllib.request.urlopen(req)
    s = r.read()
    print(s)
    with open(f'input{day}', 'wb') as f:
        f.write(s)


if __name__ == '__main__':
    import sys
    import urllib.request
    import os.path
    import stat

    if len(sys.argv) < 2:
        print('No day found.')
        exit(1)

    day_str = sys.argv[1]
    if not day_str.isdecimal():
        print('No numeric day.')
        exit(2)

    day = int(day_str)

    retrieve_input(day)

    filename = f'aoc{day:02}.py'

    scaf = """#!/usr/bin/env python3

from aoc import *

pd = Debug(True)
DAY = {day}

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

def test1(data):
    return 0

def test2(data):
    return 0

def part1(data):
    return None

def part2(data):
    return None

if __name__ == '__main__':

    test_input_1 = [1,2,3]
    print('Test Part 1:')
    test_eq('Test 1.1', test1, 42, test_input_1)
    print()

    test_input_2 = [4,5,6]
    print('Test Part 2:')
    test_eq('Test 2.1', test2, 42, test_input_1)
    print()

    data = get_input(f'input{DAY}')

    r = part1(data)
    if r is not None:
        print('Part 1:', r)
        save_solution(DAY, 1, r)

    r = part2(data)
    if r is not None:
        print('Part 2:', r)
        save_solution(DAY, 2, r)
"""

    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            f.write(scaf.replace('{day}', str(day)))
            os.chmod(filename, stat.S_IRUSR | stat.S_IXUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)
