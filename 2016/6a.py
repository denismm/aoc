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
    answer = []
    for c in counts:
        top = max(c.values())
        tops = [k for k, v in c.items() if v == top]
        if len(tops) != 1:
            raise ValueError(f"no single top: {tops}")
        answer.append(tops[0])
    print("".join(answer))
