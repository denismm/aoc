#!/usr/bin/env python3
import sys
from positions import read_char_grid, Position, add_direction, cardinal_directions, Direction
from collections import defaultdict

filename = sys.argv[1]

with open(filename, "r") as f:
    _, _, grid = read_char_grid(f)

total_price = 0
bulk_price = 0

while grid:
    # find a point
    seed = next(iter(grid.keys()))
    plant = grid[seed]
    region: set[Position] = {seed}

    # spread out to find region and boundaries

    queue: list[Position] = [seed]

    perimeter = 0
    borders_by_direction: dict[Direction, list[Position]] = defaultdict(list)

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
            borders_by_direction[dir].append(current)

    # find sides
    side_count = 0
    for dir, points in borders_by_direction.items():
        arranged_edges: dict[int, list[int]] = defaultdict(list)
        for point in points:
            if dir[0] == 0:     # NS: group by Y, sort by X
                arranged_edges[point[1]].append(point[0])
            else:               # EW: group by X, sort by Y
                arranged_edges[point[0]].append(point[1])
        # find runs within ranks
        for rank, files in arranged_edges.items():
            files = sorted(files)
            last_file = -100
            for x in files:
                if x != last_file + 1:
                    side_count += 1
                last_file = x
    # score region
    area = len(region)
    total_price += perimeter * area
    bulk_price += side_count * area

    # remove region from the grid
    for location in region:
        del grid[location]

print(total_price)
print(bulk_price)
