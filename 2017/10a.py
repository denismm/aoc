#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    lines = f.read().split('\n')
    loop_len = int(lines[0].rstrip())
    lengths = [int(x) for x in lines[1].rstrip().split(',')]

numbers = list(range(loop_len))
position = 0
skip_size = 0

for length in lengths:
    # reverse from position to position+length
    end_reverse = (position + length) % loop_len
    if end_reverse > position:
        swap = numbers[position:end_reverse]
    else:
        swap = numbers[position:] + numbers[:end_reverse]
    for i, p in enumerate(range(position, position + length)):
        numbers[p % loop_len] = swap[length - 1 - i]
    # move
    position = (position + length + skip_size) % loop_len
    # increase
    skip_size += 1
    # print(numbers)

print(numbers[0] * numbers[1])
