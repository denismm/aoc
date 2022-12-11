#!/usr/bin/env python3
import sys
import re
from typing import NamedTuple, Callable

Monkey = NamedTuple('Monkey', [
    ('items', list[int]),
    ('operation', Callable[[int], int]),
    ('test', int),
    ('dest', list[int]),
    ('inspections', list[int]),
])
monkeys: list[Monkey] = []

filename = sys.argv[1]
with open(filename, "r") as f:
    lines: list[str] = [line.rstrip() for line in f]
lines.append("")

items_re = re.compile(r'Starting items:\s([\d, ]*)')
list_re = re.compile(r'[,\s]+')
operation_re = re.compile(r'new = old (.*)')


def parse_operation(operation_str: str) -> Callable[[int], int]:
    if (m := operation_re.match(operation_str)):
        mutation = m.group(1)
        if mutation == '* old':
            def operation(x: int) -> int:
                return x*x
        else:
            operator, operand_str = mutation.split()
            operand = int(operand_str)
            if operator == '+':
                def operation(x: int) -> int:
                    return x + operand
            elif operator == '*':
                def operation(x: int) -> int:
                    return x * operand
            else:
                raise ValueError(f"bad mutation: {mutation}")
    else:
        raise ValueError(f"bad operation: {operation_str}")
    return operation


for i in range(len(lines) // 7):
    monkey_data = lines[i*7:(i+1)*7]
    if not monkey_data[0].startswith(f"Monkey {i}"):
        raise ValueError(f"wrong monkey: {monkey_data[0]} instead of {i}")
    if (m := items_re.search(monkey_data[1])):
        items: list[int] = [int(x) for x in list_re.split(m.group(1))]
    operation_str = monkey_data[2].split(': ')[1]
    operation = parse_operation(operation_str)
    test = int(monkey_data[3].split('divisible by ')[1])
    dest = [int(line.split('monkey ')[1]) for line in monkey_data[4:6]]
    monkeys.append(Monkey(items, operation, test, dest, [0]))

for _ in range(20):
    for i in range(len(monkeys)):
        monkey = monkeys[i]
        items = list(monkey.items)
        monkey.items.clear()
        for item in items:
            item = monkey.operation(item)
            monkey.inspections[0] += 1
            item //= 3
            if item % monkey.test == 0:
                monkeys[monkey.dest[0]].items.append(item)
            else:
                monkeys[monkey.dest[1]].items.append(item)

for i in range(len(monkeys)):
    print(f"Monkey {i}: {monkeys[i].inspections[0]}")
inspections = list(sorted([monkey.inspections[0] for monkey in monkeys]))
monkey_business = inspections[-1] * inspections[-2]
print(f"Monkey business: {monkey_business}")
