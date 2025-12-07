#!/usr/bin/env python3

import sys
from positions import read_char_grid

filename = sys.argv[1]

with open(filename, 'r') as f:
    w, h, grid = read_char_grid(f, skip_dots=False)

splits: int = 0
beams: set[int] = set()
# find start
for x in range(w):
    if grid[(x, 0)] == 'S':
        beams.add(x)
if len(beams) != 1:
    raise ValueError("not one beam")

for y in range(1, h):
    new_beams: set[int] = set()
    for beam in beams:
        if grid[(beam, y)] == '^':
            new_beams.add(beam - 1)
            new_beams.add(beam + 1)
            splits += 1
        else:
            new_beams.add(beam)
    beams = new_beams
print(splits)
