#!/usr/bin/env python3
import sys
from itertools import zip_longest

filename = sys.argv[1]
if len(sys.argv) > 2:
    multiplier = int(sys.argv[2])
else:
    multiplier = 1

total_counts = 0

def count_valids(
        springs: list[str],
        groups: list[int],
        unknown_locs: list[int]) -> int:
    # print(f"cv:\t>{''.join(springs)}< {groups} {unknown_locs}")
    valid_count = 0
    position = unknown_locs[0]
    work_springs = list(springs)
    for choice in ['#', ' ']:
        work_springs[position] = choice
        # check validity so far
        unknowns = sum([1 for c in work_springs if c == '?'])
        knowns = sum([1 for c in work_springs if c == '#'])
        spring_count = sum(groups)
        if not (knowns <= spring_count <= knowns + unknowns):
            # print(f"can't continue with {knowns=} {unknowns=} {spring_count=}")
            continue
        spring_groups = ''.join(work_springs).split()
        invalid = False
        full_scan = True
        # print(f"check:\t>{''.join(work_springs)}<")
        for spring_group, group in zip_longest(spring_groups, groups):
            # print(f"{spring_group=} {group=}")
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
            # "##?" is invalid for a group of 1, etc.
            if group and spring_group.startswith('#' * (group + 1)):
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
            # transform to smaller problem
            next_position = unknown_locs[1]
            # leave one previous character to anchor any in-progress group
            trim_chars = next_position - 1
            next_unknowns = [l - trim_chars for l in unknown_locs[1:]]
            handled_springs = work_springs[:trim_chars]
            next_springs = work_springs[trim_chars:]
            seen_groups = [len(group) for group in ''.join(handled_springs).split()]
            # are we subtracting from last set?
            subtraction = 0
            if handled_springs and handled_springs[-1] == '#' and next_springs[0] == '#':
                subtraction = seen_groups.pop()

            handled_groups = groups[:len(seen_groups)]
            if handled_groups != seen_groups:
                raise ValueError(f"{handled_groups=} != {seen_groups=}")
            next_groups = groups[len(seen_groups):]
            # print(f"{next_groups=} {next_unknowns=} {subtraction=}")
            if subtraction:
                next_groups[0] -= subtraction

            valid_count += count_valids(next_springs, next_groups, next_unknowns)
    # print(f"returning {valid_count}")
    return valid_count

with open(filename, 'r') as f:
    for i, line in enumerate(f):
        spring_info, group_info = line.split()
        spring_info = spring_info.replace('.', ' ')
        # print(spring_info)
        unfolded_spring_info = '?'.join([spring_info] * multiplier)
        springs = [' '] + list(unfolded_spring_info)
        groups = [int(s) for s in group_info.split(',')] * multiplier
        unknown_locs = [i for i, char in enumerate(springs) if char == '?']
        valid_arrangements = count_valids(springs, groups, unknown_locs)
        print(f"{i}: got {valid_arrangements}")
        total_counts += valid_arrangements
    print(total_counts)
