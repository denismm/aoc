#!/usr/bin/env python3
import sys
from positions import Position

filename = sys.argv[1]

grid:  dict[Position, str] = {}

with open(filename, "r") as f:
    for j, line in enumerate(f):
        for i, char in enumerate(line.rstrip()):
            if char != '.':
                grid[(i, j)] = char
    height = j+1

round_starts = [p for p, v in grid.items() if v == 'O']
round_starts.sort()
for start_pos in round_starts:
    i, j = start_pos
    while (i, j - 1) not in grid and j > 0:
        j -= 1
    new_pos = (i, j)
    if new_pos != start_pos:
        del grid[start_pos]
        grid[new_pos] = 'O'
total = sum([height - j for (i, j), v in grid.items() if v == 'O'])
print(total)
