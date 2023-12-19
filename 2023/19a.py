#!/usr/bin/env python3
import sys
from typing import NamedTuple
from pprint import pprint
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

pprint(workflows)
