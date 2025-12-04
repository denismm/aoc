#!/usr/bin/env python3

import sys
from math import ceil, floor

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = f.read()

ranges = data.split(',')
total = 0
for r in ranges:
    start_s, end_s = r.split('-')
    start = int(start_s)
    end = int(end_s)
    # print(start, end)
    # how long are our prefixes?
    prefix_lengths = range(ceil(len(start_s) / 2), (floor(len(end_s) / 2) + 1))
    for prefix_length in prefix_lengths:
        if len(start_s) == prefix_length * 2:
            prefix_start = int(start_s[:prefix_length])
        else:
            prefix_start = 10 ** (prefix_length - 1)
        if len(end_s) == prefix_length * 2:
            prefix_end = int(end_s[:prefix_length])
        else:
            prefix_end = 10 ** prefix_length - 1
        multiplier = 10 ** prefix_length + 1
        for prefix in range(prefix_start, prefix_end + 1):
            test = prefix * multiplier
            if start <= test <= end:
                # print(test)
                total += test
print(total)
