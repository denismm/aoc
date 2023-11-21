#!/usr/bin/env python3
import sys
import re
from positions import Position

instruction_re = re.compile(r'([\w ]*) (\d+),(\d+) through (\d+),(\d+)')

filename = sys.argv[1]
lit: set[Position] = set()
with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        m = instruction_re.match(line)
        if not m:
            raise ValueError(f"can't parse line {line}")

        command, *string_nums = m.groups()
        minx, miny, maxx, maxy = (int(s) for s in (string_nums))

        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                point = (x, y)
                if command == 'turn on':
                    lit.add(point)
                elif command == 'turn off':
                    lit.discard(point)
                elif command == 'toggle':
                    if point in lit:
                        lit.discard(point)
                    else:
                        lit.add(point)
                else:
                    raise ValueError(f"bad command {command}")
print(len(lit))
