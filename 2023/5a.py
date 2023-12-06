#!/usr/bin/env python3
import sys

filename = sys.argv[1]

seeds: list[int] = []
maps: list[tuple[int, int, int]] = []

def map_seeds(seeds: list[int]) -> list[int]:
    new_seeds: list[int] = []
    for seed in seeds:
        found = False
        for (target, source, size) in maps:
            if seed >= source and seed < source + size:
                if found:
                    raise ValueError("range collision")
                # print (f"{seed=} {source=} {target=}")
                new_seeds.append(seed - source + target)
                found = True
        if not found:
            new_seeds.append(seed)
    return new_seeds


with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        if line.startswith('seeds:'):
            for num_s in line.split()[1:]:
                seeds.append(int(num_s))
            # print(seeds)
        elif line == '':
            if maps:
                seeds = map_seeds(seeds)
                maps = []
                # print(seeds)
        elif 'map' in line:
            print("processing", line)
        else:
            (target, source, size) = [int(num_s) for num_s in line.split()]
            maps.append((target, source, size))
if maps:
    seeds = map_seeds(seeds)
print(sorted(seeds))
