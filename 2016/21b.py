#!/usr/bin/env python3
import sys
import re

start_password = sys.argv[1]
filename = sys.argv[2]
global password
password = list(start_password)

swap_pos_re = re.compile(r'swap position (\d+) with position (\d+)')
swap_letter_re = re.compile(r'swap letter (\w) with letter (\w)')
rot_steps_re = re.compile(r'rotate (left|right) (\d+) steps?')
rot_letter_re = re.compile(r'rotate based on position of letter (\w)')
reverse_re = re.compile(r'reverse positions (\d+) through (\d+)')
move_re = re.compile(r'move position (\d+) to position (\d+)')

def swap_pos(a: int, b: int) -> None:
    swap = password[a]
    password[a] = password[b]
    password[b] = swap

def rotate_steps(direction: str, steps: int, forward=True) -> None:
    global password
    if (direction == 'left') ^ forward:
        steps = len(password) - steps
    password = password[steps:] + password[:steps]

def reverse_range(a: int, b: int) -> None:
    global password
    reversed_section: list[str] = list(reversed(password[a:b+1]))
    password = password[:a] + reversed_section + password[b+1:]

# for a length, what does a rotate at a position turn into?
rotate_maps: dict[int, list[int]] = {
    5: [1, 3, 0, 2, 0],
    8: [1, 3, 5, 7, 2, 4, 6, 0]
} 

rotate_map = rotate_maps[len(password)]

def mutate(instruction: str, forward=True) -> None:
    if (m := swap_pos_re.match(instruction)):
        a = int(m.group(1))
        b = int(m.group(2))
        swap_pos(a, b)
    elif (m := swap_letter_re.match(instruction)):
        a = password.index(m.group(1))
        b = password.index(m.group(2))
        swap_pos(a, b)
    elif (m := rot_steps_re.match(instruction)):
        direction = m.group(1)
        steps = int(m.group(2))
        rotate_steps(direction, steps, forward)
    elif (m := rot_letter_re.match(instruction)):
        letter = m.group(1)
        if forward:
            steps = password.index(letter)
            if steps >= 4:
                steps += 1
            steps += 1
            rotate_steps('right', steps)
        else:
            scramble_pos = password.index(letter)
            if scramble_pos not in rotate_map:
                raise ValueError(f"invalid position {scramble_pos} of {letter} in {password}")
            plain_positions = [i for i in range(len(password)) if rotate_map[i] == scramble_pos]

            plain_pos = plain_positions[-1]
            steps = (scramble_pos - plain_pos) % len(password)
            rotate_steps('right', steps, forward=False)
    elif (m := reverse_re.match(instruction)):
        a = int(m.group(1))
        b = int(m.group(2))
        reverse_range(a, b)
    elif (m := move_re.match(instruction)):
        a = int(m.group(1))
        b = int(m.group(2))
        if not forward:
            (a, b) = (b, a)
        letter = password.pop(a)
        password.insert(b, letter)
    else:
        print(f"unrecognized instruction {instruction}")

with open(filename, 'r') as f:
    lines = reversed(list(f))
    for i, line in enumerate(lines):
        operation = line.rstrip()
        prev_password = list(password)
        mutate(operation, forward=False)
        saved_password = list(password)
        mutate(operation, forward=True)
        if password != prev_password:
            raise ValueError(f"asymmetry on {operation}: {prev_password} -> {saved_password} -> {password}")
        password = saved_password
print(''.join(password))
