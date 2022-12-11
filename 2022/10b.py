#!/usr/bin/env python3
import sys

filename = sys.argv[1]
with open(filename, "r") as f:
    register: int = 1
    data: dict[str, int] = {"now": 1}
    raster: list[str] = []

    def tick() -> None:
        if abs(register + 1 - data['now']) <= 1:
            raster.append('#')
        else:
            raster.append('.')
        # print(''.join(raster))
        # print(' ' * register + '^')
        data['now'] += 1

        if data['now'] % 40 == 1:
            print(''.join(raster))
            raster.clear()
            data['now'] = 1

    for line in f:
        if line.startswith('noop'):
            tick()
        elif line.startswith('addx'):
            tick()
            tick()
            argument = line.split()[1]
            register += int(argument)
        else:
            raise ValueError(f"bad line {line}")
