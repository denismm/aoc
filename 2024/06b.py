#!/usr/bin/env python3
import sys
from tqdm import tqdm
from positions import (
    Position,
    read_char_grid,
    StrGrid,
    add_direction,
    cardinal_directions,
    direction_symbols,
)

filename = sys.argv[1]

with open(filename, "r") as f:
    _, _, lab = read_char_grid(f, skip_dots=False)

class FoundLoop(Exception):
    pass

def run_lab(lab: StrGrid) -> list[Position]:
    pos = [k for k, v in lab.items() if v in direction_symbols][0]
    dir = direction_symbols.index(lab[pos])
    direction = cardinal_directions[dir]
    next_pos = add_direction(pos, direction)
    while next_pos in lab:
        if lab[next_pos] == '#':
            dir = (dir + 1) % 4
            direction = cardinal_directions[dir]
        elif lab[next_pos] == direction_symbols[dir]:
            raise FoundLoop()
        else:
            pos = next_pos
            lab[next_pos] = direction_symbols[dir]
        next_pos = add_direction(pos, direction)
    return [ k for k, v in lab.items() if v in direction_symbols ]

obstruction_count = 0
possible_obs = run_lab(dict(lab))
for obstruction in tqdm(possible_obs):
    if lab[obstruction] == '.':
        new_lab = dict(lab)
        new_lab[obstruction] = '#'
        try:
            _ = run_lab(new_lab)
        except FoundLoop:
            obstruction_count += 1

print(obstruction_count)
