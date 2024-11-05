#!/usr/bin/env python3
import sys
from collections import defaultdict

filename = sys.argv[1]

next_steps: dict[str, set[str]] = defaultdict(set)
all_steps: set[str] = set()
with open(filename, "r") as f:
    for line in f:
        tokens = line.split()
        prereq = tokens[1]
        postreq = tokens[7]
        next_steps[prereq].add(postreq)
        all_steps.add(prereq)
        all_steps.add(postreq)

order: list[str] = []

while(all_steps):
    options = set(all_steps)
    for v in next_steps.values():
        options -= v
    if not options:
        raise ValueError("no options")
    step = sorted(options)[0]
    order.append(step)
    all_steps.remove(step)
    try:
        del next_steps[step]
    except KeyError:
        pass

print(''.join(order))
