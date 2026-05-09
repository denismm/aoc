#!/usr/bin/env python3
import sys
from positions import Position, manhattan
from dataclasses import dataclass

filename = sys.argv[1]

# order means we can sort to get the best radius
@dataclass(order=True)
class Nanobot:
    radius: int
    pos: Position

nanobots: list[Nanobot] = []

with open(filename, 'r') as f:
    for line in f:
        pos_s, rad_s = line.split()
        pos_s = pos_s.strip('pos=<>,')
        pos = tuple([int(s) for s in pos_s.split(',')])
        rad = int(rad_s.split('=')[-1])
        nanobots.append(Nanobot(rad, pos))

nanobots.sort()
strongest: Nanobot = nanobots.pop()
near: int = 1   # including itself
for nb in nanobots:
    if manhattan(strongest.pos, nb.pos) <= strongest.radius:
        near += 1
print(near)
