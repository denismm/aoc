#!/usr/bin/env python3
import sys
import re
import math
import copy
from typing import NamedTuple, Optional

TIME_LIMIT = 24

blueprint_re = re.compile(r'Blueprint (\d+):\s*'
  r'Each ore robot costs (\d+) ore.\s*'
  r'Each clay robot costs (\d+) ore.\s*'
  r'Each obsidian robot costs (\d+) ore and (\d+) clay.\s*'
  r'Each geode robot costs (\d+) ore and (\d+) obsidian.')

Blueprint = tuple[int, ...]

blueprints: list[Blueprint] = []

filename = sys.argv[1]
with open(filename, "r") as f:
    for line in f:
        if m := blueprint_re.match(line):
            blueprint_numbers = [int(x) for x in m.groups()]
            blueprint = tuple(blueprint_numbers)
            blueprints.append(blueprint)
        else:
            raise ValueError("couldn't parse line {line}")

Stock = list[int]
Bots = list[int]
Cost = list[list[int]]
State = NamedTuple( 'State', [
    ('stock', Stock), ('bots', Bots), ('time', int), ('route', list[int])])
def evaluate_blueprint(blueprint: Blueprint) -> int:
    blueprint_num = blueprint[0]
    costs: Cost = [ [0] * 3 for _ in range(4)]
    costs[0][0] = blueprint[1]
    costs[1][0] = blueprint[2]
    costs[2][0] = blueprint[3]
    costs[2][1] = blueprint[4]
    costs[3][0] = blueprint[5]
    costs[3][2] = blueprint[6]

    start_stock = [0] * 4
    start_bots = [1, 0, 0, 0]
    start_time = 0
    start_state = State(start_stock, start_bots, start_time, [])

    best_score = 0
    stack = [start_state]
    print(costs)
    while stack:
        state = stack.pop()
        # print(f"===handling state {state.bots}")
        time_left = TIME_LIMIT - state.time
        end_score = state.stock[3] + state.bots[3] * time_left
        if end_score > best_score:
            best_score = end_score
            print(f"new best score: {best_score} ({state})")
        for next_bot in range(4):
            bot_cost = costs[next_bot]
            # print(f"bot cost for {next_bot} is {bot_cost}")
            time_needed: Optional[int] = 0
            for r in range(3):  # resource
                if state.bots[r] == 0:
                    if bot_cost[r] > 0:
                        # print(f"can't make bot {next_bot} due to resource {r}")
                        time_needed = None
                        break
                else:
                    resource_needed = max(0, bot_cost[r] - state.stock[r])
                    time_to_bot = math.ceil(resource_needed / state.bots[r])
                    # print(f"time to bot for resource {r} is {time_to_bot}")
                    if time_left - time_to_bot < 2:
                        # can't make this bot and profit from it
                        # print(f"not enough time to make bot {next_bot}")
                        time_needed = None
                        break
                    if time_to_bot > time_needed:  # type: ignore[operator]
                        time_needed = time_to_bot
            if time_needed is not None:
                # print(f"time needed is {time_needed}")
                # run forward to make bot, make bot, one more step
                new_stock = [ s + b * time_needed for s, b in zip(state.stock, state.bots)]
                new_time = state.time + time_needed
                new_bots = copy.copy(state.bots)
                for r, r_count in enumerate(bot_cost):
                    new_stock[r] -= r_count
                for r, r_income in enumerate(new_bots):
                    new_stock[r] += r_income
                new_time += 1
                new_bots[next_bot] += 1
                new_state = State(new_stock, new_bots, new_time, state.route + [next_bot])
                # print(f"=adding {new_state.route}")
                stack.append(new_state)
    return blueprint_num * best_score

full_score = 0
for blueprint in blueprints:
    score = evaluate_blueprint(blueprint)
    print(f"blueprint {blueprint[0]} of {len(blueprints)}: {score}")
    full_score += score
print(f"full score is {full_score}")
