#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    for line in f:
        numbers = list(line.strip())
        result = 0
        step = len(numbers) // 2
        for i in range(len(numbers)):
            if numbers[i] == numbers[i - step]:
                result += int(numbers[i])
        print(result)
