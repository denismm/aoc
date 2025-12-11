#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from itertools import combinations

filename = sys.argv[1]

@dataclass(repr=True)
class Machine:
    n: int
    target: set[int]
    buttons: list[set[int]]
    joltages: list[int]

machines: list[Machine] = []
with open(filename, 'r') as f:
    for line in f:
        segments: list[str] = line.rstrip().split()
        light_s = segments.pop(0)
        joltage_s = segments.pop()
        light_s = light_s.strip('[]')
        n = len(light_s)
        target = { p for p, c in enumerate(light_s) if c == '#' }
        joltage_s = joltage_s.strip('{}')
        joltages = [int(s) for s in joltage_s.split(',')]
        buttons: list[set[int]] = []
        for button_s in segments:
            button_s = button_s.strip('()')
            buttons.append( { int(s) for s in button_s.split(',') } )
        machines.append(Machine(n, target, buttons, joltages))

total_presses = 0

class Solution(Exception):
    pass
for machine in machines:
    try:
        for press_n in range(len(machine.buttons) + 1):
            for combo in combinations(machine.buttons, press_n):
                lights: set[int] = set()
                for button in combo:
                    lights ^= button
                if lights == machine.target:
                    raise Solution(press_n)
    except Solution as e:
        total_presses += e.args[0]
        continue
    raise ValueError(f"no solution for machine {machine}")

print(total_presses)
