#!/usr/bin/env python3

import sys
from positions import (
    read_set_grid,
    Position,
    Direction,
    StrGrid,
    print_char_grid,
    div_direction,
    get_direction,
)

from math import gcd

filename = sys.argv[1]

def simplify_direction(dir: Direction) -> Direction:
    (dx, dy) = dir
    divisor = gcd(dx, dy)
    return div_direction(dir, divisor)

with open(filename, "r") as f:
    width, height, asteroids = read_set_grid(f)

seen_for_position: dict[Position, int] = {}
for station in asteroids:
    checked_directions: set[Direction] = set()
    for asteroid in asteroids:
        if asteroid is station:
            continue
        direction = simplify_direction(get_direction(station, asteroid))
        if direction in checked_directions:
            continue
        # we don't care whether we have found the outer one, as long as
        # there is something in this direction
        checked_directions.add(direction)
    # print(f"{station}: {checked_directions}")
    seen_for_position[station] = len(checked_directions)

print(max(seen_for_position.values()))

if False:
    report: StrGrid = {p: str(v) for p, v in seen_for_position.items()}

    print(print_char_grid(width, height, report))
