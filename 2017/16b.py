#!/usr/bin/env python3
import sys

filename = sys.argv[2]
dancers = int(sys.argv[1])

with open(filename, 'r') as f:
    moves = f.read().rstrip().split(',')

dance_line = [chr(ord('a') + i) for i in range(dancers)]

def exchange(dance_line: list[str], positions: list[int]) -> list[str]:
    programs = [dance_line[p] for p in positions]
    dance_line[positions[0]] = programs[1]
    dance_line[positions[1]] = programs[0]
    return dance_line

position_numbers: dict[str] = { "".join(dance_line) : 0 }
position_list: list[str] = [ "".join(dance_line) ]

repetition = 0
while True:
    repetition += 1
    for move in moves:
        command = move[0]
        args = move[1:]
        if command == 's':
            spin_size = int(args)
            dance_line = [dance_line[i - spin_size] for i in range(dancers)]
        elif command == 'x':
            positions = [int(x) for x in args.split('/')]
            dance_line = exchange(dance_line, positions)
        elif command == 'p':
            positions = [dance_line.index(name) for name in args.split('/')]
            dance_line = exchange(dance_line, positions)
        else:
            raise ValueError("bad move {move}")
    end_position = "".join(dance_line)
    if end_position in position_numbers:
        print(f'collision between {repetition} and {position_numbers[end_position]}')
        if position_numbers[end_position] != 0:
            raise ValueError("what?")
        endpoint = 1000000000 % repetition
        print(position_list[endpoint])
        exit(0)
    else:
        position_numbers[end_position] = repetition
        position_list.append(end_position)

