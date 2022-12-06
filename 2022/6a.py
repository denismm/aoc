#!/usr/bin/env python3
import sys

marker_size = 14

filename = sys.argv[1]
with open(filename, "r") as f:
    for line in f:
        for i in range(len(line)):
            letters:set[str] = set(line[i:i+marker_size])
            if len(letters) == marker_size:
                print(i+marker_size)
                break
