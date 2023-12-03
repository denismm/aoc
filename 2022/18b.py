#!/usr/bin/env python3
import sys

Position = tuple[int, ...]
filename = sys.argv[1]
cubes: dict[Position, str] = {}
OUTSIDE = 'o'
LAVA = '#'
INSIDE = '.'

with open(filename, "r") as f:
    for line in f:
        coords: list[int] = [int(x) for x in line.rstrip().split(',')]
        cubes[tuple(coords)] = LAVA

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

def add_positions(a: Position, b: Position) -> Position:
    return tuple([ax + bx for ax, bx in zip(a, b)])

# fill box
for x in range(cube_min[0], cube_max[0] + 1):
    for y in range(cube_min[1], cube_max[1] + 1):
        for z in range(cube_min[2], cube_max[2] + 1):
            position = (x, y, z)
            if position in cubes:
                # already filled
                continue
            position_stack: list[Position] = [position]
            candidates: set[Position] = set()
            seen: set[Position] = {position}
            escape = False
            while (position_stack):
                next_position = position_stack.pop()
                candidates.add(next_position)
                for direction in directions:
                    neighbor = add_positions(next_position, direction)
                    if neighbor in seen:
                        continue
                    in_box = True
                    for c in range(3):
                        if not cube_min[c] <= neighbor[c] <= cube_max[c]:
                            in_box = False
                    if not in_box:
                        escape = True
                    else:
                        seen.add(neighbor)
                        if neighbor not in cubes:
                            position_stack.append(neighbor)
            if escape:
                fill = OUTSIDE
            else:
                fill = INSIDE
            for candidate in candidates:
                cubes[candidate] = fill

faces: int = 0
for lava_cube in [k for k, v in cubes.items() if v == LAVA]:
    for direction in directions:
        neighbor = add_positions(lava_cube, direction)
        if cubes.get(neighbor, OUTSIDE) == OUTSIDE:
            faces += 1
print(f"outside faces: {faces}")
