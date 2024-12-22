#!/usr/bin/env python3
import sys

filename: str = sys.argv[1]

towels: list[str] = []
patterns: list[str] = []

with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        if ',' in line:
            towels = line.split(', ')
        elif len(line):
            patterns.append(line)

ok_count: int = 0

doable: dict[str, bool] = {t: True for t in towels}
def check_pattern(pattern: str) -> bool:
    if pattern in doable:
        return doable[pattern]
    for t in towels:
        if pattern.startswith(t):
            if check_pattern(pattern.removeprefix(t)):
                doable[pattern] = True
                return True
    doable[pattern] = False
    return False

for pattern in patterns:
    if check_pattern(pattern):
        ok_count += 1

print(ok_count)
