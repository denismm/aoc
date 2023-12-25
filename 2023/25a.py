#!/usr/bin/env python3
import sys
import graphviz         # type: ignore [import-untyped]

filename = sys.argv[1]

connections: set[tuple[str, ...]] = set()
nodes: set[str] = set()
with open(filename, "r") as f:
    for line in f:
        source, target_s = line.split(':')
        nodes.add(source)
        targets = target_s.split()
        for target in targets:
            nodes.add(target)
            connection = tuple(sorted([source, target]))
            connections.add(connection)

dot = graphviz.Graph("AoC 25")
for node in nodes:
    dot.node(node)
for connection in connections:
    dot.edge(*connection)
print(dot.source)

# > ./25a.py 25.input.txt > 25.input.dot
# > dot -Tpng 25.input.dot > 25.input.png
#       from inspection, there are three lines between the two large sections
#       and the nodes on either side of that connection are hpq and fgd
# > dot -Tplain 25.input.dot > 25.input.plain
# > grep 'node hpq' 25.input.plain
# node hpq 370.58 8.25 0.75 0.5 hpq solid ellipse black lightgrey
# > grep 'node fgd' 25.input.plain
# node fgd 374.35 10.25 0.75 0.5 fgd solid ellipse black lightgrey
# > grep node 25.input.plain | sort -k3 -n > 25.nodes.x
# > wc -l 25.nodes.x
#     1461 25.nodes.x
# > grep -n -A1 hpq 25.nodes.x
# 732:node hpq 370.58 8.25 0.75 0.5 hpq solid ellipse black lightgrey
# 733-node fgd 374.35 10.25 0.75 0.5 fgd solid ellipse black lightgrey
#       1461 - 732 = 729
#       732 * 729 = 533628
