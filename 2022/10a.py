#!/usr/bin/env python3
import sys

filename = sys.argv[1]
with open(filename, "r") as f:
    register: int = 1
    data: dict[str, int] = {"now": 1, "total": 0}

    def tick() -> None:
        data['now'] += 1
        if data['now'] % 40 == 20:
            print(register, register * data['now'])
            data['total'] += register * data['now']

    for line in f:
        if line.startswith('noop'):
            tick()
        elif line.startswith('addx'):
            tick()
            argument = line.split()[1]
            # print(f"adding {argument}")
            register += int(argument)
            tick()
        else:
            raise ValueError(f"bad line {line}")
    print(data['total'])
