#!/usr/bin/env python3
import sys
from positions import Position, direction_for_symbol, add_direction

filename = sys.argv[1]

with open(filename, 'r') as f:
    for line in f:
        position: Position = (0, 0)
        houses: set[Position] = { position }
        for symbol in line:
            direction = direction_for_symbol.get(symbol, (0, 0))
            position = add_direction(position, direction)
            houses.add(position)
        print(len(houses))
