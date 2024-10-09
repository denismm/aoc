#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, "r") as f:
    base_polymer = f.read().rstrip()

def react_polymer(polymer: str) -> int:
    i = 0
    while i < len(polymer):
        j = i + 1
        if j >= len(polymer):
            break
        if polymer[i].upper() == polymer[j].upper() and polymer[i] != polymer[j]:
            unit = polymer[i] + polymer[j]
            polymer = polymer.replace(unit, '')
            i = max( 0, i - 1)
        else:
            i += 1
    return len(polymer)

unit_types: set[str] = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

best_len = react_polymer(base_polymer)
best_unit = ""
for unit in unit_types:
    new_polymer = base_polymer.replace(unit, "").replace(unit.lower(), "")
    new_len = react_polymer(new_polymer)
    if new_len < best_len:
        best_len = new_len
        best_unit = unit

print(best_unit, best_len)
