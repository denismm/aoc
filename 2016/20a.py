#!/usr/bin/env python3
import sys

filename = sys.argv[1]

MAX = 4294967295 + 1

# list of start and end points
blocked: list[int] = []

def combine_range(old: list[int], new: list[int]) -> list[int]:
    result: list[int] = []
    old_i = 0
    # add everything before start
    while old_i < len(old) and old[old_i] < new[0]:
        result.append(old[old_i])
        old_i += 1
    if old_i % 2 == 0:
        # even, add an entrance
        result.append(new[0])
    # skip over everything inside
    while old_i < len(old) and old[old_i] <= new[1]:
        old_i += 1
    if old_i % 2 == 0:
        # even, add an exit
        result.append(new[1])
    result += old[old_i:]
    return result

with open(filename, 'r') as f:
    for line in f:
        start, end = line.rstrip().split('-')
        first_banned = int(start)
        first_open = int(end) + 1
        if len(blocked) == 0:
            blocked = [first_banned, first_open]
        else:
            blocked = combine_range(blocked, [first_banned, first_open])
        # print(blocked)
if blocked[0] != 0:
    print(0)
else:
    print(blocked[1])

total = blocked[0]
for i in range(1, len(blocked) - 2, 2):
    total += blocked[i+1] - blocked[i]
total += MAX - blocked[-1]
print(total)
