#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    start_values = [int(line.rstrip().split()[-1]) for line in f]

values = list(start_values)

repetitions = 40 * 1000000

factors = (16807, 48271)

bigmod = 2147483647

matches = 0

for i in range(repetitions):
    new_values = [ (a * b) % bigmod for a, b in zip(values, factors)]
    if new_values[0] % 2 ** 16 == new_values[1] % 2 ** 16:
        matches += 1
    values = new_values

print(matches)
