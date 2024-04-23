#!/usr/bin/env python3
import sys
from positions import Position, zeta_directions, add_direction, read_char_grid

filename = sys.argv[1]
grid: dict[Position, str] = {}
with open(filename, 'r') as f:
    _, _, grid = read_char_grid(f)
symbol_locations = [k for k, v in grid.items() if not v.isdigit()]
total = 0
ratio_total = 0
for p in symbol_locations:
    symbol = grid[p]
    numbers: list[int] = []
    for d in zeta_directions:
        np = add_direction(p, d)
        if grid.get(np, '').isdigit():
            number_positions = [np]
            for lr_direction in (-1, 1):
                step = lr_direction
                while True:
                    maybe_number = add_direction(np, (step, 0))
                    if grid.get(maybe_number, '').isdigit():
                        number_positions.append(maybe_number)
                        step += lr_direction
                    else:
                        break
            number = 0
            for dp in sorted(number_positions):
                number *= 10
                number += int(grid[dp])
                del grid[dp]
            numbers.append(number)
    # print(f"{symbol}: {numbers}")
    if symbol == '*' and len(numbers) == 2:
        ratio_total += numbers[0] * numbers[1]
    total += sum(numbers)

print("part total:", total)
print("ratio total:", ratio_total)
