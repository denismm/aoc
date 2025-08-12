#!/usr/bin/env python3
import sys
from positions import StrGrid, read_char_grid, zeta_directions, Position, add_direction, print_char_grid
from collections import Counter

YARD = "#"
TREE = "|"
OPEN = "."

ROUNDS = 10

filename = sys.argv[1]

grid: StrGrid = {}
w: int = 0
h: int = 0

with open(filename, 'r') as f:
    w, h, grid = read_char_grid(f, skip_dots=False)

# print(print_char_grid(w, h, grid))

for i in range(ROUNDS):
    new_grid: StrGrid = {}
    for x in range(w):
        for y in range(h):
            position: Position = (x, y)
            content: str = grid[position]
            neighbors: Counter[str] = Counter()
            for d in zeta_directions:
                n: Position = add_direction(position, d)
                n_content = grid.get(n, OPEN)
                neighbors[n_content] += 1
            next_content = content
            if content == OPEN:
                if neighbors[TREE] >= 3:
                    next_content = TREE
            elif content == TREE:
                if neighbors[YARD] >= 3:
                    next_content = YARD
            elif content == YARD:
                if neighbors[YARD] == 0 or neighbors[TREE] == 0:
                    next_content = OPEN
            new_grid[position] = next_content
    grid = new_grid

population: Counter[str] = Counter()

for v in grid.values():
    population[v] += 1

print(population[YARD] * population[TREE])
