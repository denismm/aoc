#!/usr/bin/env python3
import sys
import re
from typing import NamedTuple
from positions import Position, add_direction

filename = sys.argv[1]

Particle = NamedTuple('Particle', [('p', Position), ('v', Position), ('a', Position)])

position_re = re.compile(r'\w=<\s*([\-\d,]+)\>')
particles: list[Particle] = []
with open(filename, 'r') as f:
    for line in f:
        components = line.split(', ')
        sub_coords: list[Position] = []
        for component in components:
            m = position_re.match(component)
            if not m:
                raise ValueError(component)
            sub_coords.append(tuple([int(c) for c in m.group(1).split(',')]))
        particles.append(Particle(*sub_coords))

def manhattan(position: Position) -> int:
    return sum([abs(x) for x in position])

new_list: list[tuple[int, ...]] = []

for particle in particles:
    new_list.append( tuple(reversed([manhattan(pos) for pos in particle])))

easy_answer = [x[0] for x in sorted(enumerate(new_list), key=lambda x: x[1])]
print(easy_answer[:10])
