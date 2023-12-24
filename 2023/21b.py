#!/usr/bin/env python3
import sys
from positions import Position, Direction, add_direction, cardinal_directions
import dataclasses
from typing import NamedTuple
from collections import defaultdict

filename = sys.argv[1]
steps = int(sys.argv[2])

Grid = set[Position]
walls: Grid = set()
start_position: Position = ()

with open(filename, "r") as f:
    for j, line in enumerate(f):
        line = line.rstrip()
        width = len(line)
        for i, char in enumerate(line.rstrip()):
            if char == '#':
                walls.add((i, j))
            elif char == 'S':
                start_position = (0, 0, i, j)
height = j + 1
sizes: Position = (width, height)
if height != width:
    raise ValueError("odd plots")

if start_position == ():
    raise ValueError("no start position!")

reachable: dict[int, set[Position]] = {0: {start_position}}

@dataclasses.dataclass
class PlotInfo:
    start: int                   # timestep of first contact
    fills: list[set[Position]] = dataclasses.field(default_factory=list)
    # set of subpositions filled at each subsequent step
    loop_start: int = -1
    loop_length: int = 0

# key is first two elements of position
plot_tracker: dict[Position, PlotInfo] = {}

FillPattern = NamedTuple('FillPattern', [
    ('loop_start', int),
    ('loop_length', int),
    ('reachables', tuple[frozenset[Position], ...]),
])

plots_for_pattern: dict[FillPattern, list[tuple[Position, int]]] = defaultdict(list)
pattern_for_plot: dict[Position, tuple[FillPattern, int]] = {}
next_number = 0
number_for_pattern: dict[FillPattern, int] = {}

repetition_directions: set[Direction] = set()

def unit_direction(dir: Direction) -> Direction:
    # clamp components to (-1, 0, 1)
    components: list[int] = []
    for x in dir:
        if x == 0:
            components.append(0)
        else:
            components.append(x // abs(x))
    return tuple(components)

def rolling_add_direction(pos: Position, dir: Direction) -> Position:
    subposition = pos[2:]
    subresult = add_direction(subposition, dir)
    result = list(pos[:2] + subresult)
    for i in range(2):
        j = i + 2
        if result[j] < 0:
            result[i] -= 1
            result[j] %= sizes[i]
        elif result[j] >= sizes[i]:
            result[i] += 1
            result[j] %= sizes[i]
    return tuple(result)

def wall_check(positions: set[Position]) -> set[Position]:
    new_result: set[Position] = set()
    for pos in positions:
        if pos[2:] not in walls:
            new_result.add(pos)
    return new_result

def known_check(positions: set[Position]) -> set[Position]:
    new_result: set[Position] = set()
    for pos in positions:
        if pos[:2] not in pattern_for_plot:
            new_result.add(pos)
    return new_result

for i in range(1, 10000):
    last_steps = reachable[i - 1]
    next_steps = set(rolling_add_direction(last, dir) for last in last_steps for dir in cardinal_directions)
    next_steps = known_check(next_steps)
    next_steps = wall_check(next_steps)
    reachable[i] = next_steps
    plot_positions: set[Position] = { p[:2] for p in next_steps }
    for plot_pos in plot_positions:
        if plot_pos not in plot_tracker:
            plot_tracker[plot_pos] = PlotInfo(i, [])
        plot_info = plot_tracker[plot_pos]
        if plot_info.loop_length > 0:
            continue
        plot_fill = { p[2:] for p in next_steps if p[:2] == plot_pos }
        fills = plot_info.fills
        if plot_fill in fills:
            loop_start = fills.index(plot_fill)
            loop_length = len(fills) - loop_start
            plot_info.loop_start = loop_start
            plot_info.loop_length = loop_length
            fill_pattern = FillPattern(loop_start, loop_length, tuple(frozenset(s) for s in fills))
            if fill_pattern not in number_for_pattern:
                number_for_pattern[fill_pattern] = next_number
                next_number += 1
            else:
                # repeated pattern - lock this direction
                repetition_directions.add(unit_direction(plot_pos))
            start = plot_info.start
            plots_for_pattern[fill_pattern].append((plot_pos, start))
            pattern_for_plot[plot_pos] = (fill_pattern, start)
        else:
            fills.append(plot_fill)
    if len(repetition_directions) == 8:
        break

def points_for_pattern(pattern: FillPattern, steps: int) -> int:
    if steps < 0:
        return 0
    if steps < pattern.loop_start:
        return len(pattern.reachables[steps])
    else:
        # print(f"hitting pseudostep at {steps} for pattern {number_for_pattern[pattern]}")
        pseudostep = (steps - pattern.loop_start) % pattern.loop_length + pattern.loop_start
        return len(pattern.reachables[pseudostep])

total_reachable = 0
# figure return for every pattern type
for pattern, plots in plots_for_pattern.items():
    if len(plots) == 1:
        # just add this one
        total_reachable += points_for_pattern(pattern, steps - plots[0][1])
    else:
        # repeating system
        start_plot = plots[0]
        first_start = start_plot[1]
        last_repeat = (steps - first_start) // width
        extra = (steps - first_start) % width
        # the right thing to do is to use squares and rectangles for most of this
        # but maybe we can just run like this
        if 0 in start_plot[0]:
            print(f"linear range: {last_repeat}")
            for i in range(last_repeat + 1):
                total_reachable += points_for_pattern(pattern, steps - plots[0][1] - width * i)
        else:
            print(f"triangular range: {last_repeat}")
            for i in range(last_repeat + 1):
                total_reachable += (i + 1) * points_for_pattern(pattern, steps - plots[0][1] - width * i)
print(total_reachable)

if False:
    for j in range(-4, 5):
        for i in range(-4, 5):
            plot_pos = (i, j)
            if plot_pos in pattern_for_plot:
                pattern, start = pattern_for_plot[plot_pos]
                pattern_name = chr(ord("A") + number_for_pattern[pattern])
                print(f"{pattern_name} {start}\t", end="")
            else:
                print("\t", end="")
        print()

if False:
    for plot_pos in sorted(plot_tracker.keys()):
        plot_info = plot_tracker[plot_pos]
        print(
            [sorted(s) for s in plot_info.fills[:4]],
            plot_info.start,
            plot_info.loop_start,
            plot_info.loop_length,
            plot_pos,
        )
