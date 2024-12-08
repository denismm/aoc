#!/usr/bin/env python3
import sys
from collections import defaultdict
from positions import Position, read_char_grid, add_direction, get_direction, scale_direction
from itertools import permutations
filename = sys.argv[1]

with open(filename, "r") as f:
    _, _, grid = read_char_grid(f, skip_dots=False)

antennas_for_freq: dict[str, set[Position]] = defaultdict(set)
for k, v in grid.items():
    if v == '.':
        continue
    antennas_for_freq[v].add(k)

antinodes: set[Position] = set()
harmonic_antinodes: set[Position] = set()
for freq, antennas in antennas_for_freq.items():
    # we might need freq for debugging
    for (source, target) in permutations(antennas, r=2):
        harmonic_antinodes.add(target)
        direction = get_direction(source, target)
        i = 1
        while True:
            antinode = add_direction(target, scale_direction(direction, i))
            if antinode not in grid:
                break
            if i == 1:
                antinodes.add(antinode)
            harmonic_antinodes.add(antinode)
            i += 1

print(len(antinodes))
print(len(harmonic_antinodes))
