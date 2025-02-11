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
    step = 0
    for f in range(2, s):
        if s % f == 0:
            step = s // f
            break
    print(s, step)
    for x in range(1, 302 - s):
        for y in range(1, 302 - s):
            position: Position = (x, y)
            total: int = 0
            if s == 1:
                total = grid[position]
            else:
                if step:
                    for dx in range(0, s, step):
                        for dy in range(0, s, step):
                            d: Direction = (dx, dy)
                            total += cache[add_direction(position, d), step]
                else:
                    total = cache[position, s - 1]
                    for i in range(s - 1):
                        total += grid[add_direction(position, (s - 1, i))]
                        total += grid[add_direction(position, (i, s - 1))]
                    total += grid[add_direction(position, (s - 1, s - 1))]
            cache[(position, s)] = total
            if total > best:
                best = total
                best_pos = (position, s)
    print(best, ','.join([str(x) for x in best_pos]))
