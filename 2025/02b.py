#!/usr/bin/env python3

import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = f.read()

ranges = data.split(',')
wrong_ids: set[int] = set()
for r in ranges:
    start_s, end_s = r.split('-')
    start = int(start_s)
    end = int(end_s)
    # print(start, end)
    # how long are our prefixes?
    id_lengths = range(len(start_s), len(end_s) + 1)
    for id_length in id_lengths:
        for prefix_length in range(1, (id_length // 2) + 1):
            if id_length % prefix_length > 0:
                continue
            repetitions = id_length // prefix_length
            if len(start_s) == id_length:
                prefix_start = int(start_s[:prefix_length])
            else:
                prefix_start = 10 ** (prefix_length - 1)
            if len(end_s) == id_length:
                prefix_end = int(end_s[:prefix_length])
            else:
                prefix_end = 10 ** prefix_length - 1
            for prefix in range(prefix_start, prefix_end + 1):
                test = int(str(prefix) * repetitions)
                if start <= test <= end:
                    # print(test)
                    wrong_ids.add(test)
print(sum(wrong_ids))
