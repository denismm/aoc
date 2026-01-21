#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Optional
from copy import deepcopy

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

Wiring = list[list[int]]

class Solution(Exception):
    pass

def solve_machine(wiring: Wiring, m: Machine, presses: list[Optional[int]]) -> None:
    # recursive solve
    big_buttons = max([(len(m.buttons[i]), i) for i in range(len(presses)) if presses[i] is None])
    button = big_buttons[1]
    biggest_press = min([m.joltages[i] for i in m.buttons[button]])
    for press in range(biggest_press, -1, -1):
        new_wiring = deepcopy(wiring)
        new_m = deepcopy(m)
        new_presses = deepcopy(presses)

        class NoSolution(Exception):
            pass

        def apply_button(b: int, p: int) -> None:
            # print(f"pressing button {b} {p} times ({buttons[b]})")
            if new_presses[b] is not None:
                raise ValueError(f"re-press of button {b}")
            for counter in buttons[b]:
                # print(f"handling counter {counter}")
                new_m.joltages[counter] -= p
                if new_m.joltages[counter] < 0:
                    # bad solution
                    raise NoSolution(new_m.joltages)
                new_wiring[counter][b] = 0
            new_presses[b] = p

        apply_button(button, press)
        counter = 0
        try:
            while counter < len(new_m.joltages):
                # print(f"counter {counter}: {new_wiring[counter]}")
                if sum(new_wiring[counter]) == 1:
                    # this button is solveable
                    sub_button = new_wiring[counter].index(1)
                    apply_button(sub_button, new_m.joltages[counter])
                    # restart
                    counter = 0
                else:
                    counter += 1
            # do we have a solution?
            if sum(new_m.joltages) == 0:
                raise Solution(new_presses)
            # have we run out of options?
            if None not in new_presses:
                raise NoSolution(new_m.joltages)
            # otherwise recurse
            # print(new_presses)
            solve_machine(new_wiring, new_m, new_presses)
        except NoSolution:
            continue    # try another number of presses

for machine_i, machine in enumerate(machines):
    joltages = machine.joltages
    buttons = machine.buttons
    wiring: Wiring = [ [0] * len(buttons) for _ in joltages]
    for b, counters in enumerate(buttons):
        # print(b, counters)
        for counter in counters:
            wiring[counter][b] = 1
    try:
        solve_machine(wiring, machine, [None] * len(buttons))
        raise ValueError("no solution found")
    except Solution as e:
        # print(e.args)
        solution = sum(e.args[0])
        # check solution
        results: list[int] = [0] * len(machine.joltages)
        for press, counters in zip(e.args[0], machine.buttons):
            for counter in counters:
                results[counter] += press
        if results != machine.joltages:
            print(f"incorrect solution: {results} != {machine.joltages}")
        print(machine_i, machine.joltages, e.args[0], solution)
        total_presses += solution

print(total_presses)
