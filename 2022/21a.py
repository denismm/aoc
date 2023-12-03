#!/usr/bin/env python3
import sys
import re
from typing import NamedTuple, Callable

number_re = re.compile(r'[\d]+$')

MonkeyRule = NamedTuple("MonkeyRule", [('operation', str), ('operands', list[str])])

number_monkeys: dict[str, int] = {}
rule_monkeys: dict[str, MonkeyRule] = {}

def division(inputs: list[int]) -> int:
    if inputs[0] % inputs[1] == 0:
        return inputs[0] // inputs[1]
    else:
        raise ValueError(f"non-integer division between {inputs}")

calculation: dict[str, Callable[[list[int]], int]] = {
    '+': (lambda inputs: sum(inputs)),
    '-': (lambda inputs: inputs[0] - inputs[1]),
    '*': (lambda inputs: inputs[0] * inputs[1]),
    '/': division,
}

filename = sys.argv[1]
with open(filename, "r") as f:
    for line in f:
        monkey_name, monkey_job = line.rstrip().split(': ')
        if number_re.match(monkey_job):
            number_monkeys[monkey_name] = int(monkey_job)
        else:
            equation = monkey_job.split()
            rule_monkeys[monkey_name] = MonkeyRule(equation[1], equation[0::2])

while rule_monkeys:
    print(f"monkeys: {len(number_monkeys)} / {len(rule_monkeys)}")
    rule_monkey_names = list(rule_monkeys.keys())
    for monkey_name in rule_monkey_names:
        rule = rule_monkeys[monkey_name]
        try:
            inputs = [number_monkeys[operand] for operand in rule.operands]
        except KeyError:
            continue
        number_monkeys[monkey_name] = calculation[rule.operation](inputs)
        del rule_monkeys[monkey_name]
    if 'root' in number_monkeys:
        print(number_monkeys['root'])
        exit(0)
