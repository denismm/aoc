#!/usr/bin/env python3
import sys
from collections import Counter, defaultdict

filename = sys.argv[1]
elves = int(sys.argv[2])
extra = int(sys.argv[3])

next_steps: dict[str, set[str]] = defaultdict(set)
all_steps: Counter[str] = Counter()
with open(filename, "r") as f:
    for line in f:
        tokens = line.split()
        prereq = tokens[1]
        postreq = tokens[7]
        next_steps[prereq].add(postreq)
        all_steps[prereq] = ord(prereq) - ord('@') + extra
        all_steps[postreq] = ord(postreq) - ord('@') + extra

current_tasks: set[str] = set()
time_spent: int = 0

while(all_steps):
    # assign tasks
    options = set(all_steps)
    for v in next_steps.values():
        options -= v
    options -= current_tasks
    while options and (len(current_tasks) < elves):
        step = sorted(options)[0]
        current_tasks.add(step)
        options.remove(step)
    if not current_tasks:
        raise ValueError("nobody working!")
    # complete tasks
    time_spent += 1
    for task in list(current_tasks):    # copy to list since we are mutating
        all_steps[task] -= 1
        if all_steps[task] == 0:
            del all_steps[task]
            current_tasks.remove(task)
            try:
                del next_steps[task]
            except KeyError:
                pass

print(time_spent)
