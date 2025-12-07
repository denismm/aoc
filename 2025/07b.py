#!/usr/bin/env python3

import sys
from positions import read_char_grid
from collections import Counter

filename = sys.argv[1]

with open(filename, 'r') as f:
    w, h, grid = read_char_grid(f, skip_dots=False)

beams: Counter[int] = Counter()
# find start
for x in range(w):
    if grid[(x, 0)] == 'S':
        beams[x] = 1
if len(beams) != 1:
    raise ValueError("not one beam")

for y in range(1, h):
    new_beams: Counter[int] = Counter()
    for beam, timelines in beams.items():
        if grid[(beam, y)] == '^':
            new_beams[beam - 1] += timelines
            new_beams[beam + 1] += timelines
        else:
            new_beams[beam] += timelines
    beams = new_beams
print(sum(beams.values()))
