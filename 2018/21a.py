#!/usr/bin/env python3
import sys
from dataclasses import dataclass
from typing import Optional

filename = sys.argv[1]

debug = True
debug_loop = True

RegisterSet = list[int]
Arguments = tuple[int, ...]

@dataclass
class Instruction:
    code: str
    arguments: Arguments

FrozenState = tuple[int, int, tuple[int, ...]]
@dataclass
class State:
    ip: int
    binding: int
    registers: RegisterSet

    def frozen(self) -> FrozenState:
        return (self.ip, self.binding, tuple(self.registers))


@dataclass
class Opcode:
    op: str
    a_reg: bool
    b_reg: bool


class InfiniteLoop(Exception):
    pass

    # name          op   a reg b reg
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
    if debug_loop and c == state.binding:
        print(instruction, a, b, c, result)
    state.registers[c] = result
    state.ip = state.registers[state.binding]
    state.ip += 1

program: list[Instruction] = []

binding = 0
with open(filename, "r") as f:
    data_for_test: dict[str, RegisterSet] = {}
    instruction: Optional[Instruction] = None
    for line in f:
        if line.startswith('#ip'):
            binding = int(line.split()[1])
            continue
        line = line.rstrip()
        line = line.split('#')[0]
        if line:
            elements = line.split()
            code = elements.pop(0)
            arguments = tuple([int(s) for s in elements[:3]])
            program.append(Instruction(code, arguments))

states: list[State] = [State(0, binding, RegisterSet([sr, 0, 0, 0, 0, 0])) for sr in (2, 65537)]

# Finally, process code
if debug:
    print(states)
op_count = 0
# seen_state: set[FrozenState] = {state.frozen()}
try:
    while states[0].ip < len(program):
        if debug:
            print(">>> ", program[states[0].ip])
        for state in states:
            process_opcode(state, program)
        op_count += 1
        if op_count >= 1000000:
            raise InfiniteLoop()
        if debug:
            print(op_count, states)
        # if state.frozen() in seen_state:
            # raise InfiniteLoop()
        # seen_state.add(state.frozen())
        if states[0].registers[1:] != states[1].registers[1:]:
            print("difference")
            exit(1)
    # print(f"start {start_register} finished in {op_count} operations")
except InfiniteLoop:
    pass
    # print(f"start {start_register} hit an infinite loop at {op_count}")
