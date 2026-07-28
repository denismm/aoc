#!/usr/bin/env python3

import sys
from intcode import IntCodeComputer, read_program, Program
from itertools import chain, permutations
from collections.abc import Iterable

filename = sys.argv[1]
input_s = sys.argv[2:]
input_i = [int(s) for s in input_s]

start_memory: Program = read_program(filename)

max_output = 0
for phases in permutations(range(5)):
    amps: list[IntCodeComputer] = []
    for i in range(5):
        input_source: Iterable[int]
        if i == 0:
            input_source = [0]
        else:
            input_source = amps[i - 1].run()
        amp = IntCodeComputer( start_memory, chain([phases[i]], input_source))
        amps.append(amp)

    output = (list(amps[4].run()))[0]
    max_output = max([output, max_output])
print(max_output)
