#!/usr/bin/env python3
import sys
from typing import NamedTuple
from collections import deque

filename = sys.argv[1]
Component = tuple[int, int]
pile: list[Component] = []

with open(filename, 'r') as f:
    for line in f:
        ports = line.rstrip().split('/')
        component: Component = (int(ports[0]), int(ports[1]))
        pile.append(component)

State = NamedTuple('State', [
    ('pile', tuple[Component, ...]),
    ('bridge', tuple[Component, ...])
])

original = State(tuple(pile), tuple())
queue: deque[State] = deque([original])

best_bridge: tuple[tuple[Component, ...], tuple[int, int]] = ( tuple(), (0, 0))

while queue:
    current = queue.popleft()
    if current.bridge:
        front = current.bridge[-1][-1]
    else:
        front = 0
    score = (len(current.bridge), sum([sum(c) for c in current.bridge]))
    if score > best_bridge[1]:
        best_bridge = (current.bridge, score)
    # find possible next steps
    for component in current.pile:
        if front in component:
            if front == component[0]:
                new_bridge = list(current.bridge) + [component]
            else:
                new_bridge = list(current.bridge) + [(component[1], component[0])]
            new_pile = list(current.pile)
            new_pile.remove(component)
            queue.append(State(tuple(new_pile), tuple(new_bridge)))

print(best_bridge)
