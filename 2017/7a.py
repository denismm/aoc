#!/usr/bin/env python3
import sys

filename = sys.argv[1]

parent: dict[str, str] = {}
nodes: set[str] = set()

with open(filename, 'r') as f:
    for line in f:
        (sections) = line.rstrip().split(' -> ')
        node_info = sections[0]
        node = node_info.split()[0]
        if len(sections) > 1:
            for child in sections[1].split(', '):
                parent[child] = node
        nodes.add(node)
roots = nodes - set(parent.keys())
print(roots)

