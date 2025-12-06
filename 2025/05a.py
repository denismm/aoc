#!/usr/bin/env python3

import sys
filename = sys.argv[1]

Range = tuple[int, int]
ing_ranges: list[Range] = []
fresh = 0
with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        if '-' in line:
            points = line.split('-')
            ing_ranges.append((int(points[0]), int(points[1])))
        elif len(line):
            ingredient = int(line)
            for start, end in ing_ranges:
                if start <= ingredient <= end:
                    fresh += 1
                    break
print(fresh)

# part 2 - merge the ranges
ing_ranges.sort()
# print(ing_ranges)
true_ranges: list[Range] = [ing_ranges[0]]
for start, end in ing_ranges[1:]:
    true_range = true_ranges[-1]
    # print(f"{true_range=} {start=} {end=}")
    if true_range[0] <= start <= true_range[1]:
        # overlap or capture?
        if true_range[0] <= end <= true_range[1]:
            # fully captured
            # print("capture")
            continue
        else:
            # overlap
            # print("overlap")
            true_ranges[-1] = (true_range[0], end)
    else:
        # print("separate")
        true_ranges.append((start, end))

# print(true_ranges)
all_fresh = 0
for start, end in true_ranges:
    all_fresh += (end - start) + 1
print(all_fresh)
