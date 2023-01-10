#!/usr/bin/env python3
import sys
import math

disk_size = int(sys.argv[2])
seed_str = sys.argv[1]
seed = [int(c) for c in seed_str]

if len(seed) != 17:
    raise ValueError("bad seed")

disk_power = math.log2(disk_size / 17)
if disk_power != int(disk_power):
    raise ValueError(f"bad disk size {disk_size}")

iterations = int(disk_power)

checksum = list(seed)
checksum.append(0)

checksum_list: list[list[int]] = [checksum]

first_data = seed + [0] + [1 - x for x in reversed(seed)] + [0]
first_checksum = []
for i in range(0, len(first_data) - 1, 2):
    first_checksum.append(1 if first_data[i] == first_data[i+1] else 0)

checksum = first_checksum

checksum_list.append(checksum)

current_iteration = 1

while current_iteration < iterations:
    new_checksum = []
    for i in range(0, 18, 2):
        new_checksum.append(1 if checksum[i] == checksum[i+1] else 0)
    for i in range(0, 18, 2):
        new_checksum.append(1 if checksum[i] == checksum[i+1] else 0)
    new_checksum[13] = 1 - new_checksum[13]
    checksum = new_checksum
    if checksum in checksum_list:
        print(f"loop found at {current_iteration}")
    current_iteration += 1
    checksum_list.append(checksum)
    print(''.join([str(x) for x in checksum[:-1]]), current_iteration )

