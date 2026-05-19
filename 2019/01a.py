#!/usr/bin/env python3

import sys

filename = sys.argv[1]

sum_a = 0
sum_b = 0
with open(filename, 'r') as f:
    for line in f:
        mass = int(line)
        fuel = mass // 3 - 2
        sum_a += fuel
        subtotal = 0
        while (fuel > 0):
            subtotal += fuel
            fuel = fuel // 3 - 2
        # print(subtotal)
        sum_b += subtotal

print(sum_a)
print(sum_b)
