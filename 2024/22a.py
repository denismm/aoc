#!/usr/bin/env python3
import sys
from tqdm import tqdm

iterations = 2000

filename = sys.argv[1]
initials: list[int] = []
with open(filename, "r") as f:
    for line in f:
        initials.append(int(line.rstrip()))

def mix(a: int, b: int) -> int:
    return a ^ b

def prune(a: int) -> int:
    return a % 16777216

final_sum: int = 0

for initial in tqdm(initials):
    number = initial
    for _ in range(iterations):
        number = prune(mix(number, number * 64))
        number = prune(mix(number, number // 32))
        number = prune(mix(number, number * 2048))
    final_sum += number
print(final_sum)
