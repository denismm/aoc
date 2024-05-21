#!/usr/bin/env python3
import sys
import re
from positions import Position
from collections import defaultdict

instruction_re = re.compile(r"([\w ]*) (\d+),(\d+) through (\d+),(\d+)")

filename = sys.argv[1]
lights: dict[Position, int] = defaultdict(lambda: 0)
with open(filename, "r") as f:
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
                if command == "turn on":
                    lights[point] += 1
                elif command == "toggle":
                    lights[point] += 2
                elif command == "turn off":
                    if lights[point]:
                        lights[point] -= 1
                else:
                    raise ValueError(f"bad command {command}")
print(sum(lights.values()))
