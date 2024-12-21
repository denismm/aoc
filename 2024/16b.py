#!/usr/bin/env python3
import sys
from collections import defaultdict
from positions import (
    Position,
    Direction,
    add_direction,
    read_char_grid,
    cardinal_directions,
)

turns: dict[Direction, list[Direction]] = {}
for i, dir in enumerate(cardinal_directions):
    turns[dir] = [
        cardinal_directions[(i - 1) % 4],
        cardinal_directions[(i + 1) % 4],
    ]

filename = sys.argv[1]

with open(filename, "r") as f:
    _, _, grid = read_char_grid(f)

start: Position = [k for k, v in grid.items() if v == "S"][0]
end: Position = [k for k, v in grid.items() if v == "E"][0]
walls: set[Position] = {k for k, v in grid.items() if v == "#"}

# Weighted Dijkstra but direction changes cost 1000
State = tuple[Position, Direction]
start_state = (start, (1, 0))
seen: set[State] = set()
frontiers: dict[int, dict[State, set[Position]]] = defaultdict(lambda: defaultdict(set), {0: {start_state: {start}}})

while frontiers:
    sofar: int = min(frontiers.keys())
    state_dict: dict[State, set[Position]] = frontiers.pop(sofar)
    for state, visited in state_dict.items():
        # could have found a shortcut
        if state in seen:
            continue
        seen.add(state)
        (pos, dir) = state
        if pos == end:
            print(sofar)
            print(len(visited))
            exit(0)
        # ahead
        ahead = (add_direction(pos, dir), dir)
        if ahead[0] not in walls:
            frontiers[sofar + 1][ahead] |= (visited | {ahead[0]})
        # turns
        for turn in turns[dir]:
            # print(f"checking {turn}")
            if add_direction(pos, turn) not in walls:
                frontiers[sofar + 1000][(pos, turn)] |= visited
