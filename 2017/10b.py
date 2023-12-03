#!/usr/bin/env python3
import sys
import functools

filename = sys.argv[1]

loop_len = 256
# open as bytes
with open(filename, 'rb') as f:
    for line in f:
        numbers = list(range(loop_len))
        input = line.rstrip()
        lengths = list(input) + [17, 31, 73, 47, 23]

        position = 0
        skip_size = 0

        for iteration in range(64):
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
        # numbers is sparse hash
        dense = []
        for i in range(16):
            block = numbers[i * 16: (i+1) * 16]
            dense.append(functools.reduce(lambda a, b: a ^ b, block))
        output = (''.join(["{:02x}".format(x) for x in dense]))
        print(input, " -> ", output)
