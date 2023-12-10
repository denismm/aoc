#!/usr/bin/env python3
import sys

filename = sys.argv[1]

direction: dict[str, int] = {'(': 1, ')': -1}

with open(filename, 'r') as f:
    for line in f:
        floor = 0
        for i, character in enumerate(line):
            floor += direction.get(character, 0)
            if floor < 0:
                print(i+1)
                break
