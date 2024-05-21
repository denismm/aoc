#!/usr/bin/env python3
import sys
from collections import defaultdict

filename = sys.argv[1]

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

steps = 0
frontier: set[str] = {"e"}
seen: set[str] = {"e"}


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
                if output not in seen:
                    outputs.add(output)
            position += 1
    return outputs


while destination not in frontier:
    print(f"round {steps}: {len(frontier)}")
    new_frontier: set[str] = set()
    for start in frontier:
        nexts = next_options(start)
        # print (f"{start} -> {nexts}")
        new_frontier |= nexts
        seen |= nexts
    frontier = new_frontier
    steps += 1
    # print (f"{destination} in {frontier}? {destination in frontier}")

print(steps)
