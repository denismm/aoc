#!/usr/bin/env python3
import sys
import collections
from typing import NamedTuple, Optional

Position = tuple[int, ...]
MazeState = NamedTuple("MazeState", [("position", Position), ("distance", int)])

filename = sys.argv[1]
with open(filename, "r") as f:
    lines: list[str] = [line.rstrip() for line in f]

start: Optional[Position] = None
end: Optional[Position] = None
for x, line in enumerate(lines):
    y = line.find('S')
    if y >= 0:
        start = (x, y)
    y = line.find('E')
    if y >= 0:
        end = (x, y)
if start is None or end is None:
    raise ValueError("invalid heightmap")
print(f"start: {start}, end: {end}")

extents: tuple[int, int] = (len(lines), len(lines[0]))

elevation_map = {'S': 'a', 'E': 'z'}


def step_ok(current: Position, new: Position) -> bool:
    for c in range(2):
        if not 0 <= new[c] < extents[c]:
            return False
    current_elev: str = lines[current[0]][current[1]]
    current_elev = elevation_map.get(current_elev, current_elev)
    new_elev: str = lines[new[0]][new[1]]
    new_elev = elevation_map.get(new_elev, new_elev)
    if ord(new_elev) - ord(current_elev) > 1:
        return False
    return True


def check_win(current: Position) -> bool:
    return current == end


first_state = MazeState(start, 0)
seen: set[Position] = set()
queue: collections.deque[MazeState] = collections.deque([first_state])
current_round: int = -1
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
while (queue):
    state = queue.popleft()
    if state.distance != current_round:
        print(f"round {state.distance}: {len(queue) + 1}")
        # print(state, queue)
        current_round = state.distance
    new_distance = state.distance + 1
    for direction in directions:
        new_position = tuple([c + d for c, d in zip(state.position, direction)])
        if new_position in seen:
            continue
        if not step_ok(state.position, new_position):
            continue
        seen.add(new_position)
        if check_win(new_position):
            print(f"win at distance {new_distance}!")
            exit(0)
        queue.append(MazeState(new_position, new_distance))
