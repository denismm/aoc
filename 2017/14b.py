#!/usr/bin/env python3
import sys
import functools
from positions import Position, cardinal_directions, add_direction

hash_key = sys.argv[1]

loop_len = 256

def compute_knot_hash(seed: bytes) -> list[int]:
    numbers = list(range(loop_len))
    lengths = list(seed) + [17, 31, 73, 47, 23]

    position = 0
    skip_size = 0

    for iteration in range(64):
        for length in lengths:
            # reverse from position to position+length
            end_reverse = (position + length) % loop_len
            if end_reverse > position:
                swap = numbers[position:end_reverse]
            else:
                swap = numbers[position:] + numbers[:end_reverse]
            for i, p in enumerate(range(position, position + length)):
                numbers[p % loop_len] = swap[length - 1 - i]
            # move
            position = (position + length + skip_size) % loop_len
            # increase
            skip_size += 1
    # numbers is sparse hash
    dense: list[int] = []
    for i in range(16):
        block = numbers[i * 16: (i+1) * 16]
        dense.append(functools.reduce(lambda a, b: a ^ b, block))
    return dense

def bit_pattern(x: int) -> set[int]:
    bits: set[int] = set()
    for i in range(8):
        if x % 2 == 1:
            bits.add(7 - i)
        x >>= 1
    return bits

bits_for_byte = [ bit_pattern(i) for i in range(256)]


bit_grid: set[Position] = set()
for i in range(128):
    knot_hash = compute_knot_hash( f"{hash_key}-{i}".encode('ascii'))
    for j, knot_byte in enumerate(knot_hash):
        bits = bits_for_byte[knot_byte]
        offset = j * 8
        for bit in bits:
            bit_position = (i, offset + bit)
            bit_grid.add(bit_position)

print(len(bit_grid))

regions = 0

while bit_grid:
    regions += 1
    start_point = bit_grid.pop()
    frontier = set([start_point])
    while frontier:
        next_point = frontier.pop()
        neighbors = [add_direction(dir, next_point) for dir in cardinal_directions]
        for neighbor in neighbors:
            if neighbor in bit_grid:
                frontier.add(neighbor)
                bit_grid.remove(neighbor)

print(regions)
