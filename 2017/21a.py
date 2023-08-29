#!/usr/bin/env python3
import sys
from positions import Position, add_direction

Pattern = set[Position]
KeyPattern = frozenset[Position]

filename = sys.argv[1]
iterations = int(sys.argv[2])

size_rules: dict[int, dict[KeyPattern, Pattern]] = {2: {}, 3: {} }

def rule_to_pattern(rule: str) -> Pattern:
    grid = rule.split('/')
    output: Pattern = set()
    for j, row in enumerate(grid):
        for i, character in enumerate(row):
            if character == '#':
                output.add( (i, j) )
    return output

def diagonal_flip(pattern: Pattern) -> Pattern:
    return set([ (j, i) for i, j in pattern ])

def rotate(pattern: Pattern, size: int) -> Pattern:
    return set([ (j, size - 1 - i) for i, j in pattern ])

def rotations_for_set(pattern: Pattern, size: int) -> set[KeyPattern]:
    rotations: set[KeyPattern] = { frozenset(pattern) }
    rotations.add(frozenset(diagonal_flip(pattern)))
    new_pattern = set(pattern)
    for _ in range(3):
        new_pattern = rotate(new_pattern, size)
        rotations.add(frozenset(new_pattern))
        rotations.add(frozenset(diagonal_flip(new_pattern)))
    return rotations

with open(filename, 'r') as f:
    for line in f:
        input, output = line.rstrip().split(' => ')
        size = len(input.split('/'))
        input_set = rule_to_pattern(input)
        output_set = rule_to_pattern(output)
        for rotation in rotations_for_set(input_set, size):
            size_rules[size][frozenset(rotation)] = output_set

# print(size_rules)

start_grid = rule_to_pattern('.#./..#/###')
start_size = 3
for tick in range(iterations):
    new_grid: Pattern = set()
    if start_size % 2 == 0:
        input_step = 2
        output_step = 3
    else:
        input_step = 3
        output_step = 4
    new_size = (start_size // input_step) * output_step
    for i in range(start_size // input_step):
        for j in range(start_size // input_step):
            input_offset: Position = (i * input_step, j * input_step)
            match_pattern: Pattern = set()
            for k in range(input_step):
                for l in range(input_step):
                    match_location = (k, l)
                    probe = add_direction(input_offset, match_location)
                    if probe in start_grid:
                        match_pattern.add(match_location)
            # print(f"{match_pattern =} {input_step=}")
            output_pattern = size_rules[input_step][frozenset(match_pattern)]
            output_offset = (i * output_step, j * output_step)
            for position in output_pattern:
                new_grid.add(add_direction(output_offset, position))
    start_size = new_size
    start_grid = new_grid

# print(start_grid)
print(len(start_grid))
