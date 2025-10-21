#!/usr/bin/env python3
import sys
from typing import Optional
from positions import Position, StrGrid, add_direction, direction_for_news
filename = sys.argv[1]

debug = False

regexes: list[str] = []
with open(filename, 'r') as f:
    for line in f:
        regexes.append(line.rstrip())

class Room():
    parent: Optional['Room']
    position: Position
    next: dict[str, 'Room']
    distance: int = 0

    def __init__(self, parent: Optional['Room'], dir: str) -> None:
        self.parent = parent
        self.next = {}
        if parent is None:
            self.distance = 0
            self.position = (0, 0)
        else:
            self.distance = parent.distance + 1
            parent.next[dir] = self
            self.position = add_direction(parent.position, direction_for_news[dir])

    def __repr__(self) -> str:
        return f"<Room {self.distance} {self.position} {list(self.next.keys())}>"

for directions in regexes:
    if directions[0] != '^' or directions[-1] != '$':
        raise ValueError(f"bad directions: {directions}")
    directions = directions[1:-1]

    maze = Room(None, "")
    grid: StrGrid = {}
    grid[maze.position] = chr(ord('0') + maze.distance)

    # stack is paren depth
    parsing_stack: list[Room] = [maze]
    max_dist: int = 0
    for c in directions:
        if c in "NEWS":
            room = Room(parsing_stack[-1], c)
            if room.position not in grid:
                grid[room.position] = chr(ord('0') + room.distance)
                max_dist = max(max_dist, room.distance)
            parsing_stack[-1] = room
            if debug:
                print(c, [r.distance for r in parsing_stack], room)
        else:
            if c == '(':
                parsing_stack.append(parsing_stack[-1])
            elif c == '|':
                parsing_stack.pop()
                parsing_stack.append(parsing_stack[-1])
            elif c == ')':
                parsing_stack.pop()
            else:
                raise ValueError(c)
            if debug:
                print(c, [r.distance for r in parsing_stack])

    print(max_dist)
    print(len([v for v in grid.values() if (ord(v) - ord('0')) >= 1000]))
    if debug: 
        print(''.join([chr(ord('0') + d) for d in range(max_dist + 1)]))

        min_x = min([x for (x, y) in grid.keys()])
        min_y = min([y for (x, y) in grid.keys()])
        max_x = max([x for (x, y) in grid.keys()])
        max_y = max([y for (x, y) in grid.keys()])
        output = ""
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                position = (x, y)
                s: str = grid.get(position, '.')
                output += s
            output += "\n"
        print(output)
