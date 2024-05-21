#!/usr/bin/env python3
import sys
from collections import defaultdict

filename = sys.argv[1]

destination: str = ""
replacements: dict[str, list[str]] = defaultdict(list)
with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        if len(line):
            if ' => ' in line:
                source, dest = line.split(' => ')
                replacements[dest].append(source)
            else:
                destination = line

steps = 0
current = destination

def next_options(start: str) -> set[str]:
    outputs: set[str] = set()
    sources: list[tuple[int, str]] = []
    for source, dests in replacements.items():
        # print (source)
        position = 0
        found = True
        while found:
            position = start.find(source, position)
            if position == -1:
                found = False
                break
            sources.append((position, source))
            print(f"found {source} at {position}")
            for dest in dests:
                output = start[:position] + start[position:].replace(source, dest, 1)
                # print (f"{dest}: adding {output}")
                outputs.add(output)
            position += 1
    print(sorted(sources))
    return outputs

while current != 'e':
    nexts = next_options(current)
    # print(f"nexts: {len(nexts)}")
    if not nexts:
        print(f"no replacements at {current} after {steps=}")
        exit()
    next = nexts.pop()
    steps += 1
    current = next
    # print(current)

print(steps)
