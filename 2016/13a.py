#!/usr/bin/env python3
import sys
import math
import collections

Position = tuple[int, ...]
favorite = int(sys.argv[1])
destination: Position = tuple([int(arg) for arg in sys.argv[2:4]])
start: Position = (1, 1)

maze_cache: dict[Position, bool] = {}

def is_open(position: Position) -> bool:
    if position not in maze_cache:
        (x, y) = position
        open = True
        if x < 0 or y < 0:
            open = False
        else:
            value = x*x + 3*x + 2*x*y + y + y*y + favorite
            # print(value)
            top_bit = math.ceil(math.log(value, 2)) + 1
            for i in range(top_bit):
                if value & (2 ** i):
                    open = not open
        maze_cache[position] = open
    return maze_cache[position]



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

State = tuple[Position, int]

directions = ( (0, 1), (1, 0), (0, -1), (-1, 0))

frontier: set[State] = { (start, 0) }
distance = 0
seen.add(start)

while distance <= 50:
    print(f"frontier {distance}: {len(frontier)} locations, {len(seen)} total")
    next_frontier: set[State] = set()
    for this_state in frontier:
        position, _ = this_state
        max_x = max(position[0], max_x)
        max_y = max(position[1], max_y)
        for dir in directions:
            new_position = tuple([c + d for c, d in zip(position, dir)])
            if new_position not in seen and is_open(new_position):
                seen.add(new_position)
                next_frontier.add( (new_position, distance + 1) )
    distance += 1
    frontier = next_frontier
print_maze()
