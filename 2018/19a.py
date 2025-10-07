#!/usr/bin/env python3
import sys
from dataclasses import dataclass
from typing import Optional

filename = sys.argv[1]
start_register = int(sys.argv[2])

RegisterSet = list[int]
Arguments = tuple[int, ...]

@dataclass
class Instruction:
    code: str
    arguments: Arguments

@dataclass
class State:
    ip: int
    binding: int
    registers: RegisterSet


@dataclass
class Opcode:
    op: str
    a_reg: bool
    b_reg: bool


opcodes: dict[str, Opcode] = {
    "addr": Opcode("+", True, True),
    "addi": Opcode("+", True, False),
    "mulr": Opcode("*", True, True),
    "muli": Opcode("*", True, False),
    "banr": Opcode("&", True, True),
    "bani": Opcode("&", True, False),
    "borr": Opcode("|", True, True),
    "bori": Opcode("|", True, False),
    "setr": Opcode(":=", True, False),
    "seti": Opcode(":=", False, False),
    "gtir": Opcode(">", False, True),
    "gtri": Opcode(">", True, False),
    "gtrr": Opcode(">", True, True),
    "eqir": Opcode("==", False, True),
    "eqri": Opcode("==", True, False),
    "eqrr": Opcode("==", True, True),
}


def process_opcode( state: State, program: list[Instruction]) -> None:
    registers = state.registers
    registers[state.binding] = state.ip
    instruction: Instruction = program[state.ip]
    opcode = opcodes[instruction.code]
    a, b, c = instruction.arguments
    if opcode.a_reg:
        a = registers[a]
    if opcode.b_reg:
        b = registers[b]
    result: int = 0
    if opcode.op == '+':
        result = a + b
    elif opcode.op == '*':
        result = a * b
    elif opcode.op == '&':
        result = a & b
    elif opcode.op == '|':
        result = a | b
    elif opcode.op == ':=':
        result = a
    elif opcode.op == '>':
        result = 1 if a > b else 0
    elif opcode.op == '==':
        result = 1 if a == b else 0
    else:
        raise ValueError(f"unknown op {opcode.op} in {code}")
    state.registers[c] = result
    state.ip = state.registers[state.binding]
    state.ip += 1

program: list[Instruction] = []

state: State = State(0, 0, RegisterSet([start_register, 0, 0, 0, 0, 0]))
with open(filename, "r") as f:
    data_for_test: dict[str, RegisterSet] = {}
    instruction: Optional[Instruction] = None
    for line in f:
        if line.startswith('#ip'):
            state.binding = int(line.split()[1])
            continue
        line = line.rstrip()
        if line:
            elements = line.split()
            code = elements.pop(0)
            arguments = tuple([int(s) for s in elements[:3]])
            program.append(Instruction(code, arguments))

# Finally, process code
debug = True
print(state)
while state.ip < len(program):
    process_opcode(state, program)
    if debug or state.ip == 3:
        print(state)

print(state)

print(state.registers[0])
