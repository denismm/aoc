#!/usr/bin/env python3
import sys
from positions import Position, zeta_directions, add_direction
from itertools import product

filename = sys.argv[1]
generations: int = int(sys.argv[2])
lit: set[Position] = set()
size: int = 0   # assertion: dealing with squares

with open(filename, 'r') as f:
    for y, line in enumerate(f):
        line = line.rstrip()
        if not size:
            size = len(line)
        for x, char in enumerate(line):
            if char == '#':
                lit.add((x, y))

edges = (0, size - 1)
corners = set(product(edges, repeat=2))
# make sure they're on
lit |= corners

for i in range(generations):
    new_lit: set[Position] = set(corners)
    for i in range(size):
        for j in range(size):
            point = (i, j)
            neighbors = 0
            for dir in zeta_directions:
                if add_direction(point, dir) in lit:
                    neighbors += 1
            if neighbors == 3 or (neighbors == 2 and point in lit):
                new_lit.add(point)
    lit = new_lit
print(len(lit))
# for j in range(size):
#     print(''.join(['#' if (i,j) in lit else '.' for i in range(size)]))
