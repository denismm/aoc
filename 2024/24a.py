#!/usr/bin/env python3
import sys
from typing import Callable

filename = sys.argv[1]

Gate = tuple[tuple[str, str], str]
state: dict[str, int] = {}
open_wire: dict[str, Gate] = {}

with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        if ':' in line:
            name, value = line.split(': ')
            state[name] = int(value)
        elif '->' in line:
            gate_desc, destination = line.split(' -> ')
            (a, operator, b) = gate_desc.split()
            open_wire[destination] = ((a, b), operator)

operators: dict[str, Callable[[int, int], int]] = {
    'AND': lambda x, y: x & y,
    'OR' : lambda x, y: x | y,
    'XOR': lambda x, y: x ^ y,
}

while open_wire:
    dests = list(open_wire.keys())
    for dest in dests:
        gate: Gate = open_wire[dest]
        inputs = gate[0]
        if inputs[0] in state and inputs[1] in state:
            input_values = [state[a] for a in inputs]
            state[dest] = operators[gate[1]](*input_values)
            del open_wire[dest]

outputs: dict[str, int] = {k: v for k, v in state.items() if k.startswith('z')}
output = 0
for k, v in reversed(sorted(outputs.items())):
    output <<= 1
    output += v
print(output)
