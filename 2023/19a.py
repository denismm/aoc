#!/usr/bin/env python3
import sys
from typing import NamedTuple
from pprint import pprint
from copy import deepcopy
from functools import reduce
import re

filename = sys.argv[1]

# default rule has field of "" and comparison of ""
Rule = NamedTuple('Rule', [('field', str), ('comparison', str), ('value', int), ('dest', str)])

rule_re = re.compile(r'(\w+)([<=>])(\d+):(\w+)')
workflows: dict[str, list[Rule]] = {}

Item = dict[str, int]
items: list[Item] = []

with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        if line.startswith('{'):
            fields = line.strip('{}').split(',')
            item: Item = {}
            for field in fields:
                k, v = field.split('=')
                item[k] = int(v)
            items.append(item)
        elif line:
            name, rules_s = line.split('{')
            rules: list[Rule] = []
            for entry in rules_s.rstrip('}').split(','):
                m = rule_re.match(entry)
                if m:
                    field, comparison, value_s, dest = m.groups()
                    rules.append(Rule(field, comparison, int(value_s), dest))
                else:
                    rules.append(Rule("", "", 0, entry))
            workflows[name] = rules

def compare(input: int, comparison: str, value: int) -> bool:
    if comparison == '>':
        return input > value
    elif comparison == '=':
        return input == value
    elif comparison == '<':
        return input < value
    raise ValueError(f'bad comparison {comparison}')

# drop silly rules
for name, rules in workflows.items():
    while len(rules) >= 2:
        if rules[-1].field != "":
            raise ValueError(f"bad default at {name}")
        if rules[-2].dest == rules[-1].dest:
            rules.pop(-2)
        else:
            break

accepted: list[Item] = []
end_state = { 'R', 'A' }
for item in items:
    state = 'in'
    while state not in end_state:
        new_state = ""
        for rule in workflows[state]:
            if rule.field == '':
                new_state = rule.dest
                break
            else:
                if compare(item[rule.field], rule.comparison, rule.value):
                    new_state = rule.dest
                    break
        if new_state == "":
            raise ValueError(f'no matching rule for {state}')
        state = new_state
    if state == 'A':
        accepted.append(item)
total = sum([sum(item.values()) for item in accepted])
print(total)

# combos
def set_compare(input_set: set[int], comparison: str, value: int) -> tuple[set[int], set[int]]:
    passing_map: set[int] = set()
    if comparison == '>':
        passing_map = set(range(value + 1, 4001))
    elif comparison == '=':
        passing_map = {value}
    elif comparison == '<':
        passing_map = set(range(0, value))
    else:
        raise ValueError(f'bad comparison {comparison}')
    return (input_set & passing_map, input_set - passing_map)


all_combos: dict[str, set[int]] = { k: set(range(1, 4001)) for k in 'xmas'}
def valid_combos_for_state(state: str, input: dict[str, set[int]]) -> int:
    if state == 'R':
        return 0
    if state == 'A':
        lengths = [len(s) for s in input.values()]
        return reduce(lambda x, y: x*y, lengths)
    input = deepcopy(input)
    rules = workflows[state]
    valid_total = 0
    for rule in rules:
        if rule.field == '':
            valid_total += valid_combos_for_state(rule.dest, input)
        else:
            field_set = input[rule.field]
            passing_set, failing_set = set_compare(field_set, rule.comparison, rule.value)
            if passing_set:
                passing_input = input
                passing_input[rule.field] = passing_set
                valid_total += valid_combos_for_state(rule.dest, passing_input)
            if not failing_set:
                break
            # remainder goes to next rule
            input[rule.field] = failing_set
    return valid_total

print(valid_combos_for_state('in', all_combos))
