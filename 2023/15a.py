#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        total = 0
        for substring in line.split(','):
            hash = 0
            for char in substring:
                hash += ord(char)
                hash *= 17
                hash %= 256
            total += hash
        print(total)
