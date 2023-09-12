#!/usr/bin/env python3
import sys
from positions import Position, add_direction, cardinal_directions, direction_symbols

filename = sys.argv[1]
moves_to_simulate = int(sys.argv[2])

grid: set[Position] = set()
height = 0
width = 0
with open(filename, 'r') as f:
    for j, line in enumerate(f):
        for i, character in enumerate(line.rstrip()):
            if character == '#':
                grid.add( (i, j) )
        if width == 0:
            width = len(line.rstrip())
        height += 1

carrier_pos: Position = ((width - 1) // 2, (height - 1) // 2)
carrier_dir = 3
infections = 0

for move_count in range(moves_to_simulate):
    if carrier_pos in grid:
        carrier_dir += 1
        grid.remove(carrier_pos)
    else:
        carrier_dir -= 1
        grid.add(carrier_pos)
        infections += 1

    carrier_dir %= 4

    carrier_pos = add_direction(carrier_pos, cardinal_directions[carrier_dir])

x_start = min([p[0] for p in grid])
y_start = min([p[1] for p in grid])
x_end = max([p[0] for p in grid])
y_end = max([p[1] for p in grid])

for j in range(y_start, y_end + 1):
    line_output = ""
    for i in range(x_start, x_end + 1):
        if (i, j) == carrier_pos:
            line_output += direction_symbols[carrier_dir]
        elif (i, j) in grid:
            line_output += "#"
        else:
            line_output += "."
    print(line_output)

print(infections)
