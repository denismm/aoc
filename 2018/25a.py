#!/usr/bin/env python3
import sys
from positions import Position, manhattan

filename = sys.argv[1]

points: list[Position] = []

with open(filename, 'r') as f:
    for line in f:
        pos = tuple([int(s) for s in line.split(',')])
        points.append(pos)

constellations: dict[int, list[Position]] = {}
next_const = 0

for point in points:
    near_constellations: list[int] = []
    for c_number, c_points in constellations.items():
        for c_point in c_points:
            if manhattan(point, c_point) <= 3:
                near_constellations.append(c_number)
                break
    if len(near_constellations) == 0:
        constellations[next_const] = [point]
        next_const += 1
    else:
        main_const = near_constellations.pop()
        constellations[main_const].append(point)
        for other_const in near_constellations:
            constellations[main_const] += constellations[other_const]
            del constellations[other_const]
print(len(constellations))
