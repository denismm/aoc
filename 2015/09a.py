#!/usr/bin/env python3
import sys
from typing import Optional
from itertools import permutations

filename = sys.argv[1]

distance: dict[frozenset[str], int] = {}

places: set[str] = set()

with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        tokens = line.split()
        key = frozenset([tokens[0], tokens[2]])
        distance[key] = int(tokens[4])
        places.add(tokens[0])
        places.add(tokens[2])

best_distance: Optional[int] = None
worst_distance: int = 0

for route in permutations(places):
    route_distance = 0
    for i in range(len(route) - 1):
        key = frozenset([route[i], route[i + 1]])
        route_distance += distance[key]
    if best_distance is None or route_distance < best_distance:
        best_distance = route_distance
    if route_distance > worst_distance:
        worst_distance = route_distance

print(best_distance)
print(worst_distance)
