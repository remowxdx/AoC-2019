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

