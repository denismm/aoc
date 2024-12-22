#!/usr/bin/env python3
import sys

filename = sys.argv[1]

target: list[int] = []
with open(filename, "r") as f:
    for line in f:
        if line.startswith('Program'):
            program_s = line.split()[-1]
            target = [int(s) for s in program_s.split(',')]

target.reverse()

input_values: list[int] = [0]

debug_log: list[str] = []

def process_section(input_value: int, new: int) -> int:
    debug_log.clear()
    a = input_value * 8 + new
    b = new
    debug_log.append(f"{a=} {b=}")
    b ^= 3
    c = (a >> b) % 8
    debug_log.append(f"mask and shift {b=} {c=}")
    b ^= 5
    debug_log.append(f"mask {b=}")
    b ^= c
    debug_log.append(f"mask by {c}: {b=}")
    return b

def find_num(input_value: int, t: int) -> list[int]:
    options: list[int] = []
    for new in range(8):
        if process_section(input_value, new) == t:
            # print(', '.join(debug_log))
            options.append(new)
    return options

for t in target:
    new_input_values: list[int] = []
    for input_value in input_values:
        options = find_num(input_value, t)
        for new in options:
            new_input_values.append(input_value * 8 + new)
    input_values = new_input_values

print(input_values)
print(min(input_values))
