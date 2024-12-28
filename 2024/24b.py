#!/usr/bin/env python3
import sys
from typing import Callable
from collections import defaultdict

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

forward: dict[str, set[str]] = defaultdict(set)
oper: dict[str, str] = {}
for dest, gate in open_wire.items():
    for input in gate[0]:
        forward[input].add(dest)
    oper[dest] = gate[1]

bus_width = int(max(state.keys())[1:]) + 1

mistakes: list[str] = []
role: dict[tuple[int, str], str] = {}
def fr(level: int, position: str) -> set[str]:
    try:
        return forward[role[level, position]]
    except KeyError:
        mistakes.append(f"can't find {position} at {level}")
        return set()

for i in range(bus_width):
    # expected structure
    # xN -> XOR aN, AND bN
    # yN -> XOR aN, AND bN
    # a -> AND cN, XOR zN
    # b -> OR dN
    # c -> OR dN
    # d -> XOR zN+1, AND cN+1
    # z -> no output
    num_key = "%02d" % i
    role[i, 'x'] = "x" + num_key
    role[i, 'y'] = "y" + num_key
    if fr(i, 'x') != fr(i, 'y'):
        mistakes.append(f"xy mismatch at {i}")
    ab_dests = fr(i, 'x')
    for dest in ab_dests:
        if oper[dest] == 'XOR' and (i, 'a') not in role:
            role[i, 'a'] = dest
        elif oper[dest] == 'AND' and (i, 'b') not in role:
            role[i, 'b'] = dest
        else:
            mistakes.append(f"unexpected gate in ab at {i}: {dest}")
    for dest in fr(i, 'a'):
        if oper[dest] == "AND":
            if (i, 'c') in role:
                if dest != role[i, 'c']:
                    mistakes.append(f"c doesn't line up at {i}: {role[i, 'c']} != {dest}")
            else:
                role[i, 'c'] = dest
        elif oper[dest] == 'XOR':
            if dest != 'z' + num_key:
                mistakes.append(f"z misplaced at {i}: xor from a is {dest}")
            role[i, 'z'] = dest
        else:
            mistakes.append(f"unexpected destination for a at {i}: {dest}")
    ds = fr(i, 'b')
    if len(ds) > 1:
        mistakes.append(f"too many outputs for b at {i}: {fr(i, 'b')}")
    if ds:
        d: str = list(fr(i, 'b'))[0]
        if oper[d] != 'OR':
            mistakes.append(f"bad operator for d at {i}: {d} {oper[d]}")
        role[i, 'd'] = d
        for dest in fr(i, 'd'):
            if oper[dest] == "AND":
                role[i + 1, 'c'] = dest
            elif oper[dest] == 'XOR':
                next_key = "%02d" % (i + 1)
                if dest != 'z' + next_key:
                    mistakes.append(f"z misplaced at {i+1}: xor from d {i} is {dest}")
                role[i + 1, 'z'] = dest
            else:
                mistakes.append(f"unexpected destination for d at {i}: {dest}")

print('\t'.join('#abcdxyz'))
for i in range(bus_width):
    print(i, end="\t")
    for position in 'abcdxyz':
        print(role.get((i, position), 'XXX'), end="\t")
    print()

for m in mistakes:
    print(m)
for unassigned in (set(open_wire.keys()) - set(role.values())):
    print(f"{unassigned} is unassigned: {open_wire[unassigned]} -> {forward[unassigned]}")
