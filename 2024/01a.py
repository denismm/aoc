#!/usr/bin/env python3
import sys
filename = sys.argv[1]
from collections import Counter

left: list[int] = []
right: list[int] = []
left_counter: Counter[int] = Counter()
right_counter: Counter[int] = Counter()

with open(filename, 'r') as f:
    for line in f:
        (l_in, r_in) = line.split()
        l = int(l_in)
        r = int(r_in)
        left.append(l)
        right.append(r)
        left_counter[l] += 1
        right_counter[r] += 1

left.sort()
right.sort()
total_dist = 0
for (l, r) in zip(left, right):
    total_dist += abs(l-r)
print(total_dist)

similarity = 0
for (n, l_count) in left_counter.items():
    r_count = right_counter[n]
    similarity += n * l_count * r_count
print(similarity)
