#!/usr/bin/env python3
import sys
from positions import Position, manhattan, SetGrid

filename = sys.argv[1]
target_distance = int(sys.argv[2])

locations: list[Position] = []
min_x = 100
min_y = 100
max_x = 0
max_y = 0
with open(filename, "r") as f:
    for line in f:
        coords = [int(c) for c in line.split(', ')]
        min_x = min(coords[0], min_x)
        min_y = min(coords[1], min_y)
        max_x = max(coords[0], max_x)
        max_y = max(coords[1], max_y)
        locations.append(tuple(coords))

# print(locations)
print(min_x, min_y, max_x, max_y)

close_points: SetGrid = SetGrid()
for x in range(min_x, max_x + 1):
    for y in range(min_y, max_y + 1):
        current_point = (x, y)
        total_distance = 0
        for location in locations:
            total_distance += manhattan(location, current_point)
        if total_distance < target_distance:
            close_points.add(current_point)

print(len(close_points))
