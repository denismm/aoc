#!/usr/bin/env python3
import sys
import re
import collections
import itertools
import pprint
import copy

filename = sys.argv[1]

floor_re = re.compile(r"The \w+ floor contains (.*)")
item_re = re.compile(r"(?:and )?an? (\w+)(\-compatible microchip| generator)")
separator_re = re.compile(r"\, |(?:\,? and )")

item_start = []

with open(filename, "r") as f:
    floor = 0
    for line in f:
        floor_set = set()
        floor += 1
        m = floor_re.match(line)
        if m:
            item_list = m.group(1)
            for item in separator_re.split(item_list):
                if item == "nothing relevant.":
                    continue
                m = item_re.match(item)
                if m:
                    (element, type_string) = m.groups()
                    if type_string == ' generator':
                        item_type = 0
                    else:
                        item_type = 1
                    floor_set.add((element, item_type))
                else:
                    raise ValueError(f"couldn't match {item}")
            item_start.append(floor_set)
        else:
            raise ValueError(f"can't parse line {line}")

first_state = item_start

def check_win(state):
    for i in range(3):
        if len(state[i]):
            return False
    return True

def check_safety(state):
    for floor_items in state:
        item_sets = [set(), set()]
        for (element, item_type) in floor_items:
            item_sets[item_type].add(element)
        (generators, chips) = item_sets
        if len(generators) == 0 or len(chips) == 0:
            # nothing to fry chips or no chips
            continue
        unshielded_chips = chips - generators
        if len(unshielded_chips) > 0:
            # print(f"unsafe: {unshielded_chips} and {generators}")
            return False
    return True

def print_history(history):
    for (steps, elevator, state) in history:
        print(f"step {steps}")
        print_state(elevator, state)

def print_state(elevator, state):
    print(f"elevator is {elevator}")
    for i, floor in enumerate(state):
        print(i, floor)

def freeze(elevator, state):
    return (elevator, tuple([frozenset(x) for x in state]))

# find shortest path
queue = collections.deque([(0, 0, first_state, [])])
seen = set([freeze(0, first_state)])
current_round = -1
while (queue):
    steps, elevator, state, history = queue.popleft()
    if steps != current_round:
        print(f"round {steps}: {len(queue) + 1}")
        current_round = steps
    new_history = history + [(steps, elevator, state)]
    items_here = state[elevator]
    basket_options = list(itertools.combinations(items_here, 1))
    basket_options += list(itertools.combinations(items_here, 2))
    floor_options = [elevator + x for x in [-1, 1] if 0 <= elevator + x <= 3]
    new_steps = steps + 1
    # print(f"{len(basket_options)} baskets, {len(floor_options)} floors")
    for basket in basket_options:
        for floor in floor_options:
            new_state = copy.deepcopy(state)
            for item in basket:
                new_state[elevator].remove(item)
                new_state[floor].add(item)
            frozen = freeze(floor, new_state)
            if frozen in seen:
                continue
            seen.add(frozen)
            if check_win(new_state):
                print(f'win at {new_steps}!')
                # print_history(new_history)
                exit(0)
            if check_safety(new_state):
                # print_state(floor, new_state)
                queue.append( (new_steps, floor, new_state, new_history) )
