#!/usr/bin/env python3
import sys
from positions import Position, Direction, add_direction, direction_for_udlr, scale_direction
from typing import NamedTuple, Optional

filename = sys.argv[1]

Instruction = NamedTuple('Instruction', [('dir', Direction), ('dist', int), ('color', str)])
plan: list[Instruction] = []

debug = False
with open(filename, "r") as f:
    for line in f:
        if debug:
            dir_s, dist_s, color_s = line.split()
            instruction = Instruction(direction_for_udlr[dir_s], int(dist_s), color_s.strip('()'))
            plan.append(instruction)

        else:
            c1, c2, color_s = line.split()
            color_data = color_s.strip('()#')
            dir_s = "RDLU"[int(color_data[-1])]
            distance = int(color_data[:-1], base=16)
            instruction = Instruction(direction_for_udlr[dir_s], distance, c1 + c2)
            plan.append(instruction)

cursor: Position = (0, 0)

Corner = NamedTuple('Corner', [('entry', Direction), ('exit', Direction)])

first_direction: Direction = (0, 0)

last_direction: Direction = (0, 0)

grid: dict[Position, Corner] = {}

for instruction in plan:
    new_direction = instruction.dir
    if first_direction == (0, 0):
        first_direction = instruction.dir
    else:
        grid[cursor] = Corner(last_direction, new_direction)
    step = scale_direction(instruction.dir, instruction.dist)
    cursor = add_direction(cursor, step)
    last_direction = new_direction

if cursor != (0, 0):
    raise ValueError(f"didn't close loop at {cursor}")

grid[cursor] = Corner(last_direction, first_direction)

y_values = sorted(set([position[1] for position in grid]))

total_area = 0

# convenience names
DOWN = (0, 1)
UP = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

v_lines: list[int] = []
last_y: Optional[int] = None

for y in y_values:
    if last_y is not None:
        # from the last row to this one - include this row, we'll fix it
        y_run = y - last_y
        for i in range(0, len(v_lines), 2):
            start_x, end_x = v_lines[i:i+2]
            addition = (1 + end_x - start_x) * y_run
            total_area += addition
    row_points = sorted([position for position in grid if position[1] == y])
    if len(row_points) % 2 != 0:
        raise ValueError(f"unmatched points in row {y}")
    for i in range(0, len(row_points), 2):
        start_point, end_point = row_points[i:i+2]
        start_corner = grid[start_point]
        end_corner = grid[end_point]

        # assuming that track is clockwise
        if start_corner.exit == end_corner.entry == RIGHT:
            addition = end_point[0] - start_point[0]
            # in two cases we need one more or less point on this line
            if start_corner.entry != end_corner.exit:
                if start_corner.entry == UP:
                    addition += 1
                else:
                    addition -= 1
            total_area += addition
        elif start_corner.entry == end_corner.exit == LEFT:
            # nothing, just making sure things line up
            pass
        else:
            raise ValueError(f"corner mismatch: {start_point} {start_corner} {end_point} {end_corner}")

    # remove and add points
    for point in row_points:
        corner = grid[point]
        if corner.entry == DOWN or corner.exit == UP:
            v_lines.remove(point[0])
        elif corner.entry == UP or corner.exit == DOWN:
            if point[0] in v_lines:
                raise ValueError(f"intersection at {point}")
            v_lines.append(point[0])
        else:
            raise ValueError(corner)

    v_lines.sort()
    last_y = y

print(total_area)
