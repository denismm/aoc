#!/usr/bin/env python3
import sys
from positions import Position, Direction, cardinal_directions, add_direction

# remember row 0 is on top

filename = sys.argv[1]

grid: dict[Position, str] = {}
start: Position = (-1, -1)

with open(filename, 'r') as f:
    for j, line in enumerate(f):
        for i, pipe in enumerate(line.rstrip()):
            grid[(i, j)] = pipe
            if j == 0 and pipe == '|':
                start = (i, j)

if start == (-1, -1):
    raise ValueError("no starting point")
location: Position = start
direction: Direction = (0, 1)
route: list[str] = []

while True:
    # deal with current location
    current_pipe = grid.get(location, ' ')
    if current_pipe == ' ':
        break
    elif current_pipe.isalpha():
        route.append(current_pipe)
    elif current_pipe == '+':
        dir_i = cardinal_directions.index(direction)
        possible_turns = [cardinal_directions[(dir_i + offset) % 4] for offset in (-1, 1)]
        new_direction: Direction = (0, 0)
        for turn in possible_turns:
            next_step = add_direction(location, turn)
            if grid.get(next_step, ' ') != ' ':
                new_direction = turn
                break
        if new_direction == (0, 0):
            raise ValueError(f"no exit from junction at {location}")
        direction = new_direction
    elif current_pipe in ('-|'):
        pass
    else:
        raise ValueError(f"unexpected pipe {current_pipe}")
    # take step
    location = add_direction(location, direction)

print("".join(route))
