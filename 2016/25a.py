#!/usr/bin/env python3
import sys

from typing import Union, Literal

filename = sys.argv[1]

with open(filename, "r") as f:
    instructions: list[list[str]] = [line.rstrip().split() for line in f]
commands = [inst[0] for inst in instructions]
arguments = [inst[1:] for inst in instructions]
registers: dict[str, int] = {c: 0 for c in 'abcd'}

output_limit = 20

class LastOutput(Exception):
    pass

def get_value(spec: str) -> int:
    if spec in registers:
        return registers[spec]
    return int(spec)

inst_mapping = {
    'inc': 'dec',
    'dec': 'inc',
    'tgl': 'inc',
    'jnz': 'cpy',
    'cpy': 'jnz',
}

debug = False

def print_section(pointer: int, length: int) -> None:
    if debug is False:
        return
    print(f"===section {pointer} for {length}===")
    for i in range(pointer, pointer + length):
        print(f"{i}: {commands[i]} {arguments[i]}")

def is_addition(pointer: int) -> Union[Literal[False], int]:
    inst_chain = commands[pointer:]

    def check_section(dec_line: int) -> Union[Literal[False], int]:
        # print(f"found addition inst chain at {pointer}")
        # print_section(pointer, 3)
        next_args = arguments[pointer:pointer+3]
        # print(next_args)
        if next_args[dec_line][0] != next_args[2][0]:
            print(f"1 {next_args[dec_line][0]} != 2 {next_args[2][0]}")
            return False
        if next_args[2][1] != '-2':
            print(f"jump {next_args[2][1]} != -2")
            return False
        return dec_line
    if inst_chain[0:3] == ['inc', 'dec', 'jnz']:
        return check_section(1)
    elif inst_chain[0:3] == ['dec', 'inc', 'jnz']:
        return check_section(0)
    return False


def is_multiplication(pointer: int) -> Union[Literal[False], int]:
    inst_chain = commands[pointer:]
    if inst_chain[0:6] == ['cpy', 'inc', 'dec', 'jnz', 'dec', 'jnz']:
        # print(f"found multiplication inst chain at {pointer}")
        # print_section(pointer, 6)
        addition_dec_line = is_addition(pointer + 1)
        if addition_dec_line is False:
            print("subcommand is not addition")
            return False
        dec_line = addition_dec_line + 1
        next_args = arguments[pointer:pointer+6]
        if next_args[4][0] != next_args[5][0]:
            print(f"4 {next_args[4][0]} != 5 {next_args[5][0]}")
            return False
        if next_args[5][1] != '-5':
            print(f"final jnz {next_args[5][1]} != -5")
            return False
        if next_args[0][1] != next_args[dec_line][0]:
            print(f"counter mismatch: {next_args[0][1]} != {next_args[dec_line][0]}")
            return False
        return dec_line
    return False


def parse_line() -> None:
    global ip
    global output
    # print(f"parsing {ip} {commands[ip]} {arguments[ip]} {[registers[x] for x in 'abcd']}")
    if (dec_line := is_multiplication(ip)):
        next_args = arguments[ip:ip+6]
        # accum += a * b, zero b and buffer
        a, accum, buffer, b = [next_args[i][0] for i in [0, 3 - dec_line, dec_line, 4]]
        if debug:
            print(f"{ip}: {accum} += {a} * {b} ({registers[accum]} += {get_value(a)} * {registers[b]})")
        registers[accum] += get_value(a) * registers[b]
        registers[b] = 0
        registers[buffer] = 0
        ip += 6
        return
    if (dec_line := is_addition(ip)) is not False:
        next_args = arguments[ip:ip+3]
        arg_order = [1 - dec_line, dec_line]
        # a += b
        a, b = [next_args[i][0] for i in arg_order]
        if debug:
            print(f"{ip}: {a} += {b} ({registers[a]} += { registers[b]})")
        registers[a] += registers[b]
        registers[b] = 0
        ip += 3
        return
    inst = commands[ip]
    args = arguments[ip]
    if inst == 'cpy':
        source: int = get_value(args[0])
        if debug:
            print(f"{ip}: {args[1]} = {args[0]} ({source})")
        registers[args[1]] = source
    elif inst == 'inc':
        a = args[0]
        if debug:
            print(f"{ip}: {a} up ({registers[a]} up)")
        registers[a] += 1
    elif inst == 'dec':
        a = args[0]
        if debug:
            print(f"{ip}: {a} dn ({registers[a]} dn)")
        registers[a] -= 1
    elif inst == 'jnz':
        test: int = get_value(args[0])
        if test != 0:
            jump: int = get_value(args[1])
            if debug:
                print(f"jump by {jump}")
            ip += jump
            # print_next_section()
            return
    elif inst == 'tgl':
        location = get_value(args[0]) + ip
        # print(f"toggle {location}")
        if 0 < location < len(instructions):
            command = commands[location]
            commands[location] = inst_mapping[command]
    elif inst == 'out':
        output += str(get_value(args[0]))
        if len(output) == output_limit:
            raise LastOutput(output)
    else:
        raise ValueError(f"bad instruction: {inst}")
    # print(f"ip: {ip} registers: {[registers[x] for x in 'abcd']}")
    ip += 1

output_sets: list[tuple[int, str]] = []
for start_value in range(30):
    registers['a'] = int(start_value)
    ip = 0
    output: str = ""
    try:
        while ip < len(instructions):
            parse_line()
    except LastOutput:
        output_sets.append((start_value, output))

for output_tuple in output_sets:
    print(output_tuple)

sections = set()
def print_next_section() -> None:
    i = ip
    print(f"start section at {i}")
    limit = -1
    section_text = []
    while i < len(instructions):
        print(i)
        if commands[i] == 'tgl':
            break
        if commands[i] == 'jnz':
            target = arguments[i][1]
            if target[0] != '-':
                break
            if int(target) <= limit:
                break
        section_text.append(f"{i}: {commands[i]} {arguments[i]}")
        i += 1
        limit -= 1
    section_tuple = tuple(section_text)
    if section_tuple not in sections:
        print(f"ip: {ip} registers: {[registers[x] for x in 'abcd']}")
        print(*section_tuple, sep="\n")
        sections.add(section_tuple)

