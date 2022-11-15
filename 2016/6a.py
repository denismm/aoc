#!/usr/bin/env python3
import sys
import collections

filename = sys.argv[1]
with open(filename, "r") as f:
    counts = []
    for line in f:
        for (i, letter) in enumerate(line.rstrip()):
            if len(counts) <= i:
                counts.append(collections.defaultdict(lambda: 0))
            counts[i][letter] += 1
    answers = [[],[]]
    operators = (max, min)
    for c in counts:
        for i in range(2):
            target = operators[i](c.values())
            candidates = [k for k, v in c.items() if v == target]
            if len(candidates) != 1:
                raise ValueError(f"no single solution: {candidates}")
            answers[i].append(candidates[0])
    for answer in answers:
        print("".join(answer))
