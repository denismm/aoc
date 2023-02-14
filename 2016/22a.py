#!/usr/bin/env python3
import sys
import re
from typing import NamedTuple

filename = sys.argv[1]

Node = NamedTuple('Node', [('x', int), ('y', int), ('size', int), ('used', int), ('avail', int)])

nodes: list[Node] = []

node_re = re.compile(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')

with open(filename, 'r') as f:
    for line in f:
        if m := node_re.match(line.rstrip()):
            (x, y, size, used, avail, percent) = [int(x) for x in m.groups()]
            if avail != size - used:
                raise ValueError(f"bad avail in {line}: {size - used} != {avail}")
            if percent != int(100 * used/size):
                raise ValueError(f"bad percent in {line}")
            nodes.append(Node(x, y, size, used, avail))
total = 0
for A in nodes:
    for B in nodes:
        if A != B and A.used > 0 and A.used <= B.avail:
            total += 1

print(total)
