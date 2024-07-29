#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, "r") as f:
    instructions: list[list[str]] = [line.rstrip().split() for line in f]
commands = [inst[0] for inst in instructions]
arguments = [[x.rstrip(',') for x in inst[1:]] for inst in instructions]
registers: dict[str, int] = {c: 0 for c in 'ab'}

if len(sys.argv) > 2:
    registers['a'] = int(sys.argv[2])

output_limit = 20

class LastOutput(Exception):
    pass

def get_value(spec: str) -> int:
    if spec in registers:
        return registers[spec]
    return int(spec)

debug = False

def parse_line() -> None:
    global ip
    global output
    # print(f"parsing {ip} {commands[ip]} {arguments[ip]} {[registers[x] for x in 'ab']}")
    inst = commands[ip]
    args = arguments[ip]
    jump: int
    test: int
    if inst == 'hlf':
        a = args[0]
        if registers[a] % 2:
            raise ValueError(f"Half of {registers[a]}?!")
        registers[a] //= 2
    elif inst == 'tpl':
        a = args[0]
        registers[a] *= 3
    elif inst == 'inc':
        a = args[0]
        registers[a] += 1
    elif inst == 'jmp':
        jump = get_value(args[0])
        if debug:
            print(f"jump by {jump}")
        ip += jump
        return
    elif inst == 'jie':
        test = get_value(args[0])
        if test % 2 == 0:
            jump = get_value(args[1])
            if debug:
                print(f"jie by {jump} {registers}")
            ip += jump
            # print_next_section()
            return
    elif inst == 'jio':
        test = get_value(args[0])
        if test == 1:
            jump = get_value(args[1])
            if debug:
                print(f"jio by {jump} {registers}")
            ip += jump
            # print_next_section()
            return
    else:
        raise ValueError(f"bad instruction: {inst}")
    # print(f"ip: {ip} registers: {[registers[x] for x in 'abcd']}")
    ip += 1

ip = 0
output: str = ""
while ip < len(instructions):
    parse_line()

print(registers)
