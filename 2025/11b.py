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

# state int: +1 if seen dac, +2 if seen fft
adds: dict[str, int] = {'dac': 1, 'fft': 2}
State = tuple[str, int]

flow: Counter[State] = Counter()

flow[('svr', 0)] = 1

paths: int = 0

while flow:
    new_flow: Counter[State] = Counter()
    for state, count in flow.items():
        location, seen = state
        for dest in outputs[location]:
            new_seen = seen
            new_seen += adds.get(location, 0)
            new_flow[(dest, new_seen)] += count
    flow = new_flow
    for seen in range(4):
        outstate = ('out', seen)
        if outstate in flow:
            if seen == 3:
                paths += flow[outstate]
            del flow[outstate]

print(paths)
