#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    checksum = 0
    for line in f:
        numbers = [int(x) for x in line.strip().split()]
        checksum += max(numbers) - min(numbers)
    print(checksum)
