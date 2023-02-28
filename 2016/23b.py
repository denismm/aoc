#!/usr/bin/env python3
import sys

filename = sys.argv[1]
egg_count = sys.argv[2]

with open(filename, "r") as f:
    instructions: list[list[str]] = [line.rstrip().split() for line in f]
commands = [inst[0] for inst in instructions]
arguments = [inst[1:] for inst in instructions]
registers: dict[str, int] = {c: 0 for c in 'abcd'}
# set up eggs
registers['a'] = int(egg_count)
ip = 0


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

def is_addition(pointer):
    inst_chain = commands[pointer:]
    if inst_chain[0:3] == ['inc', 'dec', 'jnz']:
        next_args = arguments[ip:ip+3]
        if next_args[1][0] == next_args[2][0] and next_args[2][1] == '-2':
            return True

def is_multiplication(pointer):
    inst_chain = commands[pointer:]
    if inst_chain[0:6] == ['cpy', 'inc', 'dec', 'jnz', 'dec', 'jnz']:
        if is_addition(pointer + 1):
            next_args = arguments[ip:ip+6]
            if next_args[4][0] == next_args[5][0] and next_args[5][1] == '-5' and next_args[0][1] == next_args[2][0]:
                return True


def parse_line() -> None:
    global ip
    if is_multiplication(ip):
        next_args = arguments[ip:ip+6]
        # accum += a * b
        accum = next_args[1][0]
        a, b = next_args[2][0], next_args[0][0]
        registers[accum] += registers[a] * registers[b]
        registers[a] = 0
        registers[b] = 0
        ip += 6
        return
    if is_addition(ip):
        next_args = arguments[ip:ip+3]
        registers[next_args[0][0]] += registers[next_args[1][0]]
        registers[next_args[1][0]] = 0
        ip += 3
        return
    inst = commands[ip]
    args = arguments[ip]
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
            print_next_section()
            return
    elif inst == 'tgl':
        location = get_value(args[0]) + ip
        # print(f"toggle {location}")
        if 0 < location < len(instructions):
            command = commands[location]
            commands[location] = inst_mapping[command]
    else:
        raise ValueError(f"bad instruction: {inst}")
    # print(f"ip: {ip} registers: {[registers[x] for x in 'abcd']}")
    ip += 1

sections = set()
def print_next_section():
    i = ip
    limit = -1
    section_text = []
    while i < len(instructions):
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

while ip < len(instructions):
    parse_line()

print(registers['a'])
# print(*(list(enumerate(instructions))), sep="\n")
