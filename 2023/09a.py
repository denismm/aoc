#!/usr/bin/env python3
import sys

end_total = 0
start_total = 0
filename = sys.argv[1]
with open(filename, 'r') as f:
    for line in f:
        data_rows: list[list[int]] = []
        data_rows.append([int(s) for s in line.split()])
        while set(data_rows[-1]) != {0}:
            data_rows.append([y - x for x, y in zip(data_rows[-1], data_rows[-1][1:])])
        while len(data_rows) > 1:
            speed_row = data_rows.pop()
            last_row = data_rows[-1]
            last_row.append(last_row[-1] + speed_row[-1])
            last_row.insert(0, last_row[0] - speed_row[0])
        end_total += last_row[-1]
        start_total += last_row[0]

print(f"start is {start_total}, end is {end_total}")
