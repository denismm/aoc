#!/usr/bin/env python3
import sys
from positions import Position, read_char_grid, add_direction
filename = sys.argv[1]

with open(filename, 'r') as f:
    width, height, grid = read_char_grid(f)

found = 0

x_directions = ((1, 1), (-1, 1), (-1, -1), (1, -1))
ok_feet = set("MS")
ms_patterns = { "MSSM", "MMSS", "SMMS", "SSMM"}
for pos in grid:
    if grid[pos] == 'A':
        feet: list[str] = []
        for dir in x_directions:
            test: Position = add_direction(pos, dir)
            foot = grid.get(test, "")
            if foot not in ok_feet:
                break
            feet.append(foot)
        if ''.join(feet) in ms_patterns:
            found += 1
print(found)
