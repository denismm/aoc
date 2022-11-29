#!/usr/bin/env python3
import sys
import re
import collections

filename = sys.argv[1]

chip_re = re.compile(r"value (\d+) goes to bot (\d+)")
bot_re = re.compile(r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)")

bot_inventory = collections.defaultdict(list)
outputs = {}
comparisons = {}

with open(filename, "r") as f:
    bot_rules = {}
    chip_rules = []
    for line in f:
        m = chip_re.match(line)
        if m:
            (chip, bot) = m.groups()
            chip = int(chip)
            bot = int(bot)
            chip_rules.append((chip, bot))
        else:
            m = bot_re.match(line)
            if m:
                (bot, t_a, id_a, t_b, id_b) = list(m.groups())
                bot = int(bot)
                id_a = int(id_a)
                id_b = int(id_b)
                if bot in bot_rules:
                    raise KeyError(f"two rules for bot {bot}")
                targets = (t_a, id_a), (t_b, id_b)
                bot_rules[bot] = targets
            else:
                raise ValueError(f"Can't parse line {line}")
    # handle chip rules
    for rule in chip_rules:
        (value, bot) = rule
        bot_inventory[bot].append(value)

    def parse_rule(bot):
        inventory = bot_inventory[bot]
        if len(inventory) > 2:
            raise ValueError(f"bot {bot} has too many chips")
        inventory.sort()
        comparisons[tuple(inventory)] = bot
        print(f"bot {bot} comparing {inventory}")
        for (chip, target) in zip(inventory, bot_rules[bot]):
            (type, id) = target
            if type == "bot":
                print(f"bot {id} got chip {chip}")
                bot_inventory[id].append(chip)
            elif type == "output":
                if id in outputs:
                    raise ValueError(f"Overflowing output {output}")
                print(f"output {id} got chip {chip}")
                outputs[id] = chip
            else:
                raise ValueError(f"unknown type in {type}")
        bot_inventory[bot] = []

    while True:
        acting_bots = [b for b, i in bot_inventory.items() if len(i) > 1]
        if len(acting_bots) == 0:
            break
        for bot in acting_bots:
            parse_rule(bot)
    print(comparisons[(17, 61)])
