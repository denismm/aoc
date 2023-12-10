#!/usr/bin/env python3
import sys
from positions import Position, direction_for_symbol, add_direction

filename = sys.argv[1]

with open(filename, 'r') as f:
    for line in f:
        santa_pos: list[Position] = [(0, 0), (0, 0)]
        houses: set[Position] = { santa_pos[0] }
        for i, symbol in enumerate(line):
            santa = i % 2
            direction = direction_for_symbol.get(symbol, (0, 0))
            santa_pos[santa] = add_direction(santa_pos[santa], direction)
            houses.add(santa_pos[santa])
        print(len(houses))
