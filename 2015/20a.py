#!/usr/bin/env python3
import sys
from math import sqrt, ceil

present_target = int(sys.argv[1])


def find_factors(n: int) -> set[int]:
    all_factors: set[int] = set()
    # lazy for now
    candidate: int = 0
    max = ceil(sqrt(n))
    while candidate <= max:
        candidate += 1
        if n % candidate == 0:
            all_factors.add(candidate)
            all_factors.add(n // candidate)
    return all_factors


n = 1
report = 10
while True:
    all_factors = find_factors(n)
    present_count = sum([elf * 10 for elf in all_factors])
    # print(f"house {n} gets {present_count} presents")
    if present_count >= present_target:
        print(f"answer is {n}")
        exit(0)
    n += 1
    if n % report == 0:
        print(f"nothing found at {n}")
        report *= 10
