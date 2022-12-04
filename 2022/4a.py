#!/usr/bin/env python3
import sys

filename = sys.argv[1]
with open(filename, "r") as f:
    containers:int = 0
    overlaps:int = 0
    for line in f:
        pairs = line.rstrip().split(',')
        elves = sorted([[int(x) for x in pair.split('-')] for pair in pairs])
        # 1-3 is before 2-4
        # 1-2 is before 1-3
        if elves[0][0] == elves[1][0] or elves[1][1] <= elves[0][1]:
            containers += 1
        if elves[1][0] <= elves [0][1]:
            overlaps += 1
    print(f"containers: {containers}, overlaps: {overlaps}")
