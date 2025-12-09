#!/usr/bin/env python3

import sys
from positions import Position, euclidean
from itertools import combinations
from math import prod

filename = sys.argv[1]
connections = int(sys.argv[2])

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

circuit_for_point: dict[Position, set[Position]] = {}

for dist, source, target in distances[:connections]:
    if source not in circuit_for_point:
        circuit_for_point[source] = {source}
    source_circuit = circuit_for_point[source]
    if target not in circuit_for_point:
        circuit_for_point[target] = {target}
    target_circuit = circuit_for_point[target]
    target_circuit |= source_circuit
    for source in source_circuit:
        circuit_for_point[source] = target_circuit
circuits: set[frozenset[Position]] = { frozenset(circuit) for circuit in circuit_for_point.values()}

circuit_sizes = [len(circuit) for circuit in circuits]
circuit_sizes.sort()

print(prod(circuit_sizes[-3:]))
