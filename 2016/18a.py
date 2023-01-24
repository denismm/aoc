#!/usr/bin/env python3
import sys

row_count = int(sys.argv[1])

with open(sys.argv[2], 'r') as f:
    seed = f.read().rstrip()

row: list[bool] = [True if c == '^' else False for c in seed]

safe_count = 0

for _ in range(row_count):
    # print(''.join(['^' if x else '.' for x in row]))
    safe_count += sum([0 if x else 1 for x in row])
    calc_row = [False] + row + [False]
    row = [calc_row[i] ^ calc_row[i+2] for i in range(len(row))]

print(safe_count)
