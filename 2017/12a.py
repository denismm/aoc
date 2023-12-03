#!/usr/bin/env python3
import sys

filename = sys.argv[1]

connections: dict[int, list[int]] = {}

with open(filename, 'r') as f:
    for line in f:
        (start, target_string) = line.rstrip().split(' <-> ')
        targets = target_string.split(', ')
        connections[int(start)] = [int(x) for x in targets]

groups: set[frozenset[int]] = set()
seen: set[int] = set()

def find_group(source: int) -> set[int]:
    stack: list[int] = [source]
    group: set[int] = set()
    while stack:
        current = stack.pop()
        seen.add(current)
        group.add(current)
        for next in connections[current]:
            if next not in seen:
                stack.append(next)
    return group

zero_group = find_group(0)
print(len(zero_group))
groups.add(frozenset(zero_group))

nodes = set(connections.keys()) - seen
while nodes:
    source_node = nodes.pop()
    newgroup = find_group(source_node)
    nodes -= newgroup
    groups.add(frozenset(newgroup))

print(len(groups))
