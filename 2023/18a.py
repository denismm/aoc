#!/usr/bin/env python3
import sys
from positions import Position, Direction, add_direction, direction_for_udlr, cardinal_directions
from typing import NamedTuple
from collections import deque

filename = sys.argv[1]

Grid = dict[Position, str]
grid: Grid = {}

Instruction = NamedTuple('Instruction', [('dir', Direction), ('dist', int), ('color', str)])
plan: list[Instruction] = []

with open(filename, "r") as f:
    for line in f:
        dir_s, dist_s, color_s = line.split()
        instruction = Instruction(direction_for_udlr[dir_s], int(dist_s), color_s.strip('()'))
        plan.append(instruction)

cursor: Position = (0, 0)

grid[cursor] = '#'
for instruction in plan:
    for _ in range(instruction.dist):
        cursor = add_direction(cursor, instruction.dir)
        grid[cursor] = '#'

farthest = max([max([abs(c) for c in pos]) for pos in grid]) + 1

if False:
    for j in range(-farthest, farthest):
        for i in range(-farthest, farthest):
            print(grid.get((i, j), ' '), end="")
        print()

# fill outside
outside: set[Position] = set()
queue: deque[Position] = deque()
queue.append((farthest, farthest))
while queue:
    pos = queue.popleft()
    if pos in outside:
        continue
    outside.add(pos)
    for dir in cardinal_directions:
        next_pos = add_direction(pos, dir)
        if next_pos in outside or next_pos in grid:
            continue
        if max([abs(c) for c in next_pos]) > farthest:
            continue
        queue.append(next_pos)
outside_size = (farthest * 2 + 1) ** 2
print(outside_size - len(outside))

