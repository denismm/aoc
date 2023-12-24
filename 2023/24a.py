#!/usr/bin/env python3
import sys
from positions import Position, Direction
from typing import NamedTuple, Optional
from itertools import combinations

filename = sys.argv[1]
min_coord = int(sys.argv[2])
max_coord = int(sys.argv[3])

# store both y = mx + b form and x = nx + a form
Line = NamedTuple('Line', [('slope', float), ('intercept', float)])
Stone = NamedTuple('Stone', [
    ('pos', Position), ('dir', Direction),
    ('y_line', Optional[Line]),
    ('x_intercept', Optional[int]),
])
stones: list[Stone] = []

with open(filename, "r") as f:
    for line in f:
        pos_s, dir_s = line.split('@')
        pos = tuple(int(x) for x in pos_s.split(', '))[:2]
        dir = tuple(int(x) for x in dir_s.split(', '))[:2]
        y_line: Optional[Line]
        x_line: Optional[Line]
        if dir[0] != 0:
            # calculate y-line
            slope = dir[1] / dir[0]
            intercept = pos[1] - slope * pos[0]
            y_line = Line(slope, intercept)
            x_intercept = None
        else:
            y_line = None
            x_intercept = pos[0]
        stones.append(Stone(pos, dir, y_line, x_intercept))

# collision point for every pair
intercepts = 0
for pair in combinations(stones, 2):
    intersection: tuple[float, ...]
    if pair[0].y_line is None:
        pair = tuple(reversed(pair))    # type: ignore [assignment]
    # now either first stone has a y-line or neither does
    y_lines = [stone.y_line for stone in pair]
    if y_lines[0] is None:
        # neither has a y-line
        raise ValueError(f"two vertical lines: {pair}")
    elif y_lines[1] is None:
        # horizontal and vertical
        intersection = (y_lines[0].intercept, pair[1].x_intercept)      # type: ignore [assignment]
    elif y_lines[0].slope == y_lines[1].slope:
        # parallel lines
        if y_lines[0].intercept == y_lines[1].intercept:
            raise ValueError(f"congruent lines: {pair}")
        continue
    else:
        intersection_x = (y_lines[1].intercept - y_lines[0].intercept) / (y_lines[0].slope - y_lines[1].slope)
        intersection_y = y_lines[0].slope * intersection_x + y_lines[0].intercept
        intersection = (intersection_x, intersection_y)

    # we have intersection, is it in range?
    intersection_ok = True
    for c in range(2):
        if not min_coord <= intersection[c] <= max_coord:
            intersection_ok = False
    if intersection_ok:
        # is it in the future for both stones?
        for stone in pair:
            # pick a non-zero direction
            c = 0
            if stone.dir[0] == 0:
                c = 1
            intersection_time = (intersection[c] - stone.pos[c]) / stone.dir[c]
            if intersection_time < 0:
                intersection_ok = False
    if intersection_ok:
        intercepts += 1


print(intercepts)
