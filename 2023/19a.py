#!/usr/bin/env python3
import sys
from typing import NamedTuple

filename = sys.argv[1]

# default rule has field of "" and comparison of ""
Rule = NamedTuple('Rule', [('field', str), ('comparison', str), ('value', int), ('dest', str)])
workflows: dict[str, list[Rule]] = {}

Item = dict[str, int]
items: list[Item] = []

with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        if line.startswith('{'):
            print(line.strip('{}').split(','))
            item = {field: 0 
                for field in line.strip('{}').split(',')
                for (k, v) in field.split('=') 
            }
            items.append(item)

print(items)
