#!/usr/bin/env python3
import sys
from collections import defaultdict
filename = sys.argv[1]

orderings: list[tuple[int, ...]] = []
right_middle_sum = 0
wrong_middle_sum = 0
# sorting code borrowed from 2018-05

def make_full_ordering(orderings: list[tuple[int, ...]]) -> list[int]:
    next_steps: dict[int, set[int]] = defaultdict(set)
    all_steps: set[int] = set()
    for prereq, postreq in orderings:
        next_steps[prereq].add(postreq)
        all_steps.add(prereq)
        all_steps.add(postreq)

    order: list[int] = []

    while (all_steps):
        options = set(all_steps)
        for v in next_steps.values():
            options -= v
        if not options:
            raise ValueError(f"no options: {order=} {all_steps=}")
        step = sorted(options)[0]
        order.append(step)
        all_steps.remove(step)
        try:
            del next_steps[step]
        except KeyError:
            pass
    return order

order_key: dict[int, int] = {}
with open(filename, 'r') as f:
    for line in f:
        if "|" in line:
            ordering = tuple([int(s) for s in line.split('|')])
            orderings.append(ordering)
        elif "," in line:
            pages = [int(s) for s in line.split(',')]
            for first, second in orderings:
                if first in pages and second in pages:
                    if pages.index(first) > pages.index(second):
                        break
            else:       # no breaks
                middle = pages[len(pages) // 2]
                right_middle_sum += middle
                continue
            # if we got here, order is wrong
            local_orderings = [o for o in orderings if o[0] in pages and o[1] in pages]
            full_order = make_full_ordering(local_orderings)
            order_key = { k: v for v, k in enumerate(full_order) }
            pages.sort(key=lambda x: order_key[x])
            middle = pages[len(pages) // 2]
            wrong_middle_sum += middle

print(right_middle_sum)
print(wrong_middle_sum)
