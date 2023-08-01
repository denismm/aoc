#!/usr/bin/env python3
import sys
from typing import NamedTuple
from collections import defaultdict, deque

filename = sys.argv[1]

Command = NamedTuple('Command', [('instruction', str), ('args', list[str])])

program: list[Command] = []

with open(filename, 'r') as f:
    for line in f:
        tokens = line.rstrip().split()
        command = Command(tokens[0], tokens[1:])
        program.append(command)

registers: tuple[dict[str, int], ...] = (defaultdict(lambda: 0), defaultdict(lambda: 0))

for id in range(2):
    registers[id]['p'] = id

def get_value(id: int, arg: str) -> int:
    if arg.isnumeric() or (arg[0] == '-' and arg[1:].isnumeric()):
        return int(arg)
    if len(arg) == 1:
        return registers[id][arg]
    raise ValueError(f"bad register {arg}")

position = [0, 0]
incoming_queue: tuple[deque[int], ...] = (deque([]), deque([]))
send_counts: list[int] = [0, 0]
instance_state: list[str] = ['run', 'run']

while 'run' in instance_state:
    for id in range(2):
        if instance_state[id] == 'end':
            continue
        if position[id] < 0 or position[id] >= len(program):
            instance_state[id] = 'end'
            continue
        command = program[position[id]]
        instruction, args = command
        if instruction == 'snd':
            value = get_value(id, args[0])
            incoming_queue[1 - id].append(value)
            send_counts[id] += 1
        elif instruction == 'set':
            registers[id][args[0]] = get_value(id, args[1])
        elif instruction == 'add':
            registers[id][args[0]] += get_value(id, args[1])
        elif instruction == 'mul':
            registers[id][args[0]] *= get_value(id, args[1])
        elif instruction == 'mod':
            registers[id][args[0]] %= get_value(id, args[1])
        elif instruction == 'rcv':
            if len(incoming_queue[id]) == 0:
                instance_state[id] = 'wait'
                continue
            else:
                value = incoming_queue[id].popleft()
                registers[id][args[0]] = value
                instance_state[id] = 'run'
        elif instruction == 'jgz':
            value = get_value(id, args[0])
            if value > 0:
                position[id] += get_value(id, args[1])
                continue
        else:
            raise ValueError(f"Bad instruction {instruction}")
        position[id] += 1
print(instance_state)
print(send_counts)
