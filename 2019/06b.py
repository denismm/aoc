#!/usr/bin/env python3

import sys
from collections import defaultdict
filename = sys.argv[1]

satellites: dict[str, list[str]] = defaultdict(list)
center: dict[str, str] = {}
with open(filename, 'r') as f:
    for line in f:
        planet, moon = line.rstrip().split(')')
        satellites[planet].append(moon)
        center[moon] = planet

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

transits = 0
start = center['YOU']
end = center['SAN']

if step_for_body[end] > step_for_body[start]:
    (start, end) = (end, start)
while step_for_body[start] > step_for_body[end]:
    start = center[start]
    transits += 1
while start != end:
    start = center[start]
    end = center[end]
    transits += 2

print(transits)
