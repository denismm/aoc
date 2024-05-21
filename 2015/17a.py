#!/usr/bin/env python3
import sys
from collections import Counter
import math

filename = sys.argv[1]
target_amount = int(sys.argv[2])

containers: Counter[int] = Counter()

with open(filename, "r") as f:
    for line in f:
        container_size = int(line)
        containers[container_size] += 1

size_list = sorted(containers.keys())


def combos(start_i: int, capacity_so_far: int) -> int:
    # print(f"{start_i=} {capacity_so_far=}")
    if start_i >= len(size_list):
        return 0
    result: int = 0
    next_size = size_list[start_i]
    available = containers[next_size]
    for count in range(available + 1):
        multiplier = math.comb(available, count)
        next_capacity = capacity_so_far + count * next_size
        # print(f"{next_size=}: {count} / {available} ({multiplier}) {next_capacity=}")
        if next_capacity == target_amount:
            subresult = 1
        elif next_capacity < target_amount:
            subresult = combos(start_i + 1, next_capacity)
            # print(f"returned {subresult}")
        else:
            break
        result += multiplier * subresult
        # print (f"{multiplier=} {subresult=} {result=}")
    return result


print(combos(0, 0))
