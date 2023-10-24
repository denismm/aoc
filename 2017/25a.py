#!/usr/bin/env python3
import sys
from typing import NamedTuple

filename = sys.argv[1]

tape: set[int] = set()

Instruction = NamedTuple('Instruction', [
    ('write', int),
    ('move', int),
    ('next', str)
])

machine: dict[str, tuple[Instruction, ...]] = {}

with open(filename, 'r') as f:
    lines = [line.rstrip() for line in f]

start_state = lines[0][-2]      # ... in state A.
checksum_steps = int(lines[1].split()[5])

i = 3
while i < len(lines):
    if not lines[i].startswith('In state '):
        raise ValueError(f"bad alignment on line {i}: {lines[i]}")
    state_name = lines[i][-2]
    instruction_list: list[Instruction] = []
    for j in (0, 1):
        inst_start = i + 2 + j*4
        inst_lines = lines[inst_start: inst_start + 4]
        write = int(inst_lines[0][-2])
        step_dir = inst_lines[1].split()[6]
        move = 1 if step_dir == 'right.' else -1
        next_state = inst_lines[2][-2]
        instruction_list.append(Instruction(write, move, next_state))
    machine[state_name] = tuple(instruction_list)
    i += 10

state = start_state
steps = 0
cursor = 0
while steps < checksum_steps:
    head_value = 1 if cursor in tape else 0
    instruction = machine[state][head_value]
    if instruction.write == 1:
        tape.add(cursor)
    else:
        tape.discard(cursor)
    cursor += instruction.move
    state = instruction.next
    steps += 1
    if steps % 1000000 == 0:
        print(steps)

# checksum!
print(f"final: {len(tape)} ({state} {cursor})")
