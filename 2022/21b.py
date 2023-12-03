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
    'backsub': (lambda inputs: inputs[1] - inputs[0]),
    'backdiv': (lambda inputs: division(list(reversed(inputs)))),
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

# fix elephant mistakes
root_monkey = rule_monkeys['root']
rule_monkeys['root'] = MonkeyRule('=', root_monkey.operands)
# we don't care about humn monkey value
del number_monkeys['humn']

# invert to humn
pointer = 'humn'
humn_track: list[str] = ['humn']
while (pointer != 'root'):
    referents = [k for k, v in rule_monkeys.items() if pointer in v.operands]
    pointer = referents[0]
    humn_track.append(pointer)
print(humn_track)

inversions: dict[str, dict[bool, str]] = {
    '+': { True: '-', False: '-'},
    '*': { True: '/', False: '/'},
    '-': { True: '+', False: 'backsub'},
    '/': { True: '*', False: 'backdiv'},
}
def invert_operation(operation: str, forward: bool) -> str:
    return inversions[operation][forward]

while len(humn_track) > 2:
    top_name = humn_track.pop()
    next_name = humn_track[-1]
    third_name = humn_track[-2]
    top_monkey = rule_monkeys[top_name]
    next_monkey = rule_monkeys[next_name]
    next_operation = next_monkey.operation
    # we don't care about the order of the top two
    next_position = top_monkey.operands.index(next_name)
    other_equal_monkey = top_monkey.operands[1 - next_position]
    # we do care about the order of the third
    third_position = next_monkey.operands.index(third_name)
    other_operation_monkey = next_monkey.operands[1 - third_position]
    new_operation = invert_operation(next_operation, (third_position == 0))
    new_top_monkey = MonkeyRule(new_operation, [other_equal_monkey, other_operation_monkey])
    rule_monkeys[top_name] = new_top_monkey
    new_next_monkey = MonkeyRule('=', [third_name, top_name])
    rule_monkeys[next_name] = new_next_monkey

equality_monkey = humn_track[1]
print(rule_monkeys[equality_monkey])
target_monkey = rule_monkeys[equality_monkey].operands[1]
print(target_monkey)
del rule_monkeys[equality_monkey]

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
    if target_monkey in number_monkeys:
        print(number_monkeys[target_monkey])
        exit(0)
