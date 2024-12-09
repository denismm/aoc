#!/usr/bin/env python3
import sys
from typing import Optional
filename = sys.argv[1]

with open(filename, "r") as f:
    compressed_diskmap = f.read().rstrip()

diskmap: list[Optional[int]] = []

for i, count_s in enumerate(compressed_diskmap):
    count = int(count_s)
    if i % 2 == 0:
        diskmap += [i // 2] * count
    else:
        diskmap += [None] * count

print(len(diskmap))

# naive compression

while True:
    try:
        dest = diskmap.index(None)
        while True:
            block = diskmap.pop()
            if block:
                break
        try:
            diskmap[dest] = block
        except IndexError:
            diskmap.append(block)
            break
    except ValueError:
        break

checksum = 0
for i, block in enumerate(diskmap):
    assert block is not None
    checksum += i * block

print(checksum)
