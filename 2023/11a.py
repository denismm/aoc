#!/usr/bin/env python3
import sys
from positions import Position, manhattan
from itertools import combinations

filename = sys.argv[1]
expansion_increment = int(sys.argv[2]) - 1
galaxy_map: set[Position] = set()
# do vertical expansion as we read
with open(filename, 'r') as f:
    expansion = 0
    for j, line in enumerate(f):
        if '#' in line:
            for i, character in enumerate(line):
                if character == '#':
                    pos = (i, j + expansion)
                    galaxy_map.add(pos)
        else:
            expansion += expansion_increment

x_coords = set([x for x, y in galaxy_map])
max_x = max(x_coords)
expansion = 0
new_map: set[Position] = set()
for i in range(max_x + 1):
    if i in x_coords:
        for (x, y) in [(x, y) for x, y in galaxy_map if x == i]:
            new_map.add((x + expansion, y))
    else:
        expansion += expansion_increment
galaxy_map = new_map

total_distance = 0
for source, target in combinations(galaxy_map, 2):
    total_distance += manhattan(source, target)

# debug print
if False:
    max_x = max(set([x for x, y in galaxy_map]))
    max_y = max(set([y for x, y in galaxy_map]))
    for j in range(max_y + 1):
        for i in range(max_x + 1):
            if (i, j) in galaxy_map:
                output = '#'
            else:
                output = '.'
            print(output, end="")
        print()
print(total_distance)
