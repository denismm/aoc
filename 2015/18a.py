#!/usr/bin/env python3
import sys
from positions import Position, zeta_directions, add_direction, read_set_grid

filename = sys.argv[1]
generations: int = int(sys.argv[2])
lit: set[Position] = set()
size: int = 0  # assertion: dealing with squares

with open(filename, "r") as f:
    size, _, lit = read_set_grid(f)

for i in range(generations):
    new_lit: set[Position] = set()
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
