#!/usr/bin/env python3
import sys
from positions import Position, add_direction, cardinal_directions
from queue import PriorityQueue
from dataclasses import dataclass

filename = sys.argv[1]

with open(filename, 'r') as f:
    lines = [l for l in f]
    depth = int(lines[0].split()[1])
    target_s = lines[1].split()[1]
    target: Position = tuple([int(s) for s in target_s.split(',')])

grid: dict[Position, int] = {}  # level for each coordinate

debug = False

index: int
level: int
display = ".=|"
position: Position
for j in range(target[1] + 1 + target[1] * 2 ):
    for i in range(target[0] + 1 + target[1] * 2):
        position = (i, j)
        if position == target:
            index = 0
        else:
            if i == 0:
                if j == 0:
                    index = 0
                else:       # (0, n)
                    index = j * 48271
            else:
                if j == 0:  # (n, 0)
                    index = i * 16807
                else:
                    index = grid[(i - 1, j)] * grid[(i, j - 1)]
        level = (index + depth) % 20183
        grid[position] = level
        if debug:
            print(display[level % 3], end="")
    if debug:
        print()

risk = sum([v % 3 for k, v in grid.items() if k[0] <= target[0] and k[1] <= target[1]])
print(risk)

cave: dict[Position, int] = {p: v % 3 for p, v in grid.items()}

# now make your way to the target

State = tuple[Position, int]    # position and tool
# neither: 0
# torch: 1
# climbing gear: 2
# tool can't be same as cave

@dataclass(order=True, eq=True, repr=True)
class Entry:
    time: int
    state: State

start = ((0, 0), 1)
end = ((target), 1)
best_time: dict[State, int] = {start: 0}
queue: PriorityQueue[Entry] = PriorityQueue()
queue.put(Entry(0, start))
while (queue):
    entry = queue.get()
    time = entry.time
    (position, tool) = entry.state
    new_entries: list[Entry] = []
    # where can we go with this tool?
    for direction in cardinal_directions:
        new_position = add_direction(position, direction)
        if new_position in cave:
            if cave[new_position] != tool:
                new_entries.append(Entry(time + 1, (new_position, tool)))
        else:
            if position[0] * position[1] > 0:
                raise ValueError(f"hit border at {new_position}")
    # or maybe we stay still
    new_tool = 3 - tool - cave[position]
    new_entries.append(Entry(time + 7, (position, new_tool)))
    for new_entry in new_entries:
        # have we seen this already?
        if new_entry.state in best_time:
            if new_entry.time >= best_time[new_entry.state]:
                continue
        if new_entry.state == end:
            print(new_entry.time)
            exit(0)
        best_time[new_entry.state] = new_entry.time
        queue.put(new_entry)
