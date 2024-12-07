#!/usr/bin/env python3
import sys
from itertools import product
from tqdm import tqdm
filename = sys.argv[1]

operators = "+*|"
calibration = 0

with open(filename, "r") as f:
    for line in tqdm(f):
        target_s, equation_s = line.split(':')
        target = int(target_s)
        equation = [int(s) for s in equation_s.split()]
        op_n = len(equation) - 1
        start = equation.pop(0)
        for op_seq in product(operators, repeat=op_n):
            result = start
            for (op, arg) in zip(op_seq, equation):
                if op == '*':
                    result *= arg
                elif op == '+':
                    result += arg
                elif op == '|':
                    result = int(str(result) + str(arg))
            if result == target:
                calibration += target
                break
print(calibration)
