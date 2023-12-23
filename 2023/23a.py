#!/usr/bin/env python3
import sys
from positions import Position, Direction, add_direction, cardinal_directions, direction_for_symbol, scale_direction
from typing import Iterator
from collections import deque
from pprint import pprint

filename = sys.argv[1]
uphill = ('uphill' in sys.argv)


Grid = dict[Position, str]
grid: Grid = {}

with open(filename, "r") as f:
    for j, line in enumerate(f):
        line = line.rstrip()
        for i, char in enumerate(line):
            position = (i, j)
            grid[position] = char
start: Position = [k for k, v in grid.items() if k[1] == 0 and v == '.'][0]
end: Position = [k for k, v in grid.items() if k[1] == j and v == '.'][0]

# make this a list of nodes and paths
# graph[source][target] = distance (inclusive of one end)
graph: dict[Position, dict[Position, int]] = {start: {}}

explorable: deque[Position] = deque([start])

def exits_for_position(pos: Position) -> Iterator[Direction]:
    char = grid[pos]
    directions: tuple[Direction, ...]
    if char in direction_for_symbol and not uphill:
        directions = (direction_for_symbol[char],)
    elif char in '.>v<^':
        directions = cardinal_directions
    else:
        raise ValueError(f"mysterious terrain {char} at {pos}")

    for dir in directions:
        next = add_direction(pos, dir)
        if next in grid and grid[next] != '#':
            yield dir

while (explorable):
    node = explorable.popleft()
    if grid[node] != '.':
        raise ValueError(f"non-path node at {node}")
    # find all directions from here
    directions = exits_for_position(node)
    for exit_dir in directions:
        distance = 0
        pos = node
        dir = exit_dir
        while True:
            distance += 1
            new_pos = add_direction(pos, dir)
            next_exits = set(exits_for_position(new_pos)) - {scale_direction(dir, -1)}
            if new_pos == end or len(next_exits) > 1:
                graph[node][new_pos] = distance
                if new_pos not in graph:
                    graph[new_pos] = {}
                    explorable.append(new_pos)
                break
            elif len(next_exits) == 0:
                # dead end
                break
            else:
                pos = new_pos
                dir = next_exits.pop()
# print(len(graph))
# pprint(graph)
# exit(0)

def longest_distance(path: list[Position], distance: int) -> int:
    options = graph[path[-1]]
    best_distance = 0
    for node, steps in options.items():
        if node in path:
            continue
        new_path = path + [node]
        new_distance = 0
        if node == end:
            new_distance = distance + steps
            # print(f'found path to end: {len(path)} {new_distance}')
        else:
            new_distance = longest_distance(new_path, distance + steps)
        if new_distance > best_distance:
            best_distance = new_distance
    return best_distance

print(longest_distance([start], 0))
