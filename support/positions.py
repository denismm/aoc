from io import TextIOBase
from typing import Optional

Position = tuple[int, ...]
Direction = Position

SetGrid = set[Position]
StrGrid = dict[Position, str]
FrozenSetGrid = frozenset[Position]


def read_set_grid(f: TextIOBase, symbol: str = '#') -> tuple[int, int, SetGrid]:
    width = 0
    height = 0
    grid: SetGrid = set()
    for y, line in enumerate(f):
        line = line.rstrip()
        if line == "":
            break
        if not width:
            width = len(line)
        for x, char in enumerate(line):
            if char == symbol:
                grid.add((x, y))
    if len(grid) == 0:
        raise ValueError("empty grid")
    height = y + 1
    return width, height, grid


def read_char_grid(
    f: TextIOBase,
    skip_dots: bool = True,
    transformation: Optional[dict[str, str]] = None,
) -> tuple[int, int, StrGrid]:
    width = 0
    height = 0
    grid: StrGrid = {}
    for y, line in enumerate(f):
        line = line.rstrip()
        if line == "":
            break
        if transformation is not None:
            line = ''.join([transformation.get(c, c) for c in line])
        if not width:
            width = len(line)
        for x, char in enumerate(line):
            if skip_dots and char == ".":
                continue
            grid[(x, y)] = char
    if len(grid) == 0:
        raise ValueError("empty grid")
    height = y + 1
    return width, height, grid


def print_set_grid(width: int, height: int, grid: SetGrid) -> str:
    output: str = ""
    for y in range(height):
        for x in range(width):
            s: str = '.'
            if (x, y) in grid:
                s = '#'
            output += s
        output += "\n"
    return output


def print_char_grid(width: int, height: int, grid: StrGrid) -> str:
    output: str = ""
    for y in range(height):
        for x in range(width):
            position = (x, y)
            s: str = '.'
            if position in grid:
                s = grid[position]
            output += s
        output += "\n"
    return output


FloatDirection = tuple[float, ...]

cardinal_directions: tuple[Direction, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
direction_symbols = ">v<^"
udlr_symbols = "RDLU"
news_symbols = "ESWN"
direction_for_symbol = {k: v for k, v in zip(direction_symbols, cardinal_directions)}
symbol_for_direction = {k: v for k, v in zip(cardinal_directions, direction_symbols)}
direction_for_udlr = {k: v for k, v in zip(udlr_symbols, cardinal_directions)}
direction_for_news = {k: v for k, v in zip(news_symbols, cardinal_directions)}
zeta_directions: tuple[Direction, ...] = tuple(
    (x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x or y
)


def add_direction(position: Position, dir: Direction) -> Position:
    return tuple([p + d for p, d in zip(position, dir)])


def scale_direction(dir: Direction, scale: int) -> Direction:
    return tuple(d * scale for d in dir)


def get_direction(source: Position, target: Position) -> Direction:
    return tuple([t - s for s, t in zip(source, target)])


def manhattan(source: Position, target: Position) -> int:
    return sum([abs(s - t) for s, t in zip(source, target)])
