#!/usr/bin/env python3
import sys

steps = int(sys.argv[1])

insertions = 2017

buffer: list[int] = [0]
position: int = 0

for i in range(1, insertions + 1):
    position = (position + steps) % len(buffer)
    position += 1
    buffer.insert(position, i)

print(buffer[position + 1])
