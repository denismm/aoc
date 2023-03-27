Position = tuple[int, ...]

cardinal_directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
direction_symbols = ">v<^"

def add_direction(position: Position, dir: Position) -> Position:
    return tuple([p + d for p, d in zip(position, dir)])
