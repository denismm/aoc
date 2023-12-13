#!/usr/bin/env python3
import sys
from itertools import zip_longest

filename = sys.argv[1]
if len(sys.argv) > 2:
    multiplier = int(sys.argv[2])
else:
    multiplier = 1

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

def count_valids(
        springs: list[str],
        groups: list[int],
        unknown_locs: list[int]) -> int:
    # print(f"cv:\t>{''.join(springs)}< {groups} {unknown_locs}")
    valid_count = 0
    position = unknown_locs[0]
    new_springs = list(springs)
    for choice in ['#', ' ']:
        new_springs[position] = choice
        # check validity so far
        unknowns = sum([1 for c in new_springs if c == '?'])
        knowns = sum([1 for c in new_springs if c == '#'])
        spring_count = sum(groups)
        if not (knowns <= spring_count <= knowns + unknowns):
            # print(f"can't continue with {knowns=} {unknowns=} {spring_count=}")
            continue
        spring_groups = ''.join(new_springs).split()
        invalid = False
        full_scan = True
        # print(f"check:\t>{''.join(new_springs)}<")
        for spring_group, group in zip_longest(spring_groups, groups):
            if spring_group is None:
                # not enough spaces left for numbers
                # print('not enough spaces left')
                invalid = True
                break
            if group is None:
                if '#' in spring_group:
                    # only ??? groups are ok
                    # print('uncounted springs')
                    invalid = True
                    break
            if '?' in spring_group:
                full_scan = False
                break
            if len(spring_group) != group:
                # print("wrong size")
                invalid = True
                break
        if invalid:
            # next choice
            continue
        if full_scan:
            # print("ok!")
            # valid result
            valid_count += 1
        if len(unknown_locs) > 1:
            # we have more groups to consider
            valid_count += count_valids(new_springs, groups, unknown_locs[1:])
    # print(f"returning {valid_count}")
    return valid_count

with open(filename, 'r') as f:
    for i, line in enumerate(f):
        spring_info, group_info = line.split()
        spring_info = spring_info.replace('.', ' ')
        # print(spring_info)
        unfolded_spring_info = '?'.join([spring_info] * multiplier)
        springs = list(unfolded_spring_info)
        groups = [int(s) for s in group_info.split(',')] * multiplier
        unknown_locs = [i for i, char in enumerate(springs) if char == '?']
        valid_arrangements = count_valids(springs, groups, unknown_locs)
        print(f"{i}: got {valid_arrangements}")
        total_counts += valid_arrangements
    print(total_counts)
