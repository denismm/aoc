#!/usr/bin/env python3
import sys
from collections import Counter
from typing import Optional
import math
filename = sys.argv[1]
target_amount = int(sys.argv[2])

containers: Counter[int] = Counter()

with open(filename, 'r') as f:
    for line in f:
        container_size = int(line)
        containers[container_size] += 1

size_list = sorted(containers.keys())

def min_combos(start_i: int, capacity_so_far: int) -> Optional[int]:
    if start_i >= len(size_list):
        return None
    result: Optional[int] = None
    next_size = size_list[start_i]
    available = containers[next_size]
    subresult: Optional[int]
    for count in range(available + 1):
        next_capacity = capacity_so_far + count * next_size
        if next_capacity == target_amount:
            subresult = 0
        elif next_capacity < target_amount:
            subresult = min_combos(start_i + 1, next_capacity)
        else:
            break
        if subresult is not None:
            new_result = count + subresult
            if result is None or new_result < result:
                result = new_result
    return result

min_count = int(min_combos(0, 0))       # type: ignore [arg-type]

def combos(start_i: int, capacity_so_far: int, count_limit: int) -> int:
    # print(f"{start_i=} {capacity_so_far=}")
    if start_i >= len(size_list):
        return 0
    result: int = 0
    next_size = size_list[start_i]
    available = containers[next_size]
    for count in range(available + 1):
        if count > count_limit:
            break
        multiplier = math.comb(available, count)
        next_capacity = capacity_so_far + count * next_size
        # print(f"{next_size=}: {count} / {available} ({multiplier}) {next_capacity=}")
        if next_capacity == target_amount:
            if count == count_limit:
                subresult = 1
            else:
                subresult = 0
        elif next_capacity < target_amount:
            if count < count_limit:
                subresult = combos(start_i + 1, next_capacity, count_limit - count)
            else:
                subresult = 0
            # print(f"returned {subresult}")
        else:
            break
        result += multiplier * subresult
        # print (f"{multiplier=} {subresult=} {result=}")
    return result

print(combos(0, 0, min_count))
