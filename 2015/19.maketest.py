#!/usr/bin/env python3
import sys
from collections import defaultdict
import random

filename = sys.argv[1]
test_steps = int(sys.argv[2])

destination: str = ""
replacements: dict[str, list[str]] = defaultdict(list)
with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        if len(line):
            if " => " in line:
                source, dest = line.split(" => ")
                replacements[source].append(dest)
            else:
                destination = line


def next_options(start: str) -> set[str]:
    outputs: set[str] = set()
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
    return outputs

current = 'e'
for _ in range(test_steps):
    options = next_options(current)
    current = random.choice(list(options))

for source, dests in replacements.items():
    for dest in dests:
        print(f"{source} => {dest}")
print()
print(current)
