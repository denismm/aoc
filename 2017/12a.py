#!/usr/bin/env python3
import sys

filename = sys.argv[1]

connections: dict[int, list[int]] = {}

with open(filename, 'r') as f:
    for line in f:
        (start, target_string) = line.rstrip().split(' <-> ')
        targets = target_string.split(', ')
        connections[int(start)] = [int(x) for x in targets]

seen: set[int] = set()
stack: list[int] = [0]

while stack:
    current = stack.pop()
    seen.add(current)
    for next in connections[current]:
        if next not in seen:
            stack.append(next)

print(len(seen))
