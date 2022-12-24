#!/usr/bin/env python3
import sys
import pprint
import math
import functools
import collections
from typing import NamedTuple

Position = tuple[int, ...]

def add_pos(position: Position, dir: Position) -> Position:
    return tuple([p + d for p, d in zip(position, dir)])

def add_pos_with_loop(position: Position, dir: Position) -> Position:
    return tuple([(p + d) % m for p, d, m in zip(position, dir, maxes)])

wind_chars = ">v<^"
wind_starts: dict[str, set[Position]] = { wind: set() for wind in wind_chars }
open_spaces: set[Position] = set()

filename = sys.argv[1]
height = 0
width = 0
with open(filename, "r") as f:
    for y, line in enumerate(f, start=-1):
        if line.startswith('#.#'):
            width = len(line.rstrip()) - 2
        if line.startswith('###'):
            height = y
        for x, character in enumerate(line.rstrip(), start=-1):
            input_position = (x, y)
            if character != '#':
                open_spaces.add(input_position)
                if character in wind_chars:
                    wind_starts[character].add(input_position)

maxes = (width, height)
loops = {'>': width, '<': width, '^': height, 'v': height}
# same as order as winds, plus stay
directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]
wind_directions = {wind: direction
    for wind, direction in zip(wind_chars, directions[:4])}

# calculate winds for each tick
winds: dict[str, list[set[Position]]] = {}
for wind, starts in wind_starts.items():
    options: list[set[Position]] = [starts]
    direction = wind_directions[wind]
    # the other options
    for i in range(1, loops[wind]):
        options.append(set([add_pos_with_loop(p, direction) for p in options[-1]]))
    winds[wind] = options

full_loop = math.lcm(*maxes)
print(f"full loop is {full_loop}")

winds_for_tick: list[set[Position]] = [
    functools.reduce(lambda a, b: a | b,
        [options[tick % loops[wind]] for wind, options in winds.items()]
    )
    for tick in range(full_loop)
]

start_position = (0, -1)
end_position = (width - 1, height)
goal_positions = [end_position, start_position, end_position]

State = NamedTuple("State", [('location', Position), ('time', int), ('goals', int)])
start_state = State(start_position, 0, 0)
queue = collections.deque([start_state])
# seen states use time % full_loop
seen: set[State] = set([start_state])

def print_state(state: State) -> None:
    print(state.time)
    tick_winds = winds_for_tick[state.time % full_loop]
    for y in range(height):
        for x in range(width):
            pp = (x, y)
            if pp in tick_winds:
                print_char = '#'
            elif pp == state.location:
                print_char = 'E'
            else:
                print_char = '.'
            print(print_char, end="")
        print()

current_time = 0
while (queue):
    if queue[0].time != current_time:
        current_time = queue[0].time
        print(f"{current_time}: {len(queue)}")
    state = queue.popleft()
    # print_state(state)
    next_tick = (state.time + 1) % full_loop
    next_winds = winds_for_tick[next_tick]
    for direction in directions:
        new_position = add_pos(state.location, direction)
        new_goals = state.goals
        if new_position == goal_positions[new_goals]:
            new_goals += 1
        if new_goals == 3:
            print(state.time + 1)
            exit(0)
        if new_position in open_spaces and new_position not in next_winds:
            seen_state = State(new_position, next_tick, new_goals)
            if seen_state not in seen:
                seen.add(seen_state)
                queue.append(State(new_position, state.time + 1, new_goals))
print("no way out")
