#!/usr/bin/env python3

from positions import Position, manhattan


p1: Position = (0, 0, 0)
r1: int = 5
p2: Position = (5, 3, 2)
r2: int = 6


for x in range(-10, 10):
    for y in range(-10, 10):
        for z in range(-10, 10):
            pos: Position = (x, y, z)
            if manhattan(pos, p1) <= r1 and manhattan(pos, p2) <= r2:
                print(pos)
