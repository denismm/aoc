#!/usr/bin/env python3
import sys
from positions import Position, Direction, add_direction, cardinal_directions
from typing import NamedTuple
from queue import PriorityQueue

filename = sys.argv[1]

Grid = dict[Position, int]
grid: Grid = {}

with open(filename, "r") as f:
    for j, line in enumerate(f):
        line = line.rstrip()
        width = len(line)
        for i, char in enumerate(line.rstrip()):
            grid[(i, j)] = int(char)
height = j + 1

# position of crucible + direction + number of steps in this direction
Step = NamedTuple('Step', [('location', Position), ('dir', Direction), ('substep', int)])
QueueEntry = NamedTuple('QueueEntry', [('heat_loss', int), ('step', Step), ('path', tuple[Step, ...])])

first_step = Step((0, 0), (1, 0), 0)
target: Position = (width - 1, height - 1)
seen_steps: set[Step] = {first_step}

queue: PriorityQueue[QueueEntry] = PriorityQueue()
queue.put(QueueEntry(0, first_step, (first_step,)))
while (queue):
    # print([(e.heat_loss, e.step.location, e.step.dir, e.step.substep) for e in queue])
    entry = queue.get()
    step = entry.step
    if step.location == target and step.substep >= 3:
        print(f"smallest_loss: {entry.heat_loss}")
        if False:
            path_locs = [step.location for step in entry.path]
            for j in range(height):
                for i in range(width):
                    pos = (i, j)
                    if pos in path_locs:
                        print('#', end="")
                    else:
                        print(grid[pos], end="")
                print()
        exit(0)
    for direction in cardinal_directions:
        new_substep = step.substep + 1
        if add_direction(direction, step.dir) == (0, 0):
            continue
        elif direction != step.dir:
            if new_substep < 4:
                # invalid turn
                continue
            # print(f"{entry.heat_loss} turning at {step.location} {new_substep}")
            new_substep = 0
        if new_substep >= 10:
            continue
        new_location = add_direction(step.location, direction)
        if new_location in grid:
            new_heat_loss = entry.heat_loss + grid[new_location]
            new_step = Step(new_location, direction, new_substep)
            new_path = entry.path + (new_step,)
            if new_step in seen_steps:
                continue
            seen_steps.add(new_step)
            queue.put(QueueEntry(new_heat_loss, new_step, new_path))
