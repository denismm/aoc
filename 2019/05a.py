#!/usr/bin/env python3

import sys
from intcode import (Program, read_program, run_program)

filename = sys.argv[1]

start_memory: Program = read_program(filename)

post_memory, output = run_program(start_memory, [1])
print(output)
