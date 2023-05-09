#!/usr/bin/env python3
import sys
from collections import defaultdict
from typing import DefaultDict, Callable

filename = sys.argv[1]

registers: DefaultDict[str, int] = defaultdict(lambda: 0)

def get_comparison_func(comparison: str) -> Callable[[int, int], bool]:
    func_dict = {
        '>': lambda a, b: a > b,
        '<': lambda a, b: a < b,
        '>=': lambda a, b: a >= b,
        '<=': lambda a, b: a <= b,
        '==': lambda a, b: a == b,
        '!=': lambda a, b: a != b,
    }
    return func_dict[comparison]

dir_direction = {'inc': 1, 'dec': -1}

def get_top() -> tuple[str, int]:
    top_value = max(registers.values())
    top_register = [k for k,v in registers.items() if v == top_value][0]
    return (top_register, top_value)

with open(filename, 'r') as f:
    ever_top_reg = ''
    ever_top_value = 0  # they're all currently 0

    for line in f:
        (target, dir, amtstr, _, compreg, comparison, conststr) = line.split()
        amount = int(amtstr)
        constant = int(conststr)

        # check if comparison met
        comparison_value = registers[compreg]
        func = get_comparison_func(comparison)
        if func(comparison_value, constant):
            registers[target] += amount * dir_direction[dir]
        current_top_reg, current_top_value = get_top()
        if current_top_value > ever_top_value:
            ever_top_value, ever_top_reg = current_top_value, current_top_reg

    top_register, top_value = get_top()
    print(f"Ever: {ever_top_reg}: {ever_top_value}")
    print(f"Now: {top_register}: {top_value}")
