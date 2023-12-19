Position = tuple[int, ...]
Direction = Position

cardinal_directions: tuple[Direction, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
direction_symbols = ">v<^"
udlr_symbols = "RDLU"
direction_for_symbol = { k: v for k, v in zip(direction_symbols, cardinal_directions)}
direction_for_udlr = { k: v for k, v in zip(udlr_symbols, cardinal_directions)}
zeta_directions: tuple[Direction, ...] = tuple( (x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x or y)

def add_direction(position: Position, dir: Direction) -> Position:
    return tuple([p + d for p, d in zip(position, dir)])

def scale_direction(dir: Direction, scale: int) -> Direction:
    return tuple( d * scale for d in dir )

def get_direction(source: Position, target: Position) -> Direction:
    return tuple([t - s for s, t in zip(source, target)])

def manhattan(source: Position, target: Position) -> int:
    return sum([abs(s - t) for s, t in zip(source, target)])
