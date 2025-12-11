#!/usr/bin/env python3

import sys
from collections import Counter

filename = sys.argv[1]

outputs: dict[str, list[str]] = {}

with open(filename, 'r') as f:
    for line in f:
        device, wires = line.split(':')
        destinations = wires.strip().split()
        outputs[device] = destinations

# I'm trusting there are no loops - heavily implied by the problem

flow: Counter[str] = Counter()

flow['you'] = 1

paths: int = 0

while flow:
    new_flow: Counter[str] = Counter()
    for location, count in flow.items():
        for dest in outputs[location]:
            new_flow[dest] += count
    flow = new_flow
    if 'out' in flow:
        paths += flow['out']
        del flow['out']

print(paths)
