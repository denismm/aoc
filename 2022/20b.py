#!/usr/bin/env python3
import sys
from typing import NamedTuple

DECRYPTION_KEY = 811589153

Entry = NamedTuple("Entry", [("order", int), ("value", int), ("move", int)])

filename = sys.argv[1]
with open(filename, "r") as f:
    values = [int(line) * DECRYPTION_KEY for line in f]
    move_mod = len(values) - 1
    data: list[Entry] = [Entry(i, value, value % move_mod) for i, value in enumerate(values)]

for _ in range(10):
    for i in range(len(data)):
        # find correct entry
        # move it
        entry = [x for x in data if x.order == i][0]
        index = data.index(entry)
        data.remove(entry)
        new_position = (index + entry.move) % len(data)
        data.insert(new_position, entry)
    # print([x.value for x in data])

origin_entry = [x for x in data if x.value == 0][0]
origin = data.index(origin_entry)
result = 0
for index in (1000, 2000, 3000):
    entry = data[(origin + index) % len(data)]
    coord = entry.value
    result += coord
print(result)
