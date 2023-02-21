#!/usr/bin/env python3
import sys
import re
import collections
from frozendict import frozendict  # type: ignore[attr-defined]
from typing import NamedTuple

filename = sys.argv[1]

Node = NamedTuple('Node', [('size', int), ('used', int)])

Coord = NamedTuple('Coord', [('x', int), ('y', int)])

Grid = dict[Coord, Node]
nodes: Grid = {}

node_re = re.compile(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')

with open(filename, 'r') as f:
    for line in f:
        if m := node_re.match(line.rstrip()):
            (x, y, size, used, avail, percent) = [int(x) for x in m.groups()]
            if avail != size - used:
                raise ValueError(f"bad avail in {line}: {size - used} != {avail}")
            if percent != int(100 * used/size):
                raise ValueError(f"bad percent in {line}")
            # drop avail so we don't have to keep it updated
            coord = Coord(x, y)
            nodes[coord] = Node(size, used)
            if used == 0:
                empty_coord: Coord = coord

max_x = max([c.x for c in nodes])
max_y = max([c.y for c in nodes])
original_goal = Coord(max([c.x for c in nodes]), 0)

# just find usable coordinates
empty_size = nodes[empty_coord].size
node_set: set[Coord] = set()
for coord, node in nodes.items():
    if node.used <= empty_size:
        node_set.add(coord)

Move = tuple[Coord, Coord]

directions = [Coord(0, 1), Coord(1, 0), Coord(-1, 0), Coord(0, -1)]

def add_coord(p: Coord, d: Coord) -> Coord:
    return Coord(p.x + d.x, p.y + d.y)

def find_moves(location: Coord) -> list[Move]:
    moves: list[Move] = []
    for d in directions:
        source = add_coord(location, d)
        if source in node_set:
            moves.append((source, location))
    return moves

State = NamedTuple('State', [('empty', Coord), ('goal', Coord)])
queue: collections.deque[tuple[State, int, tuple[Move,]]] = collections.deque()
target = Coord(0, 0)
start_state = State(empty_coord, original_goal)
queue.append((start_state, 0, ()))      # type: ignore [arg-type]
seen: set[State] = {start_state}
while len(queue):
    this_state, this_steps, this_moves = queue.popleft()
    new_steps = this_steps + 1
    moves = find_moves(this_state.empty)
    for move in moves:
        (a_pos, b_pos) = move
        # this moves what's in a_pos into the empty
        if a_pos == this_state.goal:
            new_goal = b_pos
            if b_pos == target:
                print(new_steps)
                exit(0)
        else:
            new_goal = this_state.goal
        new_state = State(a_pos, new_goal)
        if new_state not in seen:
            seen.add(new_state)
            queue.append((new_state, new_steps, this_moves + (move,)))  # type: ignore [arg-type]
print("no solution found")
