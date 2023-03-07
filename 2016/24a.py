#!/usr/bin/env python3
import sys
import itertools
from typing import Optional

filename = sys.argv[1]

Position = tuple[int, ...]
walls: set[Position] = set()
targets: dict[int, Position] = {}

with open(filename, 'r') as f:
    for y, line in enumerate(f):
        for x, letter in enumerate(line):
            if letter.isnumeric():
                targets[int(letter)] = (x, y)
            elif letter == '#':
                walls.add((x, y))

State = tuple[Position, int]
directions = ( (0, 1), (1, 0), (0, -1), (-1, 0))

# stolen from day 13
def find_distance(start: Position, destination: Position) -> int:
    seen: set[Position] = set()
    frontier: set[State] = { (start, 0) }
    distance = 0
    seen.add(start)

    while True:
        next_frontier: set[State] = set()
        for this_state in frontier:
            position, _ = this_state
            for dir in directions:
                new_position = tuple([c + d for c, d in zip(position, dir)])
                if new_position == destination:
                    return distance + 1
                if new_position not in seen and new_position not in walls:
                    seen.add(new_position)
                    next_frontier.add( (new_position, distance + 1) )
        distance += 1
        frontier = next_frontier
    raise ValueError(f"no path found from {start} to {destination}")

distances: dict[tuple[int, int], int] = {}
for i in targets.keys():
    for j in targets.keys():
        if i != j and (i, j) not in distances:
            distance = find_distance(targets[i], targets[j])
            distances[(i, j)] = distance
            distances[(j, i)] = distance

# print(distances)

best_distance: Optional[int] = None
best_path: list[int] = []

destinations = [k for k in targets.keys() if k != 0]
for sequence in itertools.permutations(destinations):
    path = [0] + list(sequence)
    # print (f"scoring {path}")
    total_distance = 0
    for i in range(len(path) - 1):
        next_step = distances[(path[i], path[i+1])]
        total_distance += next_step
        # print(f"{path[i]} -> {path[i+1]}: {next_step}")
    # print (f"total {total_distance}")
    if best_distance is None or total_distance < best_distance:
        best_distance = total_distance
        best_path = path

print(best_distance, best_path)
"""

destination: Position = tuple([int(arg) for arg in sys.argv[2:4]])
start: Position = (1, 1)


seen: set[Position] = set()

max_x = 0
max_y = 0
def print_maze() -> None:
    for row in range(max_y + 2):
        for column in range(max_x + 2):
            if (column, row) in seen:
                if is_open((column, row)):
                    print("O", end="")
                else:
                    raise ValueError(f"visited wall at {(column, row)}")
            elif is_open((column, row)):
                print(".", end="")
            else:
                print("#", end="")
        print()



print_maze()
"""
