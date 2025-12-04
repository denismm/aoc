#!/usr/bin/env python3

import sys
from positions import Position, read_set_grid, SetGrid, add_direction, zeta_directions, print_set_grid

filename = sys.argv[1]

grid: SetGrid

with open(filename, 'r') as f:
    w, h, grid = read_set_grid(f, symbol="@")

p: Position
moved = -1
ever_moved = 0
round = 0
while moved != 0:
    movable_grid: SetGrid = set()
    for p in grid:
        neighbors = 0
        for dir in zeta_directions:
            if add_direction(p, dir) in grid:
                neighbors += 1
        if neighbors < 4:
            movable_grid.add(p)

    # print(print_set_grid(w, h, movable_grid))
    moved = len(movable_grid)
    if round == 0:
        print(moved)
    grid -= movable_grid
    ever_moved += moved
    round += 1
print(ever_moved)
