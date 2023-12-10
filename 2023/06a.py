#!/usr/bin/env python3
import sys
from functools import reduce

filename = sys.argv[1]
data: list[list[int]] = []
with open(filename, 'r') as f:
    for line in f:
        tag, nums = line.split(':')
        data.append([int(s) for s in nums.split()])
races: list[tuple[int, int]] = list(zip(data[0], data[1]))

options: list[int] = []
for race in races:
    r_time, r_distance = race
    choices = 0
    for i in range(1, r_time):
        if i * (r_time - i) > r_distance:
            choices += 1
    options.append(choices)


print(reduce(lambda x, y: x*y, options))
