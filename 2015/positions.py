Position = tuple[int, ...]
Direction = Position

cardinal_directions: tuple[Direction, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
direction_symbols = ">v<^"
direction_for_symbol = { k: v for k, v in zip(direction_symbols, cardinal_directions)}

def add_direction(position: Position, dir: Direction) -> Position:
    return tuple([p + d for p, d in zip(position, dir)])
