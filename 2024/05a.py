#!/usr/bin/env python3
import sys
filename = sys.argv[1]

orderings: list[tuple[int, ...]] = []
middle_sum = 0
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
                middle_sum += middle
print(middle_sum)
