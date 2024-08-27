#!/usr/bin/env python3
import sys
from itertools import combinations
from typing import Optional

filename = sys.argv[1]

with open(filename, "r") as f:
    packages: list[int] = [int(line) for line in f]

total = sum(packages)
if total % 4 != 0:
    raise ValueError(f"indivisible sum {total}")
subtotal = total // 4

# four groups of equal sum
# first preference: by number of packages in first group
# second pref: by product of first group
# we _do not_ care about the rest beyond being same-weight

def qe(packages: tuple[int, ...]) -> int:
    product = 1
    for p in packages:
        product *= p
    return product

def validate_combo(packages: list[int], groups: int) -> bool:
    if groups == 1:
        return True
    for package_count in range(1, len(packages) // groups + 1):
        for combo in combinations(packages, package_count):
            if sum(combo) != subtotal:
                continue
            remainder = [p for p in packages if p not in combo]
            if validate_combo(remainder, groups - 1):
                return True
    return False


for package_count in range(1, len(packages) // 4 + 1):
    best_qe: Optional[int] = None
    best_combo: Optional[tuple[int,...]] = None
    for combo in combinations(packages, package_count):
        # print(f"{combo}: {sum(combo)}")
        if sum(combo) != subtotal:
            continue
        # print(f"got {subtotal=} {combo=}")
        remainder = [p for p in packages if p not in combo]
        if not validate_combo(remainder, 3):
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
