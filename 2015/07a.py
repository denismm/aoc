#!/usr/bin/env python3
import sys
import re
from typing import NamedTuple

instruction_re = re.compile(r'([\da-z]*)\s*([A-Z]*)\s*([\da-z]*)')

filename = sys.argv[1]
Instruction = NamedTuple('Instruction', [('operator', str), ('inputs', tuple[str, ...])])
feeders: dict[str, Instruction] = {}

with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        command, target = line.split(' -> ')
        m = instruction_re.match(command)
        if not m:
            raise ValueError(command)
        (a, operator, b) = m.groups()
        feeders[target] = Instruction(operator, (a, b))

registers: dict[str, int] = {}

def get_value(r: str) -> int:
    if r == '':
        return 0
    elif r.isnumeric():
        return int(r)
    else:
        return registers[r]

def evaluate_circuit(circuit: str) -> bool:
    inst = feeders[circuit]
    operator, inputs = inst
    for input in inputs:
        if input != '' and not input.isnumeric() and input not in registers:
            return False
    (a, b) = [get_value(input) for input in inputs]
    c: int = 0
    if operator == '':
        c = a
    elif operator == 'NOT':
        c = ~b
    elif operator == 'AND':
        c = a & b
    elif operator == 'OR':
        c = a | b
    elif operator == 'LSHIFT':
        c = a << b
    elif operator == 'RSHIFT':
        c = a >> b
    else:
        raise ValueError(operator)
    registers[circuit] = c
    return True

while 'a' not in registers:
    possible_circuits = list(feeders.keys())
    for circuit in possible_circuits:
        if evaluate_circuit(circuit):
            del feeders[circuit]

print(registers['a'])
