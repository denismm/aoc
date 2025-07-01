#!/usr/bin/env python3
import sys
from dataclasses import dataclass
from typing import Optional

filename = sys.argv[1]
RegisterSet = tuple[int, ...]
Instruction = tuple[int, ...]


@dataclass
class Test:
    before: RegisterSet
    instruction: Instruction
    after: RegisterSet


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


def process_opcode(
    input: RegisterSet, code: str, instruction: Instruction
) -> RegisterSet:
    _, a, b, c = instruction
    opcode = opcodes[code]
    if opcode.a_reg:
        a = input[a]
    if opcode.b_reg:
        b = input[b]
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
    output = list(input)
    output[c] = result
    return tuple(output)

tests: list[Test] = []
program: list[Instruction] = []

with open(filename, "r") as f:
    data_for_test: dict[str, RegisterSet] = {}
    instruction: Optional[Instruction] = None
    for line in f:
        line = line.rstrip()
        if line and line[0] in "AB":
            section, data_s = line.split(": ")
            data: list[int] = [
                int(s) for s in data_s.strip(" []").replace(",", "").split()
            ]
            data_for_test[section] = tuple(data)
        elif line:
            instruction = tuple([int(s) for s in line.split()])
        else:
            if instruction and data_for_test:
                tests.append(
                    Test(
                        data_for_test["Before"],
                        instruction,
                        data_for_test["After"],
                    )
                )
                instruction = None
                data_for_test = {}
            else:
                break

    for line in f:
        line = line.rstrip()
        if line:
            program.append(tuple([
                int(s) for s in line.split()
            ]))

option_mapping: dict[int, set[str]] = {}

for test in tests:
    options: set[str] = set()
    intcode: int = test.instruction[0]
    for code in opcodes.keys():
        output = process_opcode(test.before, code, test.instruction)
        if output == test.after:
            options.add(code)
    if intcode in option_mapping:
        options &= option_mapping[intcode]
    if len(options) == 0:
        raise ValueError(f"{intcode} has no options at {test}")
    option_mapping[intcode] = options

for intcode, options in option_mapping.items():
    print(intcode, options)

opname_mapping: dict[int, str] = {}
found: set[str] = set()

last_len = 0
while len(opname_mapping) < 16:
    for intcode, options in option_mapping.items():
        if len(options) == 1:
            opname: str = options.pop()
            print(f"{intcode} = {opname}")
            opname_mapping[intcode] = opname
            found.add(opname)
    for intcode in list(option_mapping.keys()):
        if intcode in opname_mapping:
            del option_mapping[intcode]
        else:
            option_mapping[intcode] -= found
            if len(option_mapping[intcode]) == 0:
                raise ValueError(f"no options for {intcode}")

# Finally, process code
registers: RegisterSet = (0, 0, 0, 0)
for instruction in program:
    opname = opname_mapping[instruction[0]]
    registers = process_opcode(registers, opname, instruction)

print(registers)
