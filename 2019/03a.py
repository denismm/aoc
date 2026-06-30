#!/usr/bin/env python3

import sys
from positions import (
    SetGrid,
    Position,
    Direction,
    add_direction,
    manhattan,
    direction_for_udlr,
)

filename = sys.argv[1]

with open(filename, "r") as f:
    wires: list[str] = [line.rstrip() for line in f]

ORIGIN: Position = (0, 0)

first_wire: SetGrid = set()
turtle: Position = ORIGIN
for segment in wires[0].split(","):
    dir: Direction = direction_for_udlr[segment[0]]
    steps: int = int(segment[1:])
    for _ in range(steps):
        turtle = add_direction(turtle, dir)
        first_wire.add(turtle)

# this seems legitimately larger than any correct answer
best_distance = len(first_wire)
turtle = ORIGIN
for segment in wires[1].split(","):
    dir = direction_for_udlr[segment[0]]
    steps = int(segment[1:])
    for _ in range(steps):
        turtle = add_direction(turtle, dir)
        if turtle in first_wire:
            distance = manhattan(ORIGIN, turtle)
            if distance < best_distance:
                best_distance = distance
if best_distance == len(first_wire):
    raise ValueError("no intersections")

print(best_distance)
