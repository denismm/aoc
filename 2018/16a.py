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
    elif opcode.op == '|':
        result = a | b
    elif opcode.op == ':=':
        result = a
    elif opcode.op == '>':
        result = 1 if a > b else 0
    elif opcode.op == '==':
        result = 1 if a > b else 0
    else:
        raise ValueError(f"unknown op {opcode.op} in {code}")
    output = list(input)
    output[c] = result
    return tuple(output)

tests: list[Test] = []

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

trios: int = 0
for test in tests:
    options: set[str] = set()
    for code in opcodes.keys():
        output = process_opcode(test.before, code, test.instruction)
        if output == test.after:
            options.add(code)
    if len(options) >= 3:
        trios += 1

print(trios)
