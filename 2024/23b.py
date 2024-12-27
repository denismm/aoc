#!/usr/bin/env python3
import sys
from collections import defaultdict
from functools import reduce

filename = sys.argv[1]

neighbors: dict[str, set[str]] = defaultdict(set)

with open(filename, "r") as f:
    for line in f:
        machines: list[str] = line.rstrip().split('-')
        neighbors[machines[0]].add(machines[1])
        neighbors[machines[1]].add(machines[0])
set_size = 2
full_sets: set[frozenset[str]] = { frozenset({k, v}) for k, n in neighbors.items() for v in n}

print(len(full_sets))

while len(full_sets) > 1:
    new_fulls: set[frozenset[str]] = set()
    set_size += 1
    for subset in full_sets:
        buddies = reduce(lambda x, y: x & y, [neighbors[s] for s in subset])
        for b in buddies:
            new_fulls.add(frozenset(subset | {b}))
    if not new_fulls:
        raise ValueError(f"no full sets at {set_size}")
    full_sets = new_fulls
    print(len(full_sets))
final_set = full_sets.pop()
print(",".join(sorted(final_set)))
