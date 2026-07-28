#!/usr/bin/env python3

import sys
from collections import defaultdict
filename = sys.argv[1]

satellites: dict[str, list[str]] = defaultdict(list)
with open(filename, 'r') as f:
    for line in f:
        planet, moon = line.rstrip().split(')')
        satellites[planet].append(moon)

steps = 0
step_for_body: dict[str, int] = {}
frontier = ['COM']
while frontier:
    next_frontier = []
    for planet in frontier:
        step_for_body[planet] = steps
        next_frontier += satellites[planet]
    steps += 1
    frontier = next_frontier

print(sum(step_for_body.values()))
