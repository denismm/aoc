#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, "r") as f:
    total_paper = 0
    total_ribbon = 0
    for line in f:
        sides = sorted([int(d) for d in line.split("x")])
        paper = (
            3 * (sides[0] * sides[1])
            + 2 * (sides[0] * sides[2])
            + 2 * (sides[1] * sides[2])
        )
        total_paper += paper
        ribbon = 2 * sides[0] + 2 * sides[1] + sides[0] * sides[1] * sides[2]
        total_ribbon += ribbon

print(f"paper: {total_paper}")
print(f"ribbon: {total_ribbon}")
