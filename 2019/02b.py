#!/usr/bin/env python3

import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    start_memory: list[int] = [int(s) for s in f.read().rstrip().split(',')]

opcodes: dict[int, str] = {
    1: "+",
    2: "*",
    99: "halt",
}


def try_input(noun: int, verb: int) -> int:
    memory = list(start_memory)
    memory[1] = noun
    memory[2] = verb
    ip = 0
    while True:
        operation, a_addr, b_addr, out_addr = memory[ip:ip+4]
        action = opcodes[operation]
        if action == 'halt':
            break
        a = memory[a_addr]
        b = memory[b_addr]
        if action == '+':
            out = a + b
        elif action == '*':
            out = a * b
        else:
            raise ValueError(f"unknown opcode at {ip=} {action=}")
        # print(f"{action} {a_addr} {b_addr} -> {out_addr} ({a} {b} -> {out})")
        memory[out_addr] = out
        ip += 4
    return memory[0]

# closest = 1000
target = 19690720
for n in range(100):
    for v in range(100):
        result = try_input(n, v)
        # closeness = abs(result - target)
        # if closeness < closest:
        if result == target:
            # closest = closeness
            print(n, v, 100*n + v, result, target - result)
