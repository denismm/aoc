#!/usr/bin/env python3
import sys
import re
filename = sys.argv[1]

total = 0
mul_re = re.compile(r'mul\((\d+),(\d+)\)')
with open(filename, 'r') as f:
    for line in f:
        for m in mul_re.finditer(line):
            args = [int(s) for s in m.groups()]
            total += args[0] * args[1]
print(total)
