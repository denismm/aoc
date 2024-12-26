#!/usr/bin/env python3
import sys
from tqdm import tqdm
from collections import Counter

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

sequence_map: Counter[tuple[int, ...]] = Counter()

for initial in tqdm(initials):
    number = initial
    local_map: dict[tuple[int, ...], int] = {}
    last_price: int = number % 10
    current_sequence: list[int] = []

    for _ in range(iterations):
        number = prune(mix(number, number * 64))
        number = prune(mix(number, number // 32))
        number = prune(mix(number, number * 2048))
        new_price = number % 10
        current_sequence.append(new_price - last_price)
        if len(current_sequence) == 4:
            key = tuple(current_sequence)
            if key not in local_map:
                local_map[key] = new_price
            current_sequence.pop(0)
        last_price = new_price
    final_sum += number
    for sequence, profit in local_map.items():
        sequence_map[sequence] += profit
print(final_sum)
top_value = max(sequence_map.values())
print(top_value)
print([k for k, v in sequence_map.items() if v == top_value])
