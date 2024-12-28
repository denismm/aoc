#!/usr/bin/env python3
import sys
import graphviz

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

dot = graphviz.Digraph("AoC 2024-24")

for input in state.keys():
    dot.node(input)
for output, gate in open_wire.items():
    dot.node(output, f"{output} {gate[1]}")
for output, gate in open_wire.items():
    for input in gate[0]:
        dot.edge(input, output)

# print(dot.source)
