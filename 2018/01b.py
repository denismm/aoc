#!/usr/bin/env python3
import sys

filename = sys.argv[1]

frequency = 0
seen: set[int] = { frequency }

with open(filename, "r") as f:
    shifts: list[int] = [int(line) for line in f]

while True:
    for shift in shifts:
        frequency += shift
        if frequency in seen:
            print(frequency)
            exit(0)
        else:
            seen.add(frequency)
