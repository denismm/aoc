#!/usr/bin/env python3

import sys

filename = sys.argv[1]

directions = {'L': -1, 'R': 1}
zeroes = 0
passes = 0
position = 50
with open(filename, 'r') as f:
    for line in f:
        direction = line[0]
        magnitude = int(line[1:])
        change = magnitude * directions[direction]
        true_new = position + change
        new_passes = 0
        if magnitude > 100:
            new_passes += magnitude // 100
            magnitude %= 100
        change = magnitude * directions[direction]
        new_position = position + change
        if new_position // 100 != 0:
            if not (position == 0 and direction == 'L'):
                new_passes += 1
        if new_position == 0 and direction == 'L':
            new_passes += 1
        # print(f"from {position} to {true_new}: {new_passes} ({position=} {new_position=} {direction=})")
        passes += new_passes
        position += change
        position %= 100
        if position == 0:
            zeroes += 1
print(zeroes)
print(passes)
