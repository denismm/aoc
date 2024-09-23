#!/usr/bin/env python3
import sys
from collections import Counter

filename = sys.argv[1]

twos: int = 0
threes: int = 0

with open(filename, "r") as f:
    for line in f:
        counts: Counter[str] = Counter(line.rstrip())
        values = counts.values()
        if 2 in values:
            twos += 1
        if 3 in values:
            threes += 1
print(f"{twos} * {threes} = {twos * threes}")
