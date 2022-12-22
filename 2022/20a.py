#!/usr/bin/env python3
import sys

data: list[tuple[int, int]]
filename = sys.argv[1]
with open(filename, "r") as f:
    data = list(enumerate([int(line) for line in f]))

for i in range(len(data)):
    # find correct entry
    # move it
    entry = [x for x in data if x[0] == i][0]
    index = data.index(entry)
    data.remove(entry)
    new_position = (index + entry[1]) % len(data)
    data.insert(new_position, entry)

origin_entry = [x for x in data if x[1] == 0][0]
origin = data.index(origin_entry)
result = 0
for index in (1000, 2000, 3000):
    entry = data[(origin + index) % len(data)]
    coord = entry[1]
    result += coord
print(result)
