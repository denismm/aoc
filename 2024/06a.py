#!/usr/bin/env python3
import sys
from positions import (
    read_char_grid,
    add_direction,
    cardinal_directions,
    direction_symbols,
)

filename = sys.argv[1]

with open(filename, "r") as f:
    _, _, lab = read_char_grid(f, skip_dots=False)

pos = [k for k, v in lab.items() if v in direction_symbols][0]
dir = direction_symbols.index(lab[pos])
direction = cardinal_directions[dir]
lab[pos] = 'X'
next_pos = add_direction(pos, direction)
while next_pos in lab:
    if lab[next_pos] == '#':
        dir = (dir + 1) % 4
        direction = cardinal_directions[dir]
    else:
        pos = next_pos
        lab[next_pos] = 'X'
    next_pos = add_direction(pos, direction)
print(len([k for k, v in lab.items() if v == 'X']))
