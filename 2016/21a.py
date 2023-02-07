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

def rotate_steps(direction: str, steps: int) -> None:
    global password
    if direction == 'right':
        steps = len(password) - steps
    password = password[steps:] + password[:steps]

def reverse_range(a: int, b: int) -> None:
    global password
    reversed_section: list[str] = list(reversed(password[a:b+1]))
    password = password[:a] + reversed_section + password[b+1:]

def mutate(instruction: str) -> None:
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
        rotate_steps(direction, steps)
    elif (m := rot_letter_re.match(instruction)):
        steps = password.index(m.group(1))
        if steps >= 4:
            steps += 1
        steps += 1
        rotate_steps('right', steps)
    elif (m := reverse_re.match(instruction)):
        a = int(m.group(1))
        b = int(m.group(2))
        reverse_range(a, b)
    elif (m := move_re.match(instruction)):
        a = int(m.group(1))
        b = int(m.group(2))
        letter = password.pop(a)
        password.insert(b, letter)
    else:
        print(f"unrecognized instruction {instruction}")

with open(filename, 'r') as f:
    for line in f:
        mutate(line.rstrip())
        # print(''.join(password), line.rstrip())
print(''.join(password))
