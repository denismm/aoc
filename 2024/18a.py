#!/usr/bin/env python3
import sys
from positions import (
    Position,
    add_direction,
    cardinal_directions,
    print_set_grid,
)

filename: str = sys.argv[1]
grid_size: int = int(sys.argv[2])
falls: int = int(sys.argv[3])

obstacles: list[Position] = []
with open(filename, "r") as f:
    for line in f:
        obstacles.append(tuple([int(s) for s in line.split(',')]))

start: Position = (0, 0)
end: Position = (grid_size - 1, grid_size - 1)
walls: set[Position] = set(obstacles[:falls])

# print(print_set_grid(grid_size, grid_size, walls))

# Dijkstra
seen: set[Position] = set()
frontier: set[Position] = {start}
steps: int = 0

while frontier:
    steps += 1
    new_frontier: set[Position] = set()
    for location in frontier:
        for direction in cardinal_directions:
            step = add_direction(location, direction)
            if step in seen or step in walls:
                continue
            if not (0 <= step[0] < grid_size):
                continue
            if not (0 <= step[1] < grid_size):
                continue
            if step == end:
                print(steps)
                exit(0)
            seen.add(step)
            new_frontier.add(step)
    frontier = new_frontier
