#!/usr/bin/env python3
import sys
from positions import read_char_grid, Position, add_direction, cardinal_directions

filename = sys.argv[1]

with open(filename, "r") as f:
    _, _, grid = read_char_grid(f)

total_price = 0

while grid:
    # find a point
    seed = next(iter(grid.keys()))
    plant = grid[seed]
    region: set[Position] = {seed}

    # spread out to find region and boundaries

    queue: list[Position] = [seed]

    # add to this whenever a spread can't expand
    # we don't care about anything else about the border
    perimeter: int = 0

    while queue:
        current = queue.pop(0)
        for dir in cardinal_directions:
            step = add_direction(current, dir)
            if step in region:
                continue
            if grid.get(step) == plant:
                region.add(step)
                queue.append(step)
                continue
            # couldn't expand, must be a border
            perimeter += 1

    # score region
    total_price += perimeter * len(region)

    # remove region from the grid
    for location in region:
        del grid[location]

print(total_price)
