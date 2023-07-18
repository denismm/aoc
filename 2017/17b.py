#!/usr/bin/env python3
import sys

steps = int(sys.argv[1])

insertions = 50 * 1000 * 1000

position: int = 0

after_0 = 0

for i in range(1, insertions + 1):
    position = (position + steps) % i
    position += 1
    if position == 1:
        # print(f"after_0 set to {i}")
        after_0 = i

print(after_0)
