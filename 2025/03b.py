#!/usr/bin/env python3

import sys

filename = sys.argv[1]

total = 0
digits = 12
with open(filename, 'r') as f:
    for line in f:
        bank = [int(s) for s in line.rstrip()]
        batteries: list[int] = []
        for d in range(digits):
            end_point = -(digits - d - 1)
            if end_point == 0:
                battery = max(bank)
            else:
                battery = max(bank[:end_point])
            batteries.append(battery)
            start_point = bank.index(battery) + 1
            bank = bank[start_point:]
        joltage = 0
        for battery in batteries:
            joltage *= 10
            joltage += battery
        # print(joltage)
        total += joltage
print(total)
