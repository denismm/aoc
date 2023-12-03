#!/usr/bin/env python3
import sys
import re
from typing import Union, Optional

Position = tuple[int, ...]
grid: dict[Position, str] = {}
path: list[Union[str, int]] = []
step_re = re.compile(r'(\d+|[LR])')

filename = sys.argv[1]
start_position: Optional[Position] = None
max_x = 0
max_y = 0
with open(filename, "r") as f:
    for y, line in enumerate(f):
        if '0' <= line[0] <= '9':
            for step_match in step_re.finditer(line.rstrip()):
                step = step_match.group(1)
                if step in 'LR':
                    path.append(step)
                else:
                    path.append(int(step))
        else:
            for x, character in enumerate(line.rstrip()):
                if character != ' ':
                    input_position = (x + 1, y + 1)
                    max_x = max(x + 1, max_x)
                    max_y = max(y + 1, max_y)
                    grid[input_position] = character
                    if start_position is None:
                        start_position = input_position

directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
direction_symbols = ">v<^"

def add_direction(position: Position, dir: Position) -> Position:
    return tuple([p + d for p, d in zip(position, dir)])

def advance(position: Position, amount: int, direction: int) -> Position:
    dir = directions[direction]
    grid[position] = direction_symbols[direction]
    for _ in range(amount):
        new_position = add_direction(position, dir)
        if new_position not in grid:
            new_position = position
            backup_dir = directions[(direction + 2) % 4]
            backup_position = position
            while backup_position in grid:
                new_position = backup_position
                backup_position = add_direction(new_position, backup_dir)
        if grid[new_position] == '#':
            break
        else:
            grid[position] = direction_symbols[direction]
            position = new_position
    return position

direction = 0
if start_position is None:
    raise ValueError("no grid!")
position = start_position
for step in path:
    if isinstance(step, str):
        if step == 'L':
            direction = (direction - 1) % 4
        else:
            direction = (direction + 1) % 4
    else:
        position = advance(position, step, direction)
print(position[1] * 1000 + position[0] * 4 + direction)

def print_maze() -> None:
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(grid.get((x, y), ' '), end="")
        print()
