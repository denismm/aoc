#!/usr/bin/env python3
import sys
from positions import Position, cardinal_directions, add_direction, read_char_grid
filename = sys.argv[1]

with open(filename, "r") as f:
    _, _, map = read_char_grid(f)

trailheads = [k for k, v in map.items() if v == '0']

total_score = 0
total_rating = 0

Path = list[Position]

for th in trailheads:
    paths: list[Path] = [[th]]
    for altitude in "123456789":
        new_paths: list[Path] = []
        for path in paths:
            for dir in cardinal_directions:
                step = add_direction(path[-1], dir)
                if step in map and map[step] == altitude:
                    new_paths.append(path + [step])
        paths = new_paths
    total_rating += len(paths)
    locations: set[Position] = { p[-1] for p in paths }
    total_score += len(locations)
print(total_score)
print(total_rating)
