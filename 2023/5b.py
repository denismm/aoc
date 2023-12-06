#!/usr/bin/env python3
import sys

filename = sys.argv[1]

Range = tuple[int, int]         # start (inclusive), end(exclusive)
seed_ranges: list[Range] = []
maps: list[tuple[Range, int]] = []

def map_seeds(seed_ranges: list[Range]) -> list[Range]:
    new_seed_ranges: list[Range] = []
    maps.sort()
    for seed_start, seed_end in seed_ranges:
        relevant_maps = [map for map in maps
            if seed_start <= map[0][0] < seed_end
            or seed_start < map[0][1] <= seed_end
            or map[0][0] < seed_start < map[0][1]
        ]
        if not relevant_maps:
            new_seed_ranges.append((seed_start, seed_end))
            continue
        # seed_start will move forward as we deal with maps
        for source, transform in relevant_maps:
            source_start, source_end = source
            if seed_start < source_start:
                # some unmapped start
                new_seed_ranges.append((seed_start, source_start))
            mappable_start = max(seed_start, source_start)
            mappable_end = min(seed_end, source_end)
            new_seed_ranges.append((mappable_start + transform, mappable_end + transform))
            seed_start = mappable_end
        if seed_start < seed_end:
            new_seed_ranges.append((seed_start, seed_end))
    new_seed_ranges.sort()
    # print(new_seed_ranges)
    # combine adjacent or overlapping ranges
    result_ranges = [new_seed_ranges[0]]
    for new_range in new_seed_ranges[1:]:
        if result_ranges[-1][1] >= new_range[0]:
            result_ranges[-1] = (result_ranges[-1][0], max(new_range[1], result_ranges[-1][1]))
        else:
            result_ranges.append(new_range)
    return result_ranges


with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        if line.startswith('seeds:'):
            seed_data = [int(num_s) for num_s in line.split()[1:]]
            for i in range(0, len(seed_data), 2):
                seed_ranges.append((seed_data[i], sum(seed_data[i:i+2])))
            seed_ranges.sort()
            print(seed_ranges)
        elif line == '':
            if maps:
                seed_ranges = map_seeds(seed_ranges)
                maps = []
                # print(seeds)
        elif 'map' in line:
            print("processing", line)
        else:
            (target, source, size) = [int(num_s) for num_s in line.split()]
            maps.append(((source, source+size), target - source))
if maps:
    seed_ranges = map_seeds(seed_ranges)
print(sorted(seed_ranges))
