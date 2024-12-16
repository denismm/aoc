#!/usr/bin/env python3
import sys
from positions import Position, Direction, add_direction, scale_direction
from functools import reduce

filename = sys.argv[1]
input_ints = [int(s) for s in sys.argv[2:5]]
(width, height, seconds) = input_ints
dimensions: Position = (width, height)

Robot = tuple[Position, Direction]
robots: list[Robot] = []
with open(filename, "r") as f:
    for line in f:
        line = line.replace(' ', ',')
        input_strs = line.split(',')
        inputs = [int(s.lstrip('pv=')) for s in input_strs]
        robots.append( ( (inputs[0], inputs[1]), (inputs[2], inputs[3])))

# n steps
for i, robot in enumerate(robots):
    new_raw_pos = add_direction(robot[0], scale_direction(robot[1], seconds))
    new_mod_pos = tuple([new_raw_pos[c] % dimensions[c] for c in (0, 1)])
    robots[i] = (new_mod_pos, robot[1])

quadrants: list[int] = [0, 0, 0, 0]
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
    quadrants[y * 2 + x] += 1

score = reduce(lambda x, y: x * y, quadrants)
print(score)
