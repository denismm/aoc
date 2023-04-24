#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    state = [int(x) for x in f.read().rstrip().split()]

permutations = set([tuple(state)])
blocks = len(state)

while True:
    # take out top entry
    length = max(state)
    entry = state.index(length)
    state[entry] = 0

    # spread around
    i = (entry + 1) % blocks
    while length:
        state[i] += 1
        length -= 1
        i = (i + 1) % blocks

    # check for repeats
    new_tuple = tuple(state)
    if new_tuple in permutations:
        print(len(permutations))
        exit(0)
    else:
        permutations.add(new_tuple)
