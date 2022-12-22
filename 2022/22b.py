#!/usr/bin/env python3
import sys
import re
import math
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
                    input_position = (x, y)
                    max_x = max(x, max_x)
                    max_y = max(y, max_y)
                    grid[input_position] = character
                    if start_position is None:
                        start_position = input_position

directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
direction_symbols = ">v<^"

dir = 0
if start_position is None:
    raise ValueError("no grid!")
position = start_position

# figure out cube
edge_float = math.sqrt(len(grid) / 6)
edge = int(edge_float)
if edge != edge_float:
    raise ValueError(f"bad cube! edge of {edge_float}")
print(f"edge is {edge}")
cube_face_grid = set([
    tuple([px // edge for px in p])
    for p in grid.keys()
    if p[0] % edge == 0 and p[1] % edge == 0
])
if cube_face_grid == {(0, 1), (2, 1), (1, 1), (2, 0), (2, 2), (3, 2)}:
    # example
    face_pairs = [
        ( ((2, 0), '^'), ((0, 1), '^') ),
        ( ((2, 0), '>'), ((3, 2), '>') ),
        ( ((2, 1), '>'), ((3, 2), '^') ),
        ( ((0, 1), '<'), ((3, 2), 'v') ),
        ( ((0, 1), 'v'), ((2, 2), 'v') ),
        ( ((1, 1), 'v'), ((2, 2), '<') ),
        ( ((1, 1), '^'), ((2, 0), '<') ),
    ]
elif cube_face_grid == {(1, 2), (1, 1), (0, 3), (2, 0), (0, 2), (1, 0)}:
    # input
    face_pairs = [
        ( ((2, 0), 'v'), ((1, 1), '>') ),
        ( ((2, 0), '>'), ((1, 2), '>') ),
        ( ((2, 0), '^'), ((0, 3), 'v') ),
        ( ((1, 0), '^'), ((0, 3), '<') ),
        ( ((1, 0), '<'), ((0, 2), '<') ),
        ( ((1, 1), '<'), ((0, 2), '^') ),
        ( ((1, 2), 'v'), ((0, 3), '>') ),
    ]
else:
    raise ValueError(f"unknown grid {cube_face_grid}")

edge_match: dict[tuple[Position, int], tuple[Position, int]] = {}
for pair in face_pairs:
    faces = [side[0] for side in pair]
    dirs = [direction_symbols.index(side[1]) for side in pair]
    edge_match[(faces[0], dirs[0])] = (faces[1], dirs[1])
    edge_match[(faces[1], dirs[1])] = (faces[0], dirs[0])

# clockwise edges
edge_for_direction = [
    [(edge - 1, y) for y in range(edge)],               # >
    [(x, edge - 1) for x in reversed(range(edge))],      # v
    [(0, y) for y in reversed(range(edge))],            # <
    [(x, 0) for x in range(edge)],                      # ^
]

def add_positions(position: Position, direction: Position) -> Position:
    return tuple([p + d for p, d in zip(position, direction)])

def transform_step(position: Position, dir: int) -> tuple[Position, int]:
    face = tuple([x // edge for x in position])
    new_face, new_edge = edge_match[(face, dir)]
    offset_position = tuple([x % edge for x in position])
    which_position = edge_for_direction[dir].index(offset_position)     # type: ignore[arg-type]
    new_offset = edge_for_direction[new_edge][(edge - 1) - which_position]
    new_dir = (new_edge + 2) % 4
    new_position = add_positions(new_offset, tuple([x * edge for x in new_face]))
    return new_position, new_dir

def advance(position: Position, amount: int, dir: int) -> tuple[Position, int]:
    grid[position] = direction_symbols[dir]
    for _ in range(amount):
        new_dir = dir
        direction = directions[new_dir]
        new_position = add_positions(position, direction)
        if new_position not in grid:
            new_position, new_dir = transform_step(position, dir)
        if grid[new_position] == '#':
            break
        else:
            grid[position] = direction_symbols[dir]
            position = new_position
            dir = new_dir
    return position, dir


for step in path:
    if isinstance(step, str):
        if step == 'L':
            dir = (dir - 1) % 4
        else:
            dir = (dir + 1) % 4
    else:
        position, dir = advance(position, step, dir)
output_position = add_positions(position, (1, 1))
print(output_position[1] * 1000 + output_position[0] * 4 + dir)

def print_maze() -> None:
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(grid.get((x, y), ' '), end="")
        print()
