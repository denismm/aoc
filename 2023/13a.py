#!/usr/bin/env python3
import sys
from positions import Position
from typing import NamedTuple

filename = sys.argv[1]

Pattern = NamedTuple(
    "Pattern", [("grid", frozenset[Position]), ("dimensions", tuple[int, int])]
)
patterns: list[Pattern] = []

with open(filename, "r") as f:
    j = 0
    current_grid: set[Position] = set()
    width = 0
    for line in f:
        line = line.rstrip()
        if line == '':
            patterns.append(Pattern(frozenset(current_grid), (width, j)))
            current_grid.clear()
            j = 0
            width = 0
        else:
            for i, char in enumerate(line):
                if char == '#':
                    current_grid.add((i, j))
            width = len(line)
            j += 1
    if patterns:
        patterns.append(Pattern(frozenset(current_grid), (width, j)))

def flip_point(position: Position, mirror: int, coordinate: int) -> Position:
    result: list[int] = []
    for c, x in enumerate(position):
        if c == coordinate:
            result.append(2 * mirror - x - 1)
        else:
            result.append(x)
    return tuple(result)

total_score = 0
total_smudge_score = 0

for p_i, pattern in enumerate(patterns):
    multipliers = (1, 100)
    for c in range(2):
        for mirror in range(1, pattern.dimensions[c]):
            min_coord = max(0, 2 * mirror - pattern.dimensions[c])
            reflected_grid = set(flip_point(p, mirror, c) for p in pattern.grid)
            first_side = set(p for p in pattern.grid if min_coord <= p[c] < mirror)
            second_side = set(p for p in reflected_grid if min_coord <= p[c] < mirror)
            if first_side == second_side:
                # print(f"{p_i}: reflection at {c}, {mirror}")
                total_score += mirror * multipliers[c]
            elif len(first_side ^ second_side) == 1:
                # print(f"{p_i}: smudge reflection at {c}, {mirror}")
                total_smudge_score += mirror * multipliers[c]
print(total_score)
print(total_smudge_score)
