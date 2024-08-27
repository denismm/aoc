#!/usr/bin/env python3
import sys
import re

filename = sys.argv[1]

coords: list[int] = []
with open(filename, "r") as f:
    line = f.read()  
    for entry in line.split():
        if entry[0].isnumeric():
            coords.append(int(re.split(r'\D', entry)[0]))

if len(coords) != 2:
    raise ValueError(f"Too many coords: {coords}")

print(coords)

# larger triangular number
triangle_len = coords[0] + coords[1] - 1
# print(triangle_len)
triangle = sum( [ x for x in range(triangle_len + 1) ] )
# print(triangle)
distance = triangle_len - coords[1]
# print(distance)
position = triangle - distance
print(position)

def modular_pow(base: int, exponent: int, modulus: int) -> int:
    if modulus == 0:
        return 0
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent >>= 1
        base = (base * base) % modulus
    return result


multiplier = modular_pow(252533, (position - 1), 33554393)
print(f"{multiplier=}")
value = (20151125 * multiplier) % 33554393

print(value)

