#!/usr/bin/env python3
import sys
from positions import Position, add_direction, cardinal_directions, direction_for_symbol
from pprint import pprint
from collections import deque

filename = sys.argv[1]

Grid = dict[Position, str]
grid: Grid = {}

with open(filename, "r") as f:
    for j, line in enumerate(f):
        line = line.rstrip()
        for i, char in enumerate(line):
            position = (i, j)
            grid[position] = char
start: Position = [k for k, v in grid.items() if k[1] == 0 and v == '.'][0]
target: Position = [k for k, v in grid.items() if k[1] == j and v == '.'][0]

# make this a list of nodes and paths
graph: dict[Position, dict[Position, int]] = {}

explorable: deque[Postion] = deque([start])

while(explorable):
    node = explorable.popleft()
    graph[node] = {}
    if grid[node] != '.":
        raise ValueError(f"non-path node at {node}")
