#!/usr/bin/env python3
import sys
from positions import Position, add_direction, cardinal_directions

filename = sys.argv[1]
steps = int(sys.argv[2])

Grid = set[Position]
walls: Grid = set()
start_position: Position = (-1, -1)

with open(filename, "r") as f:
    for j, line in enumerate(f):
        line = line.rstrip()
        width = len(line)
        for i, char in enumerate(line.rstrip()):
            if char == '#':
                walls.add((i, j))
            elif char == 'S':
                start_position = (i, j)
height = j + 1
grid: Grid = { (i, j) for i in range(width) for j in range(height) }

if start_position == (-1, -1):
    raise ValueError("no start position!")

reachable: dict[int, set[Position]] = {0: {start_position}}

for i in range(1, steps + 1):
    last_steps = reachable[i - 1]
    next_steps = set(add_direction(last, dir) for last in last_steps for dir in cardinal_directions)
    next_steps -= walls
    next_steps &= grid
    reachable[i] = next_steps
print(len(reachable[steps]))
