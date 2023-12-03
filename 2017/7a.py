#!/usr/bin/env python3
import sys
from collections import defaultdict
from typing import DefaultDict

filename = sys.argv[1]

parent: dict[str, str] = {}
children: dict[str, list[str]] = {}
weights: dict[str, int] = {}

with open(filename, 'r') as f:
    for line in f:
        (sections) = line.rstrip().split(' -> ')
        node_info = sections[0].split()
        node = node_info[0]
        weight = int(node_info[1][1:-1])
        weights[node] = weight
        if len(sections) > 1:
            node_children = sections[1].split(', ')
            for child in node_children:
                parent[child] = node
            children[node] = node_children
roots = set(weights.keys()) - set(parent.keys())
root = roots.pop()
print(root)

# check weights returns the weight of the whole tower
def check_weights(node_name: str) -> int:
    kids = children.get(node_name, [])
    kids_for_weight: DefaultDict[int, set[str]] = defaultdict(set)
    total = weights[node_name]
    for kid in kids:
        kid_weight = check_weights(kid)
        kids_for_weight[kid_weight].add(kid)
        total += kid_weight
    if len(kids_for_weight) > 1:
        weights_for_count = {len(ks): w for w, ks in kids_for_weight.items()}
        wrong_count = [count for count in weights_for_count.keys() if count > 1][0]
        wrong_weight = weights_for_count[1]
        right_weight = weights_for_count[wrong_count]
        print(f"wrong weight is {wrong_weight}, correct is {right_weight}")
        difference = right_weight - wrong_weight
        wrong_node = kids_for_weight[wrong_weight].pop()
        current_weight = weights[wrong_node]
        correct_weight = current_weight + difference
        print(f"{wrong_node} is {current_weight}, should be {correct_weight}")
        exit()
    return total

check_weights(root)
