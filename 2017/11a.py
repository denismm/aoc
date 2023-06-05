#!/usr/bin/env python3
import sys
from positions import Position, add_direction

# directions and distance from https://www.redblobgames.com/grids/hexagons/

filename = sys.argv[1]

directions: dict[str, Position] = {
    'n' : ( 0, -1),
    'ne': ( 1, -1),
    'se': ( 1,  0),
    's' : ( 0,  1),
    'sw': (-1,  1),
    'nw': (-1,  0),
}

def hex_distance(current: Position) -> int:
    (q, r) = current
    s: int = -q - r
    return max([ abs(x) for x in [q, r, s]])

with open(filename, 'r') as f:
    for line in f:
        steps = line.rstrip().split(',')
        furthest: int = 0
        location: Position = (0, 0)
        for step in steps:
            step_direction = directions[step]
            location = add_direction(location, step_direction)
            distance = hex_distance(location)
            if distance > furthest:
                furthest = distance
        print(hex_distance(location), furthest)
