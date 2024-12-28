#!/usr/bin/env python3
import sys
from itertools import combinations
from positions import SetGrid, read_set_grid

filename = sys.argv[1]

schematics: list[SetGrid] = []

with open(filename, "r") as f:
    while f:
        try:
            _, _, grid = read_set_grid(f)
            schematics.append(grid)
        except ValueError as e:
            if str(e) == 'empty grid':
                break

# we don't actually care which are keys and which are locks
# just look for overlaps

fits = 0
for (a, b) in combinations(schematics, 2):
    if not (a & b):
        fits += 1

print(fits)
