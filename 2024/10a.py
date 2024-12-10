#!/usr/bin/env python3
import sys
from positions import Position, cardinal_directions, add_direction, read_char_grid
filename = sys.argv[1]

with open(filename, "r") as f:
    _, _, map = read_char_grid(f)

trailheads = [k for k, v in map.items() if v == '0']

total_score = 0

for th in trailheads:
    locations: set[Position] = {th}
    for altitude in "123456789":
        new_locations: set[Position] = set()
        for location in locations:
            for dir in cardinal_directions:
                step = add_direction(location, dir)
                if step in map and map[step] == altitude:
                    new_locations.add(step)
        locations = new_locations
    total_score += len(locations)
print(total_score)
