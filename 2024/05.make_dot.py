#!/usr/bin/env python3
import sys
import graphviz
filename = sys.argv[1]

dot = graphviz.Digraph("AoC 2024-05")
nodes: set[str] = set()
with open(filename, 'r') as f:
    for line in f:
        if "|" in line:
            ordering = line.rstrip().split('|')
            nodes.add(ordering[0])
            nodes.add(ordering[1])
            dot.edge(*ordering)
for node in nodes:
    dot.node(node)

print(dot.source)
