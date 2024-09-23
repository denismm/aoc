#!/usr/bin/env python3
import sys

filename = sys.argv[1]

frequency = 0

with open(filename, "r") as f:
    for line in f:
        frequency += int(line)
print(frequency)
