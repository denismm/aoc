#!/usr/bin/env python3
import sys
from positions import Position, Direction, add_direction

serial = int(sys.argv[1])

def power_for_cell(p: Position) -> int:
    id = p[0] + 10
    level = id * p[1]
    level += serial
    level *= id
    level //= 100
    level %= 10
    level -= 5
    return level

neighborhood: list[Direction] = [ (dx, dy) for dx in range(3) for dy in range(3) ]

best = 0
best_pos: Position = (-1, -1)
for x in range(1, 299):
    for y in range(1, 299):
        position: Position = (x, y)
        total: int = 0
        for d in neighborhood:
            total += power_for_cell(add_direction(position, d))
        if total > best:
            best = total
            best_pos = position
print(best, ','.join([str(x) for x in best_pos]))
