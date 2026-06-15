#!/usr/bin/env python3

import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    program: list[int] = [int(s) for s in f.read().rstrip().split(',')]

opcodes: dict[int, str] = {
    1: "+",
    2: "*",
    99: "halt",
}

ip = 0

# pre-handling
program[1] = 12
program[2] = 2

while True:
    operation, a_ptr, b_ptr, out_ptr = program[ip:ip+4]
    action = opcodes[operation]
    if action == 'halt':
        break
    a = program[a_ptr]
    b = program[b_ptr]
    if action == '+':
        out = a + b
    elif action == '*':
        out = a * b
    else:
        raise ValueError(f"unknown opcode at {ip=} {action=}")
    program[out_ptr] = out
    ip += 4

print(program[0])
