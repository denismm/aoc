#!/usr/bin/env python3
import sys

filename = sys.argv[1]

seen: set[tuple[str, ...]] = set()

with open(filename, "r") as f:
    for line in f:
        key = line.rstrip()
        for i in range(len(key)):
            pattern = list(key)
            pattern[i] = ""
            if tuple(pattern) in seen:
                print("".join(pattern))
                exit(0)
            seen.add(tuple(pattern))
