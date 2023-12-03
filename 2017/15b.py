#!/usr/bin/env python3
import sys
from typing import Iterator

filename = sys.argv[1]

with open(filename, 'r') as f:
    start_values = [int(line.rstrip().split()[-1]) for line in f]

values = list(start_values)

repetitions = 5 * 1000 * 1000

factors = (16807, 48271)

filters = (4, 8)

bigmod = 2147483647

def make_generator(start: int, factor: int, filter: int) -> Iterator[int]:
    value = start
    while True:
        new_value = (value * factor) % bigmod
        if new_value % filter == 0:
            yield new_value
        value = new_value


i = 0
matches = 0
for (a, b) in zip(
        make_generator(start_values[0], factors[0], filters[0]),
        make_generator(start_values[1], factors[1], filters[1]),):
    if a % 2**16 == b % 2**16:
        matches +=1
    i += 1
    if i >= repetitions:
        print(matches)
        exit(0)

