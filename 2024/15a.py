#!/usr/bin/env python3
import sys
from positions import Position, Direction, add_direction, read_char_grid, direction_for_symbol

filename = sys.argv[1]

instructions: str = ""
with open(filename, "r") as f:
    _, _, grid = read_char_grid(f)
    for line in f:
        instructions += line.rstrip()

robot: Position = [k for k, v in grid.items() if v == '@'][0]
del grid[robot]

for dir in instructions:
    direction: Direction = direction_for_symbol[dir]

    # try to move
    step = add_direction(robot, direction)
    if grid.get(step) == '#':
        continue
    if grid.get(step) == 'O':
        bump = step
        while grid.get(bump) == 'O':
            bump = add_direction(bump, direction)
        if grid.get(bump) == '#':
            continue
        grid[bump] = 'O'
        del grid[step]
    robot = step

gps_total = 0
for k, v in grid.items():
    if v == 'O':
        gps_total += (100 * k[1] + k[0])
print(gps_total)
