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
    for c in counts:
        top = max(c.values())
        bottom = min(c.values())
        for i, target in enumerate((top, bottom)):
            candidates = [k for k, v in c.items() if v == target]
            if len(candidates) != 1:
                raise ValueError(f"no single solution: {candidates}")
            answers[i].append(candidates[0])
    for answer in answers:
        print("".join(answer))
