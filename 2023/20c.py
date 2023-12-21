#!/usr/bin/env python3
from typing import NamedTuple
from collections import defaultdict, deque
from copy import deepcopy
from pprint import pprint

# make up fake structures to see what they do

debug: set[str] = set()

# broadcaster has type of ""
Module = NamedTuple('Module', [('type', str), ('destinations', list[str])])

Modules = dict[str, Module]

modules: Modules = {}

# we also need to know all inputs for conjunction modules

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
        for i in range(100):
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

# basic system
modules['broadcaster'] = Module('', ['Xinput'])
modules['Xinput'] = Module('%', ['X'])
modules['X'] = Module('&', ['Xinput', 'Xoutput'])
modules['Xoutput'] = Module('&', ['preout'])
modules['preout'] = Module('&', ['output'])

machine = Machine(modules)
# print(machine.analyze_structure())
analysis: dict[int, tuple[set[int], int, int]] = {}

for i in range(0, 32):
    test_modules = deepcopy(modules)
    b_digits: list[bool] = list(reversed([b == '1' for b in bin(i)[2:]]))
    for b, digit in enumerate(b_digits):
        current_name = 'X' + str(b)
        if b == 0:
            prev_name = 'Xinput'
        else:
            prev_name = 'X' + str(b - 1)
        test_modules[prev_name].destinations.append(current_name)
        test_modules[current_name] = Module('%', [])
        # 1 is arrow from digit to bus
        # 0 is arrow from bus to digit
        if digit:
            test_modules[current_name].destinations.append('X')
        else:
            test_modules['X'].destinations.append(current_name)

    test_machine = Machine(test_modules)
    analysis[i] = test_machine.analyze_structure()
for i, info in analysis.items():
    print (f'{i}:\t {bin(i)[2:]}\t{info[1]} {info[2] - info[1]}\t{sorted(info[0])[:10]}')
