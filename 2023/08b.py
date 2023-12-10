#!/usr/bin/env python3
import sys
import re
from typing import Optional
from dataclasses import dataclass

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

StageLocation = tuple[int, str]
@dataclass
class RouteInfo:
    start: str
    location: str
    ends: set[int]
    seen_at_stage: dict[StageLocation, int]
    loop_len: Optional[int]
    loop_from: Optional[StageLocation]

starts = set([loc for loc in map.keys() if loc.endswith('A')])
route_info = [ RouteInfo(loc, loc, set(), {}, None, None) for loc in starts]

while [ri for ri in route_info if ri.loop_len is None]:
    route_stage = steps % route_len
    direction = route[route_stage]
    for i, ri in enumerate(route_info):
        if ri.loop_len is not None:
            continue
        ri.location = map[ri.location][direction]
        if ri.location.endswith('Z'):
            ri.ends.add(steps)
        stage_location: StageLocation = (route_stage, ri.location)
        if stage_location in ri.seen_at_stage:
            ri.loop_from = stage_location
            ri.loop_len = steps - ri.seen_at_stage[stage_location]
        ri.seen_at_stage[stage_location] = steps
    steps += 1
final_step = route_len
for ri in route_info:
    # from inspection these are all prime numbers of loops
    assert ri.loop_len is not None
    print(ri.ends, ri.loop_len, ri.loop_len / route_len, ri.loop_from)
    final_step *= ri.loop_len // route_len

print(final_step)
