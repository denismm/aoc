#!/usr/bin/env python3

import sys

filename = sys.argv[1]

total = 0
with open(filename, 'r') as f:
    for line in f:
        bank = [int(s) for s in line.rstrip()]
        tens = max(bank[:-1])
        ten_pos = bank.index(tens)
        ones = max(bank[ten_pos + 1:])
        joltage = tens * 10 + ones
        # print(joltage)
        total += joltage
print(total)
