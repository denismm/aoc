#!/usr/bin/env python3
import sys
from typing import Optional
from itertools import combinations
filename = sys.argv[1]

safe_count = 0
def check_levels(levels: list[int]) -> bool:
    direction = 0
    prev: Optional[int] = None
    for level in levels:
        if prev is not None:
            step = level - prev
            if step == 0:
                return False
            if abs(step) > 3:
                return False
            if direction == 0:
                direction = step
            elif direction * step < 0:
                return False
        prev = level
    return True

with open(filename, 'r') as f:
    for line in f:
        levels = [int(s) for s in line.split()]
        for sublevels in combinations(levels, len(levels) - 1):
            if check_levels(sublevels):
                safe_count += 1
                break
print(safe_count)