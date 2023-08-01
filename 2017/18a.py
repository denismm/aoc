#!/usr/bin/env python3
import sys
from typing import NamedTuple, Optional
from collections import defaultdict

filename = sys.argv[1]

Command = NamedTuple('Command', [('instruction', str), ('args', list[str])])

program: list[Command] = []

with open(filename, 'r') as f:
    for line in f:
        tokens = line.rstrip().split()
        command = Command(tokens[0], tokens[1:])
        program.append(command)

registers: dict[str, int] = defaultdict(lambda: 0)
def get_value(arg: str) -> int:
    if arg.isnumeric() or (arg[0] == '-' and arg[1:].isnumeric()):
        return int(arg)
    if len(arg) == 1:
        return registers[arg]
    raise ValueError(f"bad register {arg}")

position = 0
last_played: Optional[int] = None

while 0 <= position < len(program):
    command = program[position]
    instruction, args = command
    if instruction == 'snd':
        value = get_value(args[0])
        # print(f"playing {value}")
        last_played = value
    elif instruction == 'set':
        registers[args[0]] = get_value(args[1])
    elif instruction == 'add':
        registers[args[0]] += get_value(args[1])
    elif instruction == 'mul':
        registers[args[0]] *= get_value(args[1])
    elif instruction == 'mod':
        registers[args[0]] %= get_value(args[1])
    elif instruction == 'rcv':
        value = get_value(args[0])
        if value != 0:
            print(f"recovering {last_played}")
            exit(0)
    elif instruction == 'jgz':
        value = get_value(args[0])
        if value > 0:
            position += get_value(args[1])
            continue
    else:
        raise ValueError(f"Bad instruction {instruction}")
    position += 1
