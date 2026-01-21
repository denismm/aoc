#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from copy import deepcopy
from typing import Optional
from itertools import combinations_with_replacement, product
import math

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

def solve_matrix(wiring: list[list[int]]) -> list[list[int]]:
    a = deepcopy(wiring)
    # algorithm from wikipedia
    n = len(a)          # height of matrix
    m = len(a[0])       # width of matrix
    p_i = 0     # pivot row, goes to n
    p_j = 0     # pivot column, goes to m
    while p_i < n and p_j < m:
        # for r in a:
        #     print('\t'.join([str(x) for x in r]))
        p_i_max = max([(abs(a[i][p_j]), i) for i in range(p_i, n)])[1]
        # print(f"p_i is {p_i} of {n}, p_j is {p_j} of {m}, max is {p_i_max}")
        if a[p_i_max][p_j] == 0:        # no pivot in this column
            # print(f"no pivot in column {p_j} from row {p_i}")
            p_j += 1
        else:
            # swap rows
            # print(f"swapping {a[p_i]} and {a[p_i_max]}")
            (a[p_i], a[p_i_max]) = (a[p_i_max], a[p_i])
            # print(f"subtracting {a[p_i]}")
            for i in range(p_i + 1, n):         # each line
                num = a[i][p_j]
                denom = a[p_i][p_j]
                g = math.gcd(num, denom)
                # if denom > 1:
                #     print(f"target is {a[i]}")
                #     print(f"{num=} {denom=} {g=}")
                if g > 1:
                    num //= g
                    denom //= g
                # print(f"{f=} {a[i]=}")
                if (a[i][p_j] * denom) - a[p_i][p_j] * num != 0:
                    raise ValueError(f"bad division: {a[i][p_j]} {a[p_i][p_j]} {denom} / {num}")
                a[i][p_j] = 0   # we know this matches and is 0
                for j in range(p_j+1, m):
                    a[i][j] *= denom
                    a[i][j] -= a[p_i][j] * num
                # print(a[i])
                # if denom > 1:
                #     print(f"result is {a[i]}")
            p_i += 1
            p_j += 1
    return a

class PartialPress(Exception):
    pass

def find_presses(m: list[list[int]], limits: list[int]) -> Optional[dict[int, int]]:
    # return the smallest presses for the remaining matrix
    best_presses: Optional[dict[int, int]] = None
    while m and sum([abs(x) for x in m[-1]]) == 0:
        m.pop()
    if len(m) == 0:
        return {}        # 0 presses solves this config
    proc_line = m.pop()
    divisor = math.gcd(*proc_line)
    proc_line = [x // divisor for x in proc_line]
    target = proc_line.pop()
    if target < 0:
        target *= -1
        proc_line = [x * -1 for x in proc_line]
    inputs = [(col, x) for col, x in enumerate(proc_line) if x != 0]
    voids: list[int] = []
    for (col, x) in inputs:
        if x < 0:
            voids.append(col)
    buttons: list[int] = [col for col, x in inputs if col not in voids]
    # we want combinations of these
    # but the target might be raised by negative buttons
    negative_ranges: list[range] = []
    for void in voids:
        negative_ranges.append(range(limits[void] + 1))
    for negative_presses in product(*negative_ranges):
        local_target = target
        for b, p in zip(voids, negative_presses):
            local_target -= proc_line[b] * p
        for combo in combinations_with_replacement(buttons, local_target):
            try:
                raw_values: dict[int, int] = { button: 0 for button in (buttons + voids) }
                # TODO: get negatives in raw and also on other rows
                for button in combo:
                    raw_values[button] += 1
                press_values: dict[int, int] = {}
                for button, value in raw_values.items():
                    if value == 0:
                        press_values[button] = 0
                    elif value % proc_line[button] != 0:
                        raise PartialPress()
                    else:
                        press_values[button] = value // proc_line[button]
                for b, p in zip(voids, negative_presses):
                    press_values[b] = p
            except PartialPress:
                # invalid combo
                continue
            new_m = deepcopy(m)
            for button, presses in press_values.items():
                for line in new_m:
                    line[-1] -= line[button] * presses
                    line[button] = 0
            result = find_presses(new_m, limits)
            if result is None:
                continue
            result.update(press_values)
            if best_presses is None or sum(result.values()) < sum(best_presses.values()):
                best_presses = result
    return best_presses

for machine in machines:
    joltages = machine.joltages
    buttons = machine.buttons
    wiring: list[list[int]] = [ [0] * (len(buttons) + 1) for _ in joltages]
    button_limits: list[int] = []
    for i, button in enumerate(buttons):
        # print(i, button)
        for light in button:
            wiring[light][i] = 1
        button_limits.append(min([j for l, j in enumerate(joltages) if l in button]))
    for light, joltage in enumerate(joltages):
        wiring[light][-1] = joltage
    a = solve_matrix(wiring)
    # for row in a:
    #     print([int(x) for x in row])

    answer_matrix: list[list[int]] = a
    print(machine)
    # for row in answer_matrix:
    #     print(row)
    best_presses = find_presses(deepcopy(answer_matrix), button_limits)
    print(best_presses)
    if best_presses is None:
        raise ValueError(f"no solution for machine {machine}")
    total_presses += sum(best_presses.values())

print(total_presses)
