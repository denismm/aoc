#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    checksum = 0
    for line in f:
        numbers = [int(x) for x in line.strip().split()]
        for m in numbers:
            for n in numbers:
                if m != n and m % n == 0:
                    checksum += m // n
    print(checksum)
