#!/usr/bin/env python3

import sys
from intcode import (Program, read_program, run_program)

filename = sys.argv[1]
input_s = sys.argv[2:]
input_i = [int(s) for s in input_s]

start_memory: Program = read_program(filename)

post_memory, output = run_program(start_memory, input_i)
print(output)
