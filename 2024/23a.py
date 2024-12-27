#!/usr/bin/env python3
import sys
from tqdm import tqdm
from collections import defaultdict

filename = sys.argv[1]

neighbors: dict[str, set[str]] = defaultdict(set)

with open(filename, "r") as f:
    for line in f:
        machines: list[str] = line.rstrip().split('-')
        neighbors[machines[0]].add(machines[1])
        neighbors[machines[1]].add(machines[0])

t_sets: set[frozenset[str]] = set()
for machine, ns in tqdm([(m, v) for m, v in neighbors.items() if m.startswith('t')]):
    for n in ns:
        for nn in (ns & neighbors[n]):
            t_sets.add(frozenset({machine, n, nn}))
print(len(t_sets))
