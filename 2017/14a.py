#!/usr/bin/env python3
import sys
import functools

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

def bit_count(x: int) -> int:
    bits = 0
    while x > 0:
        bits += x % 2
        x >>= 1
    return bits

bits_for_byte = [ bit_count(i) for i in range(256)]

total_bits = 0
for i in range(128):
    knot_hash = compute_knot_hash( f"{hash_key}-{i}".encode('ascii'))
    total_bits += sum([bits_for_byte[c] for c in knot_hash])

print( total_bits )
