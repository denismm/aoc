#!/usr/bin/env python3
import sys
import re
filename = sys.argv[1]

total = 0
statement_re = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)")
enabled = True
with open(filename, 'r') as f:
    for line in f:
        for m in statement_re.finditer(line):
            if m.group(0) == 'do()':
                enabled = True
            elif m.group(0) == "don't()":
                enabled = False
            elif enabled:
                args = [int(s) for s in m.groups()]
                total += args[0] * args[1]
print(total)
