#!/usr/bin/env python3
import sys

filename = sys.argv[1]
egg_count = sys.argv[2]

with open(filename, "r") as f:
    instructions: list[list[str]] = [line.rstrip().split() for line in f]
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
    inst_chain = [ inst[0] for inst in instructions[pointer:] ]
    if inst_chain[0:3] == ['inc', 'dec', 'jnz']:
        next_set = instructions[ip:ip+3]
        if next_set[1][1] == next_set[2][1] and next_set[2][2] == '-2':
            return True

def is_multiplication(pointer):
    inst_chain = [ inst[0] for inst in instructions[pointer:] ]
    if inst_chain[0:6] == ['cpy', 'inc', 'dec', 'jnz', 'dec', 'jnz']:
        if is_addition(pointer + 1):
            next_set = instructions[ip:ip+6]
            if next_set[4][1] == next_set[5][1] and next_set[5][2] == '-5' and next_set[0][2] == next_set[2][1]:
                return True


def parse_line() -> None:
    global ip
    if is_multiplication(ip):
        next_set = instructions[ip:ip+6]
        # accum += a * b
        accum = next_set[1][1]
        a, b = next_set[2][1], next_set[0][1]
        registers[accum] += registers[a] * registers[b]
        registers[a] = 0
        registers[b] = 0
        ip += 6
        return
    if is_addition(ip):
        next_set = instructions[ip:ip+3]
        registers[next_set[0][1]] += registers[next_set[1][1]]
        registers[next_set[1][1]] = 0
        ip += 3
        return
    components = instructions[ip]
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
            # print_next_section()
            return
    elif inst == 'tgl':
        location = get_value(args[0]) + ip
        # print(f"toggle {location}")
        if 0 < location < len(instructions):
            command = instructions[location][0]
            instructions[location][0] = inst_mapping[command]
            # print(f"command at {location} now {instructions[location][0]} ")
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
        if instructions[i][0] == 'tgl':
            break
        if instructions[i][0] == 'jnz':
            target = instructions[i][2]
            if target[0] != '-':
                break
            if int(target) <= limit:
                break
        section_text.append(f"{i}: {instructions[i]}")
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
