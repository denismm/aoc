#!/usr/bin/env python3
import sys

filename = sys.argv[1]
with open(filename, "r") as f:
    valid_count = 0
    for line in f:
        sides = sorted([int(x) for x in line.rstrip().split()])
        # print(sides)
        if sides[0] + sides[1] > sides[2]:
            # print("ok")
            valid_count += 1
    print(valid_count)
