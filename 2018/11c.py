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

grid: dict[Position, int] = {}
for x in range(1, 301):
    for y in range(1, 301):
        p = (x, y)
        grid[p] = power_for_cell(p)

cache: dict[tuple[Position, int], int] = {}

neighborhood: list[Direction] = [ (dx, dy) for dx in range(3) for dy in range(3) ]

best = 0
best_pos_size: tuple[Position, int] = ((-1, -1), 0)
for s in range(1, 301):
    for x in range(1, 302 - s):
        for y in range(1, 302 - s):
            position: Position = (x, y)
            total: int = 0
            if s == 1:
                total = grid[position]
            elif s == 2:
                for dx in range(0, s):
                    for dy in range(0, s):
                        d: Direction = (dx, dy)
                        total += grid[add_direction(position, d)]
            else:
                offset_p = add_direction(position, (1, 1))
                total = cache[position, s - 1]
                total += cache[offset_p, s - 1]
                total -= cache[offset_p, s - 2]
                total += grid[add_direction(position, (0, s - 1))]
                total += grid[add_direction(position, (s - 1, 0))]
            cache[(position, s)] = total
            if total > best:
                best = total
                best_pos = (position, s)
print(best, ','.join([str(x) for x in best_pos]))
