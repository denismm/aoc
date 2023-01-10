#!/usr/bin/env python3
import sys
import collections
import hashlib

seed: str = sys.argv[1]

Position = tuple[int, ...]
start: Position = (0, 0)
destination: Position = (3, 3)
directions: dict[str, Position] = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }

dir_list = "UDLR"

def add_pos(position: Position, dir: Position) -> Position:
    return tuple([p + d for p, d in zip(position, dir)])

State = tuple[Position, str]    # second is path to here

queue: collections.deque[State] = collections.deque()
queue.append( (start, "") )
current_distance = -1

while len(queue):
    this_state = queue.popleft()
    position, path = this_state
    if len(path) > current_distance:
        current_distance = len(path)
        if current_distance % 10 == 0:
            print(len(queue), len(path))
    hash_input = seed + path
    hash = hashlib.md5(hash_input.encode()).hexdigest()
    for (dir, door) in zip(dir_list, hash[:4]):
        if door in 'bcdef':
            new_position = add_pos(position, directions[dir])
            new_path = path + dir
            if new_position == destination:
                print(">>>", len(new_path))
            elif 0 <= new_position[0] < 4 and 0 <= new_position[1] < 4:
                queue.append( (new_position, new_path))
