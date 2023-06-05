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

with open(filename, 'r') as f:
    for line in f:
        steps = line.rstrip().split(',')
        location: Position = (0, 0)
        for step in steps:
            step_direction = directions[step]
            location = add_direction(location, step_direction)
        (q, r) = location
        s: int = -q - r
        distance = max([ abs(x) for x in [q, r, s]])
        print(distance)
