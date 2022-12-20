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
                if value & 2 ** i:
                    open = not open
        maze_cache[position] = open
    return maze_cache[position]



seen: set[Position] = set()

def print_maze() -> None:
    for row in range(10):
        for column in range(10):
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

queue: collections.deque[State] = collections.deque()
queue.append( (start, 0) )
seen.add(start)

current_dist = 0
while len(queue):
    this_state = queue.popleft()
    position, distance = this_state
    if distance > current_dist:
        current_dist = distance
        print(len(seen), this_state)
    if position == destination:
        final_distance = distance
        break
    for dir in directions:
        new_position = tuple([c + d for c, d in zip(position, dir)])
        if new_position not in seen and is_open(new_position):
            seen.add(new_position)
            queue.append( (new_position, distance + 1) )

print(final_distance)
