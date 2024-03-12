#!/usr/bin/env python3
import sys
from typing import NamedTuple
from collections import defaultdict
filename = sys.argv[1]
race_time = int(sys.argv[2])

Reindeer = NamedTuple('Reindeer',
    [('speed', int), ('span', int), ('rest', int), ('step', int)])

reindeer: dict[str, Reindeer] = {}

with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        tokens = line.split()
        # Comet can fly 14 km/s for 10 seconds, but then must rest for 127 ...
        # 0     1   2   3  4    5   6  7        8   9    10   11   12  13
        speed, span, rest = int(tokens[3]), int(tokens[6]), int(tokens[13])
        step = span + rest
        spec = Reindeer(speed, span, rest, step)
        reindeer[tokens[0]] = spec

r_points: dict[str, int] = defaultdict(lambda: 0)

for sofar in range(1, race_time + 1):
    r_distance: dict[str, int] = {}
    for r, spec in reindeer.items():
        steps = sofar // spec.step
        distance = spec.speed * spec.span * steps
        extra = sofar % spec.step
        distance += spec.speed * min([extra, spec.span])
        r_distance[r] = distance
    max_distance = max(r_distance.values())
    winners = 0
    for r, distance in r_distance.items():
        if distance == max_distance:
            r_points[r] += 1
            winners += 1
    # if winners > 1:
        # print(f"tie at {sofar} seconds")

max_points = max(r_points.values())
for r, points in r_points.items():
    if points == max_points:
        print(r, points)
