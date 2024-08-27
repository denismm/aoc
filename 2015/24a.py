#!/usr/bin/env python3
import sys
from itertools import combinations
from typing import Optional

filename = sys.argv[1]

with open(filename, "r") as f:
    packages: list[int] = [int(line) for line in f]

total = sum(packages)
if total % 3 != 0:
    raise ValueError(f"indivisible sum {total}")
subtotal = total // 3

# three groups of equal sum
# first preference: by number of packages in first group
# second pref: by product of first group
# we _do not_ care about the second and third beyond being same-weight

def qe(packages: tuple[int, ...]) -> int:
    product = 1
    for p in packages:
        product *= p
    return product

for package_count in range(1, len(packages) // 3):
    best_qe: Optional[int] = None
    best_combo: Optional[tuple[int,...]] = None
    for combo in combinations(packages, package_count):
        if sum(combo) != subtotal:
            continue
        # print(f"got {subtotal=} {combo=}")
        remainder = [p for p in packages if p not in combo]
        found_second = False
        for second_count in range(1, len(packages) // 2):
            for second_combo in combinations(remainder, second_count):
                if sum(second_combo) == subtotal:
                    found_second = True
                    # print(f"{second_combo} works")
                    break
            if found_second:
                break
        if not found_second:
            continue
        # print("valid")
        # this is a valid first-combo
        combo_qe = qe(combo)
        if best_qe is None or combo_qe < best_qe:
            best_qe = combo_qe
            best_combo = combo
    if best_qe:
        print(f"Best QE is {best_qe} ({best_combo})")
        exit(0)
print ("no good options found")
