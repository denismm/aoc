#!/usr/bin/env python3
import sys
from typing import NamedTuple

filename = sys.argv[1]
race_time = int(sys.argv[2])

Reindeer = NamedTuple("Reindeer", [("speed", int), ("span", int), ("rest", int)])

reindeer: dict[str, Reindeer] = {}

with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        tokens = line.split()
        # Comet can fly 14 km/s for 10 seconds, but then must rest for 127 ...
        # 0     1   2   3  4    5   6  7        8   9    10   11   12  13
        spec = Reindeer(int(tokens[3]), int(tokens[6]), int(tokens[13]))
        reindeer[tokens[0]] = spec

best_reindeer: str = ""
best_distance: int = 0

for r, spec in reindeer.items():
    step_time = spec.span + spec.rest
    steps = race_time // step_time
    distance = spec.speed * spec.span * steps
    extra = race_time % step_time
    distance += spec.speed * min([extra, spec.span])
    if distance > best_distance:
        best_distance = distance
        best_reindeer = r

print(best_reindeer, best_distance)
