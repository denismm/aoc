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
    for direction in cardinal_directions:
        if add_direction(direction, step.dir) == (0, 0):
            continue
        elif direction == step.dir:
            new_substep = step.substep + 1
        else:
            new_substep = 0
        if new_substep >= 3:
            continue
        new_location = add_direction(step.location, direction)
        if new_location in grid:
            new_heat_loss = entry.heat_loss + grid[new_location]
            if new_location == target:
                print(f"smallest_loss: {new_heat_loss}")
                exit(0)
            else:
                new_step = Step(new_location, direction, new_substep)
                if new_step in seen_steps:
                    continue
                seen_steps.add(new_step)
                queue.put(QueueEntry(new_heat_loss, new_step, entry.path + (new_step,)))
