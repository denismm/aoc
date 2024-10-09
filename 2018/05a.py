#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, "r") as f:
    polymer = f.read().rstrip()

reactions = -1
while reactions != 0:
    reactions = 0
    for i in range(len(polymer)):
        j = i + 1
        if j >= len(polymer):
            break
        if polymer[i].upper() == polymer[j].upper() and polymer[i] != polymer[j]:
            unit = polymer[i] + polymer[j]
            polymer = polymer.replace(unit, '')
            reactions += 1

print(len(polymer))
