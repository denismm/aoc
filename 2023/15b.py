#!/usr/bin/env python3
import sys
import re
from collections import defaultdict

filename = sys.argv[1]

def hash(label: str) -> int:
    val = 0
    for char in label:
        val += ord(char)
        val *= 17
        val %= 256
    return val

# I think I can rely on python3's sorted dictionaries here
boxes: dict[int, dict[str, int]] = defaultdict(dict)
instruction_re = re.compile(r'(\w+)([\-\=])(\d*)$')
with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        total = 0
        for instruction in line.split(','):
            m = instruction_re.match(instruction)
            if not m:
                raise ValueError(f"unparseable instruction {instruction}")
            (label, command, focus) = m.groups()
            box = hash(label)
            if command == '-':
                if label in boxes[box]:
                    del boxes[box][label]
            elif command == '=':
                boxes[box][label] = int(focus)
power = 0
for box, lenses in boxes.items():
    for i, (label, focal_power) in enumerate(lenses.items(), start=1):
        power += (box + 1) * i * focal_power
print(power)
