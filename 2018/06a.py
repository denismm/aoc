#!/usr/bin/env python3
import sys
from positions import Position, manhattan
from collections import Counter

filename = sys.argv[1]

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
# print(min_x, min_y, max_x, max_y)

infinites: set[Position] = set()
area_sizes: Counter[Position] = Counter()
distant_point = (2 * max_x, 2 * max_y)
for x in range(min_x, max_x + 1):
    for y in range(min_y, max_y + 1):
        current_point = (x, y)
        closest_distance = 10000
        closest_location: list[Position] = [distant_point]
        for location in locations:
            distance = manhattan(location, current_point)
            if distance < closest_distance:
                closest_distance = distance
                closest_location = [location]
            elif distance == closest_distance:
                closest_location.append(location)
        if distant_point in closest_location:
            raise ValueError(f"{current_point=} is {closest_distance} from nowhere")
        if len(closest_location) == 1:
            source = closest_location[0]
            # print(f"{current_point} is {closest_distance} from {source}")
            area_sizes[source] += 1
            # assume no finites get past edge
            if current_point[0] in (min_x, max_x) or current_point[1] in (min_y, max_y):
                infinites.add(source)
        else:
            # print(f"tie: {current_point} is {closest_distance} from {closest_location}")
            pass
# print(infinites)
# print(area_sizes)
for location in infinites:
    del area_sizes[location]
print(max(area_sizes.values()))
