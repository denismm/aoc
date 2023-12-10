#!/usr/bin/env python3
import sys

filename = sys.argv[1]
firstbag = {'red': 12, 'green': 13, 'blue': 14}
total = 0
power_total = 0
def check_pulls(pulls: str) -> bool:
    for pull_s in pulls_s.split('; '):
        for cubes in pull_s.split(', '):
            count_s, color = cubes.split(' ')
            if int(count_s) > firstbag[color]:
                return False
    return True

def bag_power(pulls: str) -> int:
    bag: dict[str, int] = {}
    for pull_s in pulls_s.split('; '):
        for cubes in pull_s.split(', '):
            count_s, color = cubes.split(' ')
            cube_count = int(count_s)
            if cube_count > bag.get(color, 0):
                bag[color] = cube_count
    product = 1
    for cube_count in bag.values():
        product *= cube_count
    return product

with open(filename, 'r') as f:
    for line in f:
        game_name, pulls_s = line.rstrip().split(': ')
        game_id = int(game_name.split(' ')[1])
        if check_pulls(pulls_s):
            total += game_id
        power_total += bag_power(pulls_s)

print(f"possible game ID sum: {total}")
print(f"bag power total: {power_total}")
