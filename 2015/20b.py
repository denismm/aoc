#!/usr/bin/env python3
import sys
from math import sqrt, ceil

present_target = int(sys.argv[1])

def find_elves(n: int) -> set[int]:
    all_elves: set[int] = set()
    # lazy for now
    candidate: int = 0
    max = min([ceil(sqrt(n)), 50])
    while candidate <= max:
        candidate += 1
        if n % candidate == 0:
            if n // candidate <= 50:
                all_elves.add(candidate)
            if candidate <= 50:
                all_elves.add(n // candidate)
    return all_elves

n = 1
report = 10
while True:
    all_elves = find_elves(n)
    present_count = sum([elf * 11 for elf in all_elves])
    # print(f"house {n} gets {present_count} presents")
    if present_count >= present_target:
        print(f"answer is {n}")
        exit(0)
    if n % report == 0:
        print(f"house {n} gets {present_count} presents")
        report *= 10
    n += 1
