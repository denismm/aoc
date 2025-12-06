#!/usr/bin/env python3

import sys
from math import prod
filename = sys.argv[1]

data: list[str] = []
operations: list[str] = []

with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        if len(data) == 0:
            data = list(line)
        elif '+' in line:
            operations = line.split()
        else:
            for i, character in enumerate(line):
                if i >= len(data):
                    data.append(character)
                else:
                    data[i] += character
numbers: list[list[int]] = []
operands: list[int] = []
for element in data:
    element = element.strip()
    if len(element) > 0:
        operands.append(int(element))
    else:
        numbers.append(operands)
        operands = []
if len(operands) > 0:
    numbers.append(operands)

total = 0
for operation, operands in zip(operations, numbers):
    if operation == '+':
        result = sum(operands)
    else:
        result = prod(operands)
    total += result
print(total)
