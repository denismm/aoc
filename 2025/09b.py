#!/usr/bin/env python3

import sys
from positions import Position
from itertools import combinations
from dataclasses import dataclass

filename = sys.argv[1]

tiles: list[Position] = []
# also find vertical lines
@dataclass(repr=True, order=True)
class VLine:
    x: int
    top: int
    bottom: int

with open(filename, 'r') as f:
    for line in f:
        points = [int(s) for s in line.rstrip().split(',')]
        tiles.append(tuple(points))

vlines: list[VLine] = []
relevant_y: list[int] = sorted([tile[1] for tile in tiles])
last_point = tiles[0]
for point in tiles[1:] + tiles[0:1]:
    if last_point[0] == point[0]:
        line_points = sorted([last_point, point])
        vlines.append(VLine(point[0], line_points[0][1], line_points[1][1]))
    last_point = point
# sort by x for convenience
vlines.sort()

# print(vlines)

big_area: int = 0

class Outside(Exception):
    pass

for source, target in combinations(tiles, 2):
    area = (abs(source[0] - target[0]) + 1) * (abs(source[1] - target[1]) + 1)
    if area > big_area:
        # print()
        # print(source, target, area)
        try:
            # check for inclusion
            box_y: list[int] = sorted([source[1], target[1]])
            box_x: list[int] = sorted([source[0], target[0]])
            ys_to_check: set[float] = set()
            # ignore any internal lines actually on the top or bottom edge
            ys_to_check.add(box_y[0] + 0.5)
            ys_to_check.add(box_y[1] - 0.5)
            for y in relevant_y:
                if y > box_y[0]:
                    if y >= box_y[1]:
                        break
                    else:
                        ys_to_check.add(y)
            # print(f"{box_x=} {box_y=}")
            # print(ys_to_check)
            # check line
            for line_y in ys_to_check:
                # print(f"checking {line_y=}")
                # green's members: green above? green below?
                green: list[bool] = [False, False]
                for vline in vlines:
                    # did we pass it?
                    if box_x[1] <= vline.x:
                        if True not in green:
                            # print(f"missed at {line_y=}")
                            raise Outside()
                        else:
                            break

                    if vline.top <= line_y <= vline.bottom:
                        if vline.x <= box_x[0]:
                            if vline.top != line_y:
                                green[0] = not green[0]
                            if vline.bottom != line_y:
                                green[1] = not green[1]
                            # print(f"{green=} at {vline}")
                        elif box_x[0] < vline.x < box_x[1]:
                            # internal transition
                            # print(f"internal at {vline}")
                            raise Outside()
                        # we don't need third possibility
                # print(f"ok at {line_y=}")
        except Outside:
            continue
        big_area = area

print(big_area)
