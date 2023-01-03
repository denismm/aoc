#!/usr/bin/env python3
import sys

disk_size = int(sys.argv[2])
seed_str = sys.argv[1]
seed = [int(c) for c in seed_str]

data = list(seed)

while len(data) < disk_size:
    data = data + [0] + [1 - x for x in reversed(data)]

checksum = data[:disk_size]

while len(checksum) % 2 == 0:
    new_checksum = []
    for i in range(0, len(checksum), 2):
        new_checksum.append(1 if checksum[i] == checksum[i+1] else 0)
    checksum = new_checksum
print(''.join([str(x) for x in checksum]))

