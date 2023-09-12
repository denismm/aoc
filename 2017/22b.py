#!/usr/bin/env python3
import sys
from positions import Position, add_direction, cardinal_directions, direction_symbols

filename = sys.argv[1]
moves_to_simulate = int(sys.argv[2])

grid: dict[Position, int] = {}
# 0 1 2 3 = C W I F
height = 0
width = 0
with open(filename, 'r') as f:
    for j, line in enumerate(f):
        for i, character in enumerate(line.rstrip()):
            if character == '#':
                grid[(i, j)] = 2
        if width == 0:
            width = len(line.rstrip())
        height += 1

carrier_pos: Position = ((width - 1) // 2, (height - 1) // 2)
carrier_dir = 3
infections = 0

direction_for_state = (-1, 0, 1, 2)

for move_count in range(moves_to_simulate):
    status = grid.get(carrier_pos, 0)
    carrier_dir += direction_for_state[status]
    carrier_dir %= 4
    status += 1
    status %= 4
    if status == 2:
        infections += 1
    grid[carrier_pos] = status

    carrier_pos = add_direction(carrier_pos, cardinal_directions[carrier_dir])

print(infections)

# exit(0)

x_start = min([p[0] for p in grid])
y_start = min([p[1] for p in grid])
x_end = max([p[0] for p in grid])
y_end = max([p[1] for p in grid])

char_for_status = ('.', 'W', '#', 'F')

for j in range(y_start, y_end + 1):
    line_output = ""
    for i in range(x_start, x_end + 1):
        if (i, j) == carrier_pos:
            line_output += direction_symbols[carrier_dir]
        else:
            line_output += char_for_status[grid.get((i, j), 0)]
    print(line_output)

