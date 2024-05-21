#!/usr/bin/env python3
import sys
import re

filename = sys.argv[1]

rep_total = 0
memory_total = 0
expanded_total = 0
with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        orig = line
        rep_total += len(line)
        line = line[1:-1]
        line = line.replace(r"\\", "\\")
        line = line.replace(r"\"", r'"')
        line = re.sub(r"\\x[0-9a-f][0-9a-f]", ".", line)
        # print(f"{orig}:->:{line}")
        memory_total += len(line)
        expanded = orig
        expanded = expanded.replace("\\", r"..")
        expanded = expanded.replace(r'"', r"..")
        expanded_total += len(expanded) + 2
        # print(f"{orig}:->:{expanded}")
print(rep_total - memory_total)
print(expanded_total - rep_total)
