#!/usr/bin/env python3
import sys
import re
from typing import NamedTuple

filename = sys.argv[1]

disc_re = re.compile(r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).")

DiscInfo = NamedTuple('DiscInfo', [
    ('number', int),
    ('size', int),
    ('position', int),
])

disc_info: list[DiscInfo] = []

with open(filename, "r") as f:
    for line in f:
        if m := disc_re.match(line):
            (number, size, position) = [int(x) for x in m.groups()]
            disc_info.append(DiscInfo(number, size, position))
        else:
            raise ValueError(f"bad disc {line}")

final_time: int = 0
disc_modulus: int = 0
for disc in disc_info:
    # get time for this disc
    disc_time = (disc.size - (disc.number + disc.position)) % disc.size
    if disc_modulus == 0:
        final_time = disc_time
        disc_modulus = disc.size
    else:
        escape = 0
        while final_time % disc.size != disc_time:
            final_time += disc_modulus
            escape += 1
            if escape == disc.size:
                raise ValueError("runaway")
        disc_modulus *= disc.size
print(final_time)
