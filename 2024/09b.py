#!/usr/bin/env python3
import sys
from typing import Optional
from dataclasses import dataclass
from tqdm import tqdm
filename = sys.argv[1]

with open(filename, "r") as f:
    compressed_diskmap = f.read().rstrip()

@dataclass
class Entry:
    block: Optional[int]
    count: int

    def __repr__(self) -> str:
        return f"[{self.block} x {self.count}]"

diskmap: list[Entry] = []

for i, count_s in enumerate(compressed_diskmap):
    count = int(count_s)
    if i % 2 == 0:
        entry = Entry(i // 2, count)
    else:
        entry = Entry(None, count)
    if count > 0:
        diskmap.append(entry)
max_block = i // 2

print(len(diskmap))

for block in tqdm(range(max_block, 0, -1)):   # we don't need to move 0
    location, entry = [(i, entry) for i, entry in enumerate(diskmap) if entry.block == block][0]
    for space_loc, space in enumerate(diskmap):
        if space.block is not None:
            continue
        if space.count < entry.count:
            continue
        if space_loc > location:
            break
        # ok to move
        diskmap[location] = Entry(None, entry.count)
        insertion = [entry]
        if entry.count < space.count:
            insertion.append(Entry(None, space.count - entry.count))
        diskmap[space_loc : space_loc + 1] = insertion
        break

checksum = 0
position = 0
for entry in diskmap:
    if entry.block is not None:
        for i in range(entry.count):
            checksum += entry.block * (i + position)
    position += entry.count

print(checksum)
