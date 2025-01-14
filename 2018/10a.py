#!/usr/bin/env python3
import sys
import re
from positions import Position, Direction, add_direction, scale_direction
from typing import Optional
import png      # type: ignore
import os.path

# pretending everything is robots because I copied this from 2024/14b

filename = sys.argv[1]
target = int(sys.argv[2])

Robot = tuple[Position, Direction]
robot_re = re.compile(r'position=<([^<>]+)> velocity=<([^<>]+)>')
base_robots: list[Robot] = []
with open(filename, "r") as f:
    for line in f:
        m = robot_re.match(line)
        if not m:
            raise ValueError(f"can't parse line {line}")
        inputs = [[int(ss) for ss in (s.split(','))] for s in m.groups()]
        base_robots.append((tuple(inputs[0]), tuple(inputs[1])))

min_dim: Optional[int] = None
seconds = 0
best_seconds = 0
checkpoint: int = 1
while True:
    seconds += 1
    maxes: list[int] = []
    mins: list[int] = []
    filename = f"10_messages/10.output.{seconds}.png"
    if os.path.exists(filename):
        continue
    robots = [robot for robot in base_robots]
    # n steps
    for i, robot in enumerate(robots):
        new_pos = add_direction(robot[0], scale_direction(robot[1], seconds))
        if len(maxes):
            for c in (0, 1):
                if new_pos[c] < mins[c]:
                    mins[c] = new_pos[c]
                elif new_pos[c] > maxes[c]:
                    maxes[c] = new_pos[c]
        else:
            maxes = list(new_pos)
            mins = list(new_pos)
        robots[i] = (new_pos, robot[1])

    width = 1 + maxes[0] - mins[0]
    height = 1 + maxes[1] - mins[1]
    if min_dim is None:
        min_dim = height
    if height < min_dim:
        min_dim = height
        best_seconds = seconds
    if width < min_dim:
        min_dim = width
        best_seconds = seconds
    if seconds == checkpoint:
        print(seconds, height, width)
        checkpoint *= 2
    if height > 2 * min_dim and width > 2 * min_dim:
        break
    if seconds == target:
        offset: Direction = scale_direction(tuple(mins), -1)
        output_set: set[Position] = { add_direction(r[0], offset) for r in robots }
        output_array: list[list[int]] = []
        for y in range(height):
            row: list[int] = []
            for x in range(width):
                pos = (x, y)
                if pos in output_set:
                    row.append(0)
                else:
                    row.append(1)
            output_array.append(row)
        image = png.from_array(output_array, "L;1")
        image.save(filename)
        print("done!")
        exit(0)

print(best_seconds, min_dim)
