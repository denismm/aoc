#!/usr/bin/env python3

import sys
from positions import Position, euclidean
from itertools import combinations

filename = sys.argv[1]

nodes: list[Position] = []
with open(filename, 'r') as f:
    for line in f:
        points = [int(s) for s in line.rstrip().split(',')]
        nodes.append(tuple(points))
print("nodes:", len(nodes))

distances: list[tuple[float, Position, Position]] = []

for source, target in combinations(nodes, 2):
    dist = euclidean(source, target)
    distances.append((dist, source, target))

print("distances:", len(distances))

distances.sort()

circuit_for_point: dict[Position, frozenset[Position]] = {p: frozenset([p]) for p in nodes}
circuits: set[frozenset[Position]] = set(circuit_for_point.values())

for dist, source, target in distances:
    source_circuit = circuit_for_point[source]
    target_circuit = circuit_for_point[target]
    if source_circuit == target_circuit:
        continue
    new_circuit = frozenset(target_circuit | source_circuit)
    for node in new_circuit:
        circuit_for_point[node] = new_circuit
    circuits.remove(source_circuit)
    circuits.remove(target_circuit)
    circuits.add(new_circuit)
    if len(circuits) == 1:
        print(source[0] * target[0])
        exit(0)
