#!/usr/bin/env python3
import sys
from positions import Position, read_char_grid, add_direction, scale_direction, zeta_directions
filename = sys.argv[1]

with open(filename, 'r') as f:
    width, height, grid = read_char_grid(f)

target = 'XMAS'
found = 0

for pos in grid:
    if grid[pos] == 'X':
        for dir in zeta_directions:
            for i in range(1, 4):
                test: Position = add_direction(pos, scale_direction(dir, i))
                miss = False
                if grid.get(test, "") != target[i]:
                    miss = True
                    break
            if not miss:
                found += 1
print(found)
