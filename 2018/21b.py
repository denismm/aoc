#!/usr/bin/env python3
import sys
from dataclasses import dataclass
from typing import Optional

filename = sys.argv[1]

debug = False
debug_loop = False

RegisterSet = list[int]
Arguments = tuple[int, ...]

@dataclass
class Instruction:
    code: str
    arguments: Arguments

    def pretty_print(self) -> str:
        opcode = opcodes[self.code]
        return opcode.pretty_print(self.arguments)


FrozenState = tuple[int, int, tuple[int, ...]]
@dataclass
class State:
    ip: int
    binding: int
    registers: RegisterSet

    def frozen(self) -> FrozenState:
        return (self.ip, self.binding, tuple(self.registers))


register_names = "zIbcde"
@dataclass
class Opcode:
    op: str
    a_reg: bool
    b_reg: bool

    def pretty_print(self, arguments: Arguments) -> str:
        # turn "eqrr 5 0 4" into "d = (5 == z)"
        pretty: str = ""
        if self.a_reg:
            pretty += register_names[arguments[0]]
        else:
            pretty += str(arguments[0])
        pretty += " "
        if self.op != ":=":
            pretty += f"{self.op} "
            if self.b_reg:
                pretty += register_names[arguments[1]]
            else:
                pretty += str(arguments[1])
            pretty += " "
        pretty += f"-> {register_names[arguments[2]]}"
        return pretty


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
    if state.ip == 29:
        print(state.registers[5])

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

# for (i, cmd) in enumerate(program):
    # print(f"{i};{cmd.pretty_print()}")
# exit(0)

state: State = State(0, binding, RegisterSet([0, 0, 0, 0, 0, 0]))

# Finally, process code
if debug:
    print(state)
op_count = 0
seen_state: set[FrozenState] = {state.frozen()}
try:
    while state.ip < len(program):
        if debug:
            print(">>> ", program[states[0].ip])
        process_opcode(state, program)
        op_count += 1
        # if op_count >= 1000000:
            # raise InfiniteLoop()
        if debug:
            print(op_count, state)
        if state.frozen() in seen_state:
            raise InfiniteLoop()
        seen_state.add(state.frozen())
    # print(f"start {start_register} finished in {op_count} operations")
    print("safe exit")
except InfiniteLoop:
    print(f"infinite loop found")
    exit(0)

    # print(f"start {start_register} hit an infinite loop at {op_count}")
