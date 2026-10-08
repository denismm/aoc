#!/usr/bin/env python3

import sys
from collections import defaultdict
from positions import (
    read_set_grid,
    Position,
    Direction,
    StrGrid,
    print_char_grid,
    div_direction,
    get_direction,
)

from math import gcd, atan2

jackpot = 200

filename = sys.argv[1]

def simplify_direction_with_distance(dir: Direction) -> tuple[Direction, int]:
    (dx, dy) = dir
    divisor = gcd(dx, dy)
    return div_direction(dir, divisor), divisor

with open(filename, "r") as f:
    width, height, asteroids = read_set_grid(f)

Target = tuple[int, Position]   # "distance" and position
TargetDict = dict[Direction, list[Target]]
seen_for_position: dict[Position, int] = {}
polar_for_position: dict[Position, TargetDict] = {}
for station in asteroids:
    polar_asteroids: TargetDict = defaultdict(list)
    for asteroid in asteroids:
        if asteroid is station:
            continue
        direction, distance = simplify_direction_with_distance(get_direction(station, asteroid))
        polar_asteroids[direction].append( (distance, asteroid))
    seen_for_position[station] = len(polar_asteroids)
    polar_for_position[station] = dict(polar_asteroids)

most_seen = max(seen_for_position.values())
best_station = [pos for pos, n in seen_for_position.items() if n == most_seen][0]
print(f"{best_station}: {most_seen}")

targets = polar_for_position[best_station]

directions = list(targets.keys())
def fake_angle(dir: Direction) -> float:
    # I believe feeding -x, -y into the function expecting y, x
    # does the right thing here
    (dx, dy) = dir
    return atan2(-dx, dy)

dir_for_angle: dict[float, Direction] = {fake_angle(d): d for d in directions}
angles = list(sorted(dir_for_angle.keys()))

if dir_for_angle[angles[-1]] == (0, -1):
    # the atan2 in math goes from (-pi to pi] and I want [-pi to pi)
    last_angle = angles.pop()
    angles.insert(0, last_angle)

if False:
    for angle in angles:
        print(f"{angle}: {dir_for_angle[angle]}")
    exit(0)
zaps = 0
while True:
    for angle in angles:
        dir = dir_for_angle[angle]
        zappable = targets[dir]
        zappable.sort()
        if zappable:
            zapped = zappable.pop(0)
            zaps += 1
            # print(f"{angle} ({dir}) {zaps}: {zapped}")
            if zaps == 200:
                code = zapped[1][0] * 100 + zapped[1][1]
                print(f"{code} ({zapped})")
                exit(0)

if False:
    report: StrGrid = {p: str(v) for p, v in seen_for_position.items()}

    print(print_char_grid(width, height, report))
