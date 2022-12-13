#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, "r") as f:
    instructions: list[str] = [line.rstrip() for line in f]
registers: dict[str, int] = {c: 0 for c in 'abcd'}
ip = 0


def get_value(spec: str) -> int:
    if spec in registers:
        return registers[spec]
    return int(spec)


def parse_line() -> None:
    global ip
    components = instructions[ip].split()
    inst = components[0]
    args = components[1:]
    if inst == 'cpy':
        source: int = get_value(args[0])
        registers[args[1]] = source
    elif inst == 'inc':
        registers[args[0]] += 1
    elif inst == 'dec':
        registers[args[0]] -= 1
    elif inst == 'jnz':
        test: int = get_value(args[0])
        if test != 0:
            jump: int = get_value(args[1])
            ip += jump
            return
    else:
        raise ValueError(f"bad instruction: {inst}")
    ip += 1


while ip < len(instructions):
    parse_line()

print(registers['a'])
