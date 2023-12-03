#!/usr/bin/env python3
import sys

filename = sys.argv[1]

direction: dict[str, int] = {'(': 1, ')': -1}

with open(filename, 'r') as f:
    for line in f:
        floor = 0
        for character in line:
            floor += direction.get(character, 0)
        print(floor)
