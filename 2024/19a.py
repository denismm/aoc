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
option_total: int = 0

doable: dict[str, int] = {"": 1}
def check_pattern(pattern: str) -> int:
    if pattern in doable:
        return doable[pattern]
    options: int = 0
    for t in towels:
        if pattern.startswith(t):
            options += check_pattern(pattern.removeprefix(t))
    doable[pattern] = options
    return options

for pattern in patterns:
    options = check_pattern(pattern)
    if options:
        ok_count += 1
    option_total += options


print(ok_count)
print(option_total)
