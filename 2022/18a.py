#!/usr/bin/env python3
import sys

Position = tuple[int, ...]
filename = sys.argv[1]
with open(filename, "r") as f:
    cubes: set[Position] = set()
    for line in f:
        coords: list[int] = [int(x) for x in line.rstrip().split(',')]
        cubes.add(tuple(coords))

cube_max: list[int] = []
cube_min: list[int] = []
directions: list[Position] = []
for c in range(3):
    cube_max.append(max([cube[c] for cube in cubes]))
    cube_min.append(min([cube[c] for cube in cubes]))
    temp_direction = [0, 0, 0]
    for a in [-1, 1]:
        temp_direction[c] = a
        directions.append(tuple(temp_direction))
print(cube_max, cube_min)

faces: int = 0
for cube in cubes:
    for direction in directions:
        neighbor = tuple([x + d for x, d in zip(cube, direction)])
        if neighbor not in cubes:
            faces += 1
print(f"all faces: {faces}")
