#!/usr/bin/env python3
import sys
from dataclasses import dataclass

filename = sys.argv[1]

@dataclass
class Node:
    children: list['Node']
    metadata: list[int]

with open(filename, 'r') as f:
    data = [int(s) for s in f.read().split()]


def read_tree(data: list[int]) -> tuple[Node, int]:
    total_metadata = 0
    c_count = data.pop(0)
    m_count = data.pop(0)
    node = Node([], [])
    for i in range(c_count):
        new_child, sub_sum = read_tree(data)
        node.children.append(new_child)
        total_metadata += sub_sum
    for i in range(m_count):
        node.metadata.append(data.pop(0))
    total_metadata += sum(node.metadata)
    return node, total_metadata

root, total = read_tree(data)
if len(data) > 0:
    raise ValueError(f"finished with {len(data)} extra")

def node_value(node: Node) -> int:
    if len(node.children) == 0:
        return sum(node.metadata)
    total = 0
    for m in node.metadata:
        if m <= len(node.children):
            total += node_value(node.children[m-1])
    return total

print(total)
print(node_value(root))
