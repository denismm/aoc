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

with open(filename, 'r') as f:
    for line in f:
        (target, dir, amtstr, _, compreg, comparison, conststr) = line.split()
        amount = int(amtstr)
        constant = int(conststr)

        # check if comparison met
        comparison_value = registers[compreg]
        func = get_comparison_func(comparison)
        if func(comparison_value, constant):
            registers[target] += amount * dir_direction[dir]
    top_value = max(registers.values())
    top_register = [k for k,v in registers.items() if v == top_value][0]
    print(f"{top_register}: {top_value}")
