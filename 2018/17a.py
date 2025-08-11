#!/usr/bin/env python3
import sys
import re
from positions import StrGrid, Position, Direction, add_direction

grid: StrGrid = {}

filename = sys.argv[1]

CLAY = "#"
STILL = "~"
FLOWING = "|"

with open(filename, 'r') as f:
    line_re = re.compile(r'([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)')
    for line in f:
        if m := line_re.match(line.rstrip()):
            axis_dim, position_s, range_dim, start_s, end_s = m.groups()
            axis_position = int(position_s)
            start_pos = int(start_s)
            end_pos = int(end_s)
            if axis_dim == range_dim:
                raise ValueError(f"bad line {line}")
            if start_pos > end_pos:
                raise ValueError(f"bad line {line}")
            for px in range(start_pos, end_pos + 1):
                pos: Position = (0, 0)
                if axis_dim == 'x':
                    pos = (axis_position, px)
                else:
                    pos = (px, axis_position)
                grid[pos] = CLAY
        else:
            raise ValueError(f"can't parse line {line}")

xs: set[int] = set([pos[0] for pos in grid.keys()])
ys: set[int] = set([pos[1] for pos in grid.keys()])
min_x = min(xs)
min_y = min(ys)
max_x = max(xs)
max_y = max(ys)

fountain_pos: Position = (500, 0)

def pretty_print() -> None:
    for y in range(0, max_y + 1):
        for x in range(min_x, max_x + 1):
            draw_pos = (x, y)
            dot = ""
            if draw_pos == fountain_pos:
                dot = "+"
            elif draw_pos in grid:
                dot = grid[draw_pos]
            else:
                dot = "."

            print(dot, end="")
        print()

# we can just skip ahead to the position below the fountain that's in range
flow_points: set[Position] = set([(500, min_y)])

class Overflow(Exception):
    pass

# end condition: all flow points y > max_y
# so remove flow points as they pass that
up: Direction = (0, -1)
down: Direction = (0, 1)
sides: tuple[Direction, ...] = ((1, 0), (-1, 0))
try:
    while (flow_points):
        new_flow_points: set[Position] = set()
        for flow_point in flow_points:
            down_pos = add_direction(flow_point, down)
            down_char = grid.get(down_pos, ".")
            if down_char in {CLAY, STILL}:
                # find edges
                puddle: set[Position] = {flow_point}
                spill: set[Position] = set()
                for direction in sides:
                    edge: Position = add_direction(flow_point, direction)
                    while True:
                        # print(f"checking {edge}")
                        edge_char = grid.get(edge, '.')
                        if edge_char == CLAY:
                            break
                        if edge[0] < (min_x - 1) or edge[0] > (max_x + 1):
                            raise Overflow(f"overflow {direction=} {edge=}")
                        down_pos = add_direction(edge, down)
                        down_char = grid.get(down_pos, ".")
                        if down_char in {CLAY, STILL}:
                            puddle.add(edge)
                            edge = add_direction(edge, direction)
                        else:
                            spill.add(edge)
                            break
                # react appropriately
                if spill:
                    for position in puddle:
                        grid[position] = FLOWING
                    new_flow_points |= spill
                else:
                    for position in puddle:
                        grid[position] = STILL
                    new_flow_points.add(add_direction(flow_point, up))
            else:
                grid[flow_point] = FLOWING
                # flow downward
                if down_pos[1] <= max_y:
                    new_flow_points.add(down_pos)
        flow_points = new_flow_points

except Overflow as e:
    print(e)
    max_y = max([pos[1] for pos in flow_points])
    pretty_print()
    exit()

# pretty_print()
water_tile_count = sum([1 for v in grid.values() if v in {STILL, FLOWING}])
print(water_tile_count)
still_water_count = sum([1 for v in grid.values() if v in {STILL}])
print(still_water_count)

