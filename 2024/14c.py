#!/usr/bin/env python3
# analysis script for finding useful times

import sys
from positions import Position, Direction, add_direction, scale_direction
import png      # type: ignore
import os.path

filename = sys.argv[1]
input_ints = [int(s) for s in sys.argv[2:5]]
(width, height, last_second) = input_ints
dimensions: Position = (width, height)

Robot = tuple[Position, Direction]
base_robots: list[Robot] = []
with open(filename, "r") as f:
    for line in f:
        line = line.replace(' ', ',')
        input_strs = line.split(',')
        inputs = [int(s.lstrip('pv=')) for s in input_strs]
        base_robots.append( ( (inputs[0], inputs[1]), (inputs[2], inputs[3])))

for seconds in range(last_second+1):
    filename = f"14_robots/14.output.{seconds}.png"
    if os.path.exists(filename):
        continue
    robots = [robot for robot in base_robots]
    # n steps
    for i, robot in enumerate(robots):
        new_raw_pos = add_direction(robot[0], scale_direction(robot[1], seconds))
        new_mod_pos = tuple([new_raw_pos[c] % dimensions[c] for c in (0, 1)])
        robots[i] = (new_mod_pos, robot[1])

    for robot in robots:
        pos = robot[0]
        if pos[0] < dimensions[0] // 2:
            x = 0
        elif pos[0] > dimensions[0] // 2:
            x = 1
        else:
            continue
        if pos[1] < dimensions[1] // 2:
            y = 0
        elif pos[1] > dimensions[1] // 2:
            y = 1
        else:
            continue

    output_set: set[Position] = { r[0] for r in robots }
    output_array: list[list[int]] = []
    for y in range(height):
        row: list[int] = []
        for x in range(width):
            pos = (x, y)
            if pos in output_set:
                row.append(1)
            else:
                row.append(0)
        output_array.append(row)
    image = png.from_array(output_array, "L;1")
    image.save(f"14_robots/14.output.{seconds}.png")
