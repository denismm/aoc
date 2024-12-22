#!/usr/bin/env python3
import sys

filename = sys.argv[1]
new_a = int(sys.argv[2])

reg: dict[str, int] = {}
program: list[int] = []
with open(filename, "r") as f:
    for line in f:
        if line.startswith('Register'):
            regname = line[9]
            reg[regname] = int(line.split()[-1])
        elif line.startswith('Program'):
            program_s = line.split()[-1]
            program = [int(s) for s in program_s.split(',')]

reg['A'] = new_a

output: list[int] = []

pointer = 0

opcode_map = "ZZZZABC"

def combo(opcode: int) -> int:
    if opcode <= 3:
        return opcode
    if opcode <= 6:
        return reg[opcode_map[opcode]]
    raise ValueError("bad combo operand")

def xdv(operand: int) -> int:
    return reg['A'] >> combo(operand)

while pointer < len(program):
    opcode = program[pointer]
    operand = program[pointer + 1]

    if opcode == 0:     # adv
        reg['A'] = xdv(operand)
    elif opcode == 1:   # bxl
        reg['B'] = reg['B'] ^ operand
    elif opcode == 2:   # bst
        reg['B'] = combo(operand) % 8
    elif opcode == 3:   # jnz
        if reg['A'] != 0:
            pointer = operand
            continue
    elif opcode == 4:   # bxc
        reg['B'] = reg['B'] ^ reg['C']
    elif opcode == 5:   # out
        output.append(combo(operand) % 8)
    elif opcode == 6:   # bdv
        reg['B'] = xdv(operand)
    elif opcode == 7:   # cdv
        reg['C'] = xdv(operand)
    pointer += 2

print(','.join([str(x) for x in output]))
