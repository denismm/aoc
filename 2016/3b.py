#!/usr/bin/env python3
import sys

filename = sys.argv[1]
with open(filename, "r") as f:
    valid_count = 0
    side_sets = [[], [], []]
    for line in f:
        input_sides = [int(x) for x in line.rstrip().split()]
        for i in range(3):
            side_sets[i].append(input_sides[i])
        if len(side_sets[0]) == 3:
            for triangle in side_sets:
                sides = sorted(triangle)
                if sides[0] + sides[1] > sides[2]:
                    valid_count += 1
            side_sets = [[], [], []]
    print(valid_count)
