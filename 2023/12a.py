#!/usr/bin/env python3
import sys
from itertools import combinations

filename = sys.argv[1]

total_counts = 0

def get_arrangement(springs: list[str], combination: tuple[int, ...]) -> list[str]:
    output: list[str] = []
    combo_i = 0
    for char in springs:
        if char == '?':
            if combo_i in combination:
                new_char = "#"
            else:
                new_char = " "
            combo_i += 1
        elif char == ".":
            new_char = " "
        else:
            new_char = char
        output.append(new_char)
    return output

def get_groups(arrangement: list[str]) -> list[int]:
    springs = ''.join(arrangement)
    groups = [len(x) for x in springs.split()]
    return groups

with open(filename, 'r') as f:
    for line in f:
        spring_info, group_info = line.split()
        springs = list(spring_info)
        groups = [int(s) for s in group_info.split(',')]
        known_count = sum([1 for c in springs if c == '#'])
        unknown_count = sum([1 for c in springs if c == '?'])
        spring_count = sum(groups)
        unknown_springs = spring_count - known_count
        valid_arrangements = 0
        for combination in combinations(range(unknown_count), unknown_springs):
            arrangement = get_arrangement(springs, combination)
            if get_groups(arrangement) == groups:
                valid_arrangements += 1
        total_counts += valid_arrangements
    print(total_counts)
