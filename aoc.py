#!/usr/bin/env python3

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
    
