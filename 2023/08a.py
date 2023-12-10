#!/usr/bin/env python3
import sys
import re

route: list[int] = []
map: dict[str, tuple[str, str]] = {}
node_re = re.compile(r'(\w+) = \((\w+), (\w+)\)')
direction_for_letter = {'L': 0, 'R': 1}

filename = sys.argv[1]
with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        if route == []:
            route = [direction_for_letter[c] for c in line]
        elif line == "":
            continue
        else:
            m = node_re.match(line)
            if m:
                location, left, right = m.groups()
                map[location] = (left, right)
            else:
                raise ValueError(f"couldn't parse line {line}")

route_len = len(route)
steps = 0       # this is 0-based but 1 gets added at the end of the loop
location = 'AAA'

while location != 'ZZZ':
    direction = route[steps % route_len]
    location = map[location][direction]
    steps += 1
print(steps)
