#!/usr/bin/env python3
import sys

filename = sys.argv[1]
with open(filename, "r") as f:
    # start with an elf
    cal_for_elf: list[int] = [0]
    for line in f:
        entry: str = line.rstrip()
        if len(entry) == 0:
            # next elf
            cal_for_elf.append(0)
        else:
            calories: int = int(entry)
            cal_for_elf[-1] += calories
    sorted_elves = sorted(cal_for_elf)
    print(sum(sorted_elves[-3:]))
