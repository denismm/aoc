#!/usr/bin/env python3
import sys
from positions import SetGrid, FrozenSetGrid
import re

filename = sys.argv[1]
line_re = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')

current_points: SetGrid = set()
overlap_points: SetGrid = set()
Claim = tuple[int, FrozenSetGrid]
free_claims: set[Claim] = set()
with open(filename, "r") as f:
    for line in f:
        m = line_re.match(line)
        if not m:
            raise ValueError("bad line: " + line)
        matches: list[int] = [int(x) for x in m.groups()]
        ordinal, startx, starty, sizex, sizey = matches
        claim_points: SetGrid = set()
        for i in range(sizex):
            for j in range(sizey):
                claim_points.add((startx + i, starty + j))
        claim_overlap = (claim_points & current_points)
        if claim_overlap:
            overlap_points |= claim_overlap
            for claim in list(free_claims):
                if claim_points & claim[1]:
                    free_claims.remove(claim)
        else:
            free_claims.add((ordinal, frozenset(claim_points)))
        current_points |= claim_points

print(len(overlap_points))
print([c[0] for c in free_claims])
