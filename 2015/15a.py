#!/usr/bin/env python3
import sys
from copy import copy
from collections import Counter
from itertools import product

filename = sys.argv[1]

Ingredient = dict[str, int]
ingredients: dict[str, Ingredient] = {}

with open(filename, "r") as f:
    for line in f:
        line.rstrip()
        ing_name, properties = line.split(": ")
        scratch_ing: Ingredient = {}
        for prop in properties.split(", "):
            prop_name, prop_amount_s = prop.split(" ")
            scratch_ing[prop_name] = int(prop_amount_s)
        ingredients[ing_name] = scratch_ing


def score(teaspoons: dict[str, int]) -> int:
    totals: Counter[str] = Counter()
    for ing_name, amount in teaspoons.items():
        # print(f"{ing_name} * {amount}")
        for prop_name, prop_amount in ingredients[ing_name].items():
            totals[prop_name] += prop_amount * amount
            # print(f"  {prop_name}: {prop_amount * amount}")
    total = 1
    # print("===")
    for prop_name, x in totals.items():
        if prop_name == "calories":
            continue
        # print(f"{prop_name} {x}")
        if x < 0:
            total = 0
        else:
            total *= x
    return total


# pick a starting state and search from there?
total_tsp = 100
ings_n = len(ingredients)
current_amts: dict[str, int] = {
    ing_name: total_tsp // ings_n for ing_name in ingredients.keys()
}
if sum(current_amts.values()) != total_tsp:
    raise ValueError("bad start")
current_score = score(current_amts)

directions = list(product(ingredients.keys(), repeat=2))

peak = False
while not peak:
    next_amts: dict[str, int] = {}
    next_score = -1
    for dir in directions:
        try_amts = copy(current_amts)
        if try_amts[dir[0]] <= 0:
            continue
        try_amts[dir[0]] -= 1
        try_amts[dir[1]] += 1
        try_score = score(try_amts)
        if try_score > current_score and try_score > next_score:
            next_score = try_score
            next_amts = try_amts
    if next_score == -1:
        peak = True
    else:
        current_amts = next_amts
        current_score = next_score

print(current_score)
print(current_amts)
