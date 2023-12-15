#!/usr/bin/env python3
import sys
from positions import Position, add_direction

directions = ((0, -1), (-1, 0), (0, 1), (1, 0))

filename = sys.argv[1]

Grid = dict[Position, str]
grid: Grid = {}

with open(filename, "r") as f:
    for j, line in enumerate(f):
        line = line.rstrip()
        width = len(line)
        for i, char in enumerate(line.rstrip()):
            if char != '.':
                grid[(i, j)] = char
    height = j+1

def rounds(grid: Grid) -> list[Position]:
    return [p for p, v in grid.items() if v == 'O']

def score_points(points: list[Position]) -> int:
    return sum([height - j for (i, j) in points])

seen_grids: dict[frozenset[Position], int] = {}
total_cycles = 1_000_000_000
for cycle in range(total_cycles):
    for tilt in range(4):
        round_starts = rounds(grid)
        round_starts.sort()
        if tilt in (2, 3):
            round_starts.reverse()
        tilt_direction = directions[tilt]
        for start_pos in round_starts:
            new_pos = start_pos
            next_pos = add_direction(new_pos, tilt_direction)
            while next_pos not in grid and 0 <= next_pos[0] < width and 0 <= next_pos[1] < height:
                new_pos = next_pos
                next_pos = add_direction(new_pos, tilt_direction)
            if new_pos != start_pos:
                del grid[start_pos]
                grid[new_pos] = 'O'
        if cycle == 0 and tilt == 0:
            print(f"first_tilt: {score_points(rounds(grid))}")
    key = frozenset(rounds(grid))
    if key in seen_grids:
        print(f"got grid collision at {cycle}, {seen_grids[key]}")
        loop = cycle - seen_grids[key]
        end_phase = (total_cycles - 1) % loop
        # might be a run-up so use the last entry of that phase
        end_points = [
            points for points, cycle in seen_grids.items() if cycle % loop == end_phase][-1]
        print(f"last_cycle: {score_points(list(end_points))}")
        break
    else:
        seen_grids[key] = cycle
