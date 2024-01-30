#!/usr/bin/env python3
import sys

repetitions = int(sys.argv[1])
input = sys.argv[2]

output: list[str] = list(input)

for rep in range(repetitions):
    i = 0
    buffer: list[str] = []
    while i < len(output):
        # count similar
        repetend = output[i]
        j = 0
        while i + j < len(output) and output[i + j] == repetend:
            j += 1
        buffer.extend(list(str(j)))
        buffer.append(repetend)
        i += j
    output = buffer
if len(output) < 20:
    print(''.join(output))
print(len(output))
