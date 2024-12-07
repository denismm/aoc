#!/usr/bin/env python3
import sys
from positions import (
    read_char_grid,
    StrGrid,
    add_direction,
    cardinal_directions,
    direction_symbols,
)

filename = sys.argv[1]

with open(filename, "r") as f:
    _, _, lab = read_char_grid(f, skip_dots=False)

def loop_check(lab: StrGrid) -> bool:
    pos = [k for k, v in lab.items() if v in direction_symbols][0]
    dir = direction_symbols.index(lab[pos])
    direction = cardinal_directions[dir]
    lab[pos] = 'X'
    next_pos = add_direction(pos, direction)
    while next_pos in lab:
        if lab[next_pos] == '#':
            dir = (dir + 1) % 4
            direction = cardinal_directions[dir]
        elif lab[next_pos] == direction_symbols[dir]:
            return True
        else:
            pos = next_pos
            lab[next_pos] = direction_symbols[dir]
        next_pos = add_direction(pos, direction)
    return False

obstruction_count = 0
for obstruction in lab.keys():
    if lab[obstruction] == '.':
        new_lab = dict(lab)
        new_lab[obstruction] = '#'
        if loop_check(new_lab):
            obstruction_count += 1

print(obstruction_count)
