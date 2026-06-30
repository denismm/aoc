#!/usr/bin/env python3

import sys
from positions import (
    IntGrid,
    Position,
    Direction,
    ORIGIN,
    add_direction,
    direction_for_udlr,
)

filename = sys.argv[1]

with open(filename, "r") as f:
    wires: list[str] = [line.rstrip() for line in f]

first_wire: IntGrid = {}
turtle: Position = ORIGIN
full_steps: int = 0
for segment in wires[0].split(","):
    dir: Direction = direction_for_udlr[segment[0]]
    steps: int = int(segment[1:])
    for _ in range(steps):
        turtle = add_direction(turtle, dir)
        full_steps += 1
        if turtle not in first_wire:
            first_wire[turtle] = full_steps

# this seems legitimately larger than any correct answer
best_distance = len(first_wire) * 2
turtle = ORIGIN
full_steps = 0
for segment in wires[1].split(","):
    dir = direction_for_udlr[segment[0]]
    steps = int(segment[1:])
    for _ in range(steps):
        turtle = add_direction(turtle, dir)
        full_steps += 1
        if turtle in first_wire:
            distance = first_wire[turtle] + full_steps
            if distance < best_distance:
                best_distance = distance
if best_distance == len(first_wire):
    raise ValueError("no intersections")

print(best_distance)
