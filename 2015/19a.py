#!/usr/bin/env python3
import sys
from collections import defaultdict

filename = sys.argv[1]

start: str = ""
replacements: dict[str, list[str]] = defaultdict(list)
with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        if len(line):
            if " => " in line:
                source, dest = line.split(" => ")
                replacements[source].append(dest)
            else:
                start = line

outputs: set[str] = set()
# print(start)

for source, dests in replacements.items():
    # print (source)
    position = 0
    found = True
    while found:
        position = start.find(source, position)
        if position == -1:
            found = False
            break
        # print(f"found {source} at {position}")
        for dest in dests:
            output = start[:position] + start[position:].replace(source, dest, 1)
            # print (f"{dest}: adding {output}")
            outputs.add(output)
        position += 1
# print(outputs)
print(len(outputs))
