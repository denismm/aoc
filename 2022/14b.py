#!/usr/bin/env python3
import sys

Position = tuple[int, ...]

def print_grid(grid: list[list[str]]) -> None:
    for i in range(len(grid[0])):
        print(''.join([rank[i] for rank in grid]))

filename = sys.argv[1]
with open(filename, "r") as f:
    rock_lines: list[list[Position]] = []
    for line in f:
        rock_line = []
        for entry in line.split():
            if entry == '->':
                continue
            coords = [int(c) for c in entry.split(",")]
            rock_line.append(tuple(coords))
        rock_lines.append(rock_line)
max_extents = [ max([max([position[c] for position in rock_line])
        for rock_line in rock_lines]) for c in range(2) ]
min_extents = [ min([min([position[c] for position in rock_line])
        for rock_line in rock_lines]) for c in range(2) ]

min_extents[1] = 0
max_extents[1] += 1
min_extents[0] -= 1
max_extents[0] += 1
width = 1 + max_extents[0] - min_extents[0]
depth = 1 + max_extents[1] - min_extents[1]
grid: list[list[str]] = [ ['.'] * depth for _ in range(width)]

def transform_point(point: Position) -> Position:
    return tuple( [ a - b for a, b in zip(point, min_extents)] )

def place_rock(point: Position) -> None:
    grid[point[0]][point[1]] = '#'
def place_sand(point: Position) -> None:
    grid[point[0]][point[1]] = 'o'

for rock_line in rock_lines:
    transformed_line = [transform_point(point) for point in rock_line]
    current_point = transformed_line[0]
    place_rock(current_point)
    for next_point in transformed_line[1:]:
        if next_point[0] == current_point[0]:
            distance = next_point[1] - current_point[1]
            step = distance // abs(distance)
            for i in range(current_point[1] + step, next_point[1] + step, step):
                new_point = (current_point[0], i)
                place_rock(new_point)
        else:
            distance = next_point[0] - current_point[0]
            step = distance // abs(distance)
            for i in range(current_point[0] + step, next_point[0] + step, step):
                new_point = (i, current_point[1])
                place_rock(new_point)
        current_point = next_point

print_grid(grid)

source = transform_point( (500, 0) )

class Escape(Exception):
    pass

piles: list[int] = [0, 0]

def handle_pile(pile_index: int, y: int) -> str:
    if depth - piles[pile_index] < y:
        return 'o'
    else:
        piles[pile_index] += 1
        raise Escape()

def get_grid(position: Position) -> str:
    x, y = position
    if y >= depth:
        return '#'
    if x < 0:
        return handle_pile(0, y)
    if x >= width:
        return handle_pile(1, y)
    return grid[x][y]

def drop_sand(position: Position) -> None:
    x, y = position
    contents = get_grid((x, y + 1))
    while contents == '.':
        y += 1
        contents = get_grid((x, y + 1))
    for side in [-1, 1]:
        side_fall = get_grid((x + side, y + 1))
        if side_fall == '.':
            return drop_sand((x + side, y + 1))
    place_sand((x, y))
    return

dropped_sand = 0
while get_grid(source) == '.':
    try:
        drop_sand(source)
        dropped_sand += 1
    except Escape:
        pass

print_grid(grid)
for pile in piles:
    dropped_sand += (pile * (pile - 1)) // 2
print(dropped_sand)
print(piles)
