#!/usr/bin/env python3

import sys

pwd_range = [int(s) for s in sys.argv[1].split('-')]

def check_pwd(candidate: int) -> bool:
    pwd_str = str(candidate)
    double = False
    double_char = "."
    for i in range(5):
        a = pwd_str[i]
        b = pwd_str[i + 1]
        if a == b:
            # if we're still in the same char as a double, kill it
            if double_char == a:
                double = False
            # if we don't already have a double, mark it
            elif not double:
                double = True
                double_char = a
            # if we already have a double but it's a different char, ignore it
            else:
                pass
        elif a > b:
            return False
    return double

valids = 0

for pwd_candidate in range(pwd_range[0], pwd_range[1] + 1):
    if check_pwd(pwd_candidate):
        valids += 1
print(valids)
