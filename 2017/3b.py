#!/usr/bin/env python3
import sys
from positions import Position, add_direction, cardinal_directions

limit = int(sys.argv[1])
Grid = dict[Position, int]
grid: Grid = {(0, 0): 1}
neighbors = [ (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy ]

location: Position = (0, 0)
direction_index = 0

while grid[location] < limit:
    # take a step
    location = add_direction(location, cardinal_directions[direction_index])
    if location in grid:
        raise ValueError(f"retracing steps at {location}")
    # fill grid
    value = 0
    for dn in neighbors:
        n = add_direction(location, dn)
        value += grid.get(n, 0)
    grid[location] = value
    # print (f"setting {location} to {value}")
    # decide on next step
    if direction_index == 0:
        if location[0] - 1 == abs(location[1]):
            direction_index = 1
            # print(f"0-turning to {direction_index} at {location}")
    elif abs(location[0]) == abs(location[1]):
        direction_index += 1
        direction_index %= 4
        # print(f"turning to {direction_index} at {location}")
print(f"at {location} value is {grid[location]}")
