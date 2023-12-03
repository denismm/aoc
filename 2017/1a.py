#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    for line in f:
        numbers = list(line.strip())
        result = 0
        for i in range(len(numbers)):
            if numbers[i] == numbers[i - 1]:
                result += int(numbers[i])
        print(result)
