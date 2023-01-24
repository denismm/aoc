#!/usr/bin/env python3
import sys

elf_count = int(sys.argv[1])

next_start = 0

answer = 0
exponent = 0

while elf_count > 1:
    answer += next_start * (2 ** exponent)
    exponent += 1
    new_count = (elf_count + (1 - next_start)) // 2
    next_start = (next_start + elf_count) % 2
    elf_count = new_count

print(answer + 1)
