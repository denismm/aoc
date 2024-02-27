#!/usr/bin/env python3
import sys
from typing import Optional
from itertools import permutations
from collections import defaultdict

filename = sys.argv[1]

distance: dict[frozenset[str], int] = defaultdict(int)

places: set[str] = set()

with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        line = line.rstrip('.')
        tokens = line.split()
        # Alice would gain 54 happiness units by sitting next to Bob
        # 0     1     2    3  4         5     6  7       8    9  10
        key = frozenset([tokens[0], tokens[10]])
        happiness = int(tokens[3])
        if tokens[2] == 'lose':
            happiness *= -1
        distance[key] += happiness
        places.add(tokens[0])
        places.add(tokens[10])

best_distance: Optional[int] = None
worst_distance: int = 0

for route in permutations(places):
    route_distance = 0
    for i in range(len(route) - 1):
        key = frozenset([route[i], route[i + 1]])
        route_distance += distance[key]
    route_distance += distance[frozenset([route[-1], route[0]])]
    if best_distance is None or route_distance < best_distance:
        best_distance = route_distance
    if route_distance > worst_distance:
        worst_distance = route_distance

print(best_distance)
print(worst_distance)
