#!/usr/bin/env python3

import sys
from positions import Position
from itertools import combinations

filename = sys.argv[1]

tiles: list[Position] = []
with open(filename, 'r') as f:
    for line in f:
        points = [int(s) for s in line.rstrip().split(',')]
        tiles.append(tuple(points))

big_area: int = 0

for source, target in combinations(tiles, 2):
    area = (abs(source[0] - target[0]) + 1) * (abs(source[1] - target[1]) + 1)
    big_area = max(big_area, area)

print(big_area)
