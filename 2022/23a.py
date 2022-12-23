#!/usr/bin/env python3
import sys
from collections import defaultdict
from typing import DefaultDict

Position = tuple[int, ...]
grid: set[Position] = set()

filename = sys.argv[1]
with open(filename, "r") as f:
    for y, line in enumerate(f):
        for x, character in enumerate(line.rstrip()):
            if character == '#':
                input_position = (x, y)
                grid.add(input_position)

neighbors = [ (dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if dx or dy]
direction_start = 0
# NSWE, N is neg
obstructions = [
    [ (dx, -1) for dx in range(-1, 2) ],
    [ (dx, 1) for dx in range(-1, 2) ],
    [ (-1,  dy) for dy in range(-1, 2) ],
    [ (1,  dy) for dy in range(-1, 2) ],
]
# same order as obstructions
directions = [obs[1] for obs in obstructions]

def add_pos(position: Position, dir: Position) -> Position:
    return tuple([p + d for p, d in zip(position, dir)])

def print_grid() -> None:
    maxes: list[int] = []
    mins: list[int] = []
    for c in range(2):
        maxes.append(max([elf[c] for elf in grid]))
        mins.append(min([elf[c] for elf in grid]))
    full_area = (1 + maxes[0] - mins[0]) * (1 + maxes[1] - mins[1])
    for y in range(mins[1], maxes[1] + 1):
        elf_row = ['#' if (x, y) in grid else '.' for x in range(mins[0], maxes[0] + 1)]
        print(''.join(elf_row))
    print(full_area - len(grid))


for round in range(10):
    round_dirs = [ (dir + direction_start) % 4 for dir in range(4) ]
    proposal: dict[Position, Position] = {}
    for elf in grid:
        neighbor_set = set([ add_pos(elf, n) for n in neighbors])
        if not neighbor_set & grid:
            continue
        for dir in round_dirs:
            obstruction_set = set([add_pos(elf, d) for d in obstructions[dir]])
            # print(f"elf at {elf} checking {obstruction_set}")
            if not obstruction_set & grid:
                proposal[elf] = add_pos(elf, directions[dir])
                # print(f"elf at {elf} moving to {proposal[elf]}")
                break
    collision_dict: DefaultDict[Position, int] = defaultdict(lambda: 0)
    for value in proposal.values():
        collision_dict[value] += 1
    for elf, next_step in proposal.items():
        if collision_dict[next_step] == 1:
            if next_step in grid:
                raise ValueError(f"ELF COLLISION in round {round} at {next_step}!")
            grid.remove(elf)
            grid.add(next_step)
    direction_start = (direction_start + 1) % 4
print_grid()
