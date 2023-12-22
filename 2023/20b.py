#!/usr/bin/env python3
import sys
import re
from typing import NamedTuple
from collections import defaultdict, deque
from copy import deepcopy
from pprint import pprint

# make up fake structures to see what they do

debug: set[str] = set()

# broadcaster has type of ""
Module = NamedTuple('Module', [('type', str), ('destinations', list[str])])

Modules = dict[str, Module]

module_re = re.compile(r'([\%\&]?)(\w+) -> ([\w, ]+)$')

class Machine(object):
    def __init__(self, modules: Modules):
        self.modules = modules

        self.network_state: set[str] = set()
        self.live_modules: deque[str] = deque()

        module_inputs: dict[str, set[str]] = defaultdict(set)
        for k, module in modules.items():
            for dest in module.destinations:
                module_inputs[dest].add(k)
        self.module_inputs = dict(module_inputs)

    # return true if low output is sent
    def handle_pulse(self, source: str, dest: str, high: bool, i: int) -> bool:
        # signal changes state
        pulse_name = ('low', 'high')[high]
        if 'pulse' in debug:
            print(f"{source} -{pulse_name}-> {dest}")
        # output modules may not be in module list
        # we don't do anything with them
        if dest not in self.modules:
            if dest != 'output':
                raise ValueError(f"unexpected output node {dest}")
            if 'output' in debug:
                print(f"module {dest} recieved {pulse_name}")
            return not high
        dest_module = self.modules[dest]
        if dest_module.type == '%':
            if high:
                # don't even activate it
                return False
            else:
                self.network_state.symmetric_difference_update({dest})
        elif dest_module.type == '&':
            key = f"{dest} {source}"
            if high:
                self.network_state.add(key)
            else:
                self.network_state.discard(key)
        elif dest_module.type == "":
            if high:
                self.network_state.add(dest)
            else:
                self.network_state.discard(dest)
        else:
            raise ValueError("shouldn't get here")
        # signal queues module to act
        self.live_modules.append(dest)
        return False

    # pass along result from pulses
    def handle_activate(self, module_name: str, i: int) -> bool:
        high_pulse: bool = False
        module = self.modules[module_name]
        if 'handle' in debug:
            print(f"handling module {module_name}: {module}")
        if module.type == '%':
            high_pulse = module_name in self.network_state
        elif module.type == '&':
            if 'conj' in debug:
                memory = [x for x in self.network_state if x.startswith(module_name)]
                print(f"{self.module_inputs[module_name]=} {memory=}")
            for input in self.module_inputs[module_name]:
                if f"{module_name} {input}" not in self.network_state:
                    high_pulse = True
                    break
        elif module.type == "":
            high_pulse = module_name in self.network_state

        result = False
        for dest in module.destinations:
            if self.handle_pulse(module_name, dest, high_pulse, i):
                result = True
        return result

    # button-presses
    def analyze_structure(self) -> tuple[set[int], int, int]:
        loop_start = -1
        loop_end = -1
        seen_states: dict[frozenset[str], int] = {}
        successes: set[int] = set()
        for i in range(100_000_000):
            if loop_end == -1:
                frozen_state = frozenset(self.network_state)
                if frozen_state in seen_states:
                    loop_start = seen_states[frozen_state]
                    loop_end = i
                    # print(f"loop found from {i} to {loop_start}")
                    break
                seen_states[frozen_state] = i

            self.handle_pulse('button', 'broadcaster', False, i)
            while (self.live_modules):
                if self.handle_activate(self.live_modules.popleft(), i):
                    successes.add(i)
            if 'state' in debug:
                print(i, sorted(self.network_state))
        return (successes, loop_start, loop_end)

for filename in sys.argv[1:]:
    modules: Modules = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            if m := module_re.match(line):
                modtype, modname, dest_info = m.groups()
                destinations = dest_info.split(', ')
                module = Module(modtype, destinations)
                modules[modname] = module
            else:
                raise ValueError(f"can't parse line {line}")

    machine = Machine(modules)
    info = machine.analyze_structure()
    print(f'{filename}:\t {info[1]} {info[2] - info[1]}\t{sorted(info[0])[:10]}')
