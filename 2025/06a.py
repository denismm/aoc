#!/usr/bin/env python3

import sys
from math import prod
filename = sys.argv[1]

data: list[list[int]] = []
operations: list[str] = []

with open(filename, 'r') as f:
    for line in f:
        elements = line.split()
        if elements[0].isnumeric():
            data.append([int(s) for s in elements])
        else:
            operations = elements
total = 0
result: int
for i, operation in enumerate(operations):
    if operation == '+':
        result = sum([elements[i] for elements in data])
    else:
        result = prod([elements[i] for elements in data])
    total += result
print(total)
