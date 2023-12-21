#!/usr/bin/env python3
import sys
from typing import NamedTuple
from collections import defaultdict
import re
import graphviz

filename = sys.argv[1]

# broadcaster has type of ""
Module = NamedTuple('Module', [('type', str), ('destinations', tuple[str, ...])])

module_re = re.compile(r'([\%\&]?)(\w+) -> ([\w, ]+)$')
modules: dict[str, Module] = {}

with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        if m := module_re.match(line):
            modtype, modname, dest_info = m.groups()
            destinations = tuple(dest_info.split(', '))
            module = Module(modtype, destinations)
            modules[modname] = module
        else:
            raise ValueError(f"can't parse line {line}")

# we also need to know all inputs for conjunction modules

module_inputs: dict[str, set[str]] = defaultdict(set)
for k, module in modules.items():
    for dest in module.destinations:
        module_inputs[dest].add(k)

module_inputs = dict(module_inputs)

# output dot

dot = graphviz.Digraph("AoC 20")
all_nodes = set(modules.keys())
all_nodes |= set(module_inputs.keys())
for node in all_nodes:
    prefix = ""
    if node in modules:
        prefix = modules[node].type
    dot.node(node, prefix + node)
for modname, module in modules.items():
    for dest in module.destinations:
        dot.edge(modname, dest)
print(dot.source)
