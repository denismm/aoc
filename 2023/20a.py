#!/usr/bin/env python3
import sys
from typing import NamedTuple
from collections import defaultdict, deque
import re

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

# State of network is set of "on" flipflops (stored as "name")
# and set of conjunction-input pairs for which the conjunction
# remembers a high pulse from that input (stored as "conj input").
# Also broadcaster remembers whether last pulse is high or low
# and repeats it - include in set if high.
# Conveniently, starting state is an empty state.

network_state: set[str] = set()

live_modules: deque[str] = deque()

debug = 1

sent_pulses: list[int] = [0, 0]

def handle_pulse(source: str, dest: str, high: bool) -> None:
    # signal changes state
    sent_pulses[high] += 1
    pulse_name = ('low', 'high')[high]
    if debug:
        print(f"{source} -{pulse_name}-> {dest}")
    # output modules may not be in module list
    # we don't do anything with them
    if dest not in modules:
        if debug:
            print(f"module {dest} recieved {pulse_name}")
        return
    dest_module = modules[dest]
    if dest_module.type == '%':
        if high:
            # don't even activate it
            return
        else:
            network_state.symmetric_difference_update({dest})
    elif dest_module.type == '&':
        key = f"{dest} {source}"
        if high:
            network_state.add(key)
        else:
            network_state.discard(key)
    elif dest_module.type == "":
        if high:
            network_state.add(dest)
        else:
            network_state.discard(dest)
    else:
        raise ValueError(f"mysterious module {dest}: {dest_module}")
    # signal queues module to act
    live_modules.append(dest)

def handle_activate(module_name: str) -> None:
    high_pulse: bool = False
    module = modules[module_name]
    if debug >= 2:
        print(f"handling module {module_name}: {module}")
    if module.type == '%':
        high_pulse = module_name in network_state
    elif module.type == '&':
        if debug >= 2:
            memory = [x for x in network_state if x.startswith(module_name)]
            print(f"{module_inputs[module_name]=} {memory=}")
        for input in module_inputs[module_name]:
            if f"{module_name} {input}" not in network_state:
                high_pulse = True
                break
    elif module.type == "":
        high_pulse = module_name in network_state

    for dest in module.destinations:
        handle_pulse(module_name, dest, high_pulse)

# button-presses
loop_size = 0
seen_states: dict[frozenset[str], int] = {}
for i in range(1000):

    frozen_state = frozenset(network_state)
    if False and frozen_state in seen_states:
        loop_start = seen_states[frozen_state]
        print(f"loop found from {i} to {loop_start}")
        if loop_start != 0:
            raise ValueError("strange loop")
        loop_size = i
        break
    seen_states[frozen_state] = i

    handle_pulse('button', 'broadcaster', False)
    while (live_modules):
        handle_activate(live_modules.popleft())
    if debug:
        print(network_state)

if loop_size > 0:
    repeats = 1000 / loop_size
else:
    repeats = 1
print(sent_pulses)
print(sent_pulses[0] * sent_pulses[1] * repeats * repeats)
