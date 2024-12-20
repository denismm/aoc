#!/usr/bin/env python3
import sys

player_count = int(sys.argv[1])
last_marble = int(sys.argv[2])

scores: list[int] = [0] * player_count

circle: list[int] = [0]
current = 0             # index into circle
current_player = 0      # index into player_scores

for marble in range(1, last_marble + 1):
    if marble % 23 == 0:
        scores[current_player] += marble
        current = (current - 7) % len(circle)
        scores[current_player] += circle.pop(current)
    else:
        new_pos = (current + 2) % len(circle)
        circle.insert(new_pos, marble)
        current = new_pos
    current_player = (current_player + 1) % player_count

    if marble % 10_000 == 0:
        print(marble // 10_000, end=" ", flush=True)

print(max(scores))

