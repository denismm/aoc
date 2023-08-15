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

def tick() -> None:
    for i, particle in enumerate(particles):
        new_v = add_direction(particle.v, particle.a)
        new_p = add_direction(particle.p, new_v)
        particles[i] = Particle(new_p, new_v, particle.a)

def manhattan(position: Position) -> int:
    return sum([abs(x) for x in position])

# unused
def gone(particle: Particle) -> bool:
    # is everything in the same quadrant?
    for coordinate in range(3):
        directions = [ 0 if x == 0 else x // abs(x) for x in [position[coordinate] for position in particle]]
        if directions[0] != directions[1] or directions[1] != directions[2]:
            return False
    return True

arrangement: list[list[int]] = []
for i in range(1000):
    tick()
    distances = enumerate([manhattan(particle.p) for particle in particles])
    sorted_distances = sorted(distances, key=lambda x: x[1])
    arrangement.append([x[0] for x in sorted_distances])
    # print(arrangement[-1][:5])
    if len(arrangement) > 3 and arrangement[-1] == arrangement[-2] == arrangement[-3]:
        print(f"at step {i}, arrangement is {arrangement[-1][:5]}")
