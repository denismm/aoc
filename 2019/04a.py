#!/usr/bin/env python3

import sys

pwd_range = [int(s) for s in sys.argv[1].split('-')]

def check_pwd(candidate: int) -> bool:
    pwd_str = str(candidate)
    double = False
    for i in range(5):
        a = pwd_str[i]
        b = pwd_str[i + 1]
        if a == b:
            double = True
        elif a > b:
            return False
    return double

valids = 0

for pwd_candidate in range(pwd_range[0], pwd_range[1] + 1):
    if check_pwd(pwd_candidate):
        valids += 1
print(valids)
