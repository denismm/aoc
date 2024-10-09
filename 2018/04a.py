#!/usr/bin/env python3
import sys
from collections import defaultdict, Counter

filename = sys.argv[1]

Shift = list[int]       # sleep/wake events during midnight hour
Guard = dict[str, Shift]        # date -> Shift

post: dict[int, Guard] = defaultdict(lambda: {})

with open(filename, "r") as f:
    current_guard = -1
    current_shift: Shift = []
    for line in f:
        date, time, message = line.split(maxsplit=2)
        date = date.lstrip('[')
        time = time.rstrip(']')
        message = message.rstrip()
        if 'begins shift' in message:
            id_s = message.split()[1]
            current_guard = int(id_s.lstrip('#'))
            current_shift = []
            post[current_guard][date] = current_shift
        else:
            if message == 'falls asleep':
                if len(current_shift) % 2 == 1:
                    raise ValueError(f"sleep parity error {line}")
            else:
                if len(current_shift) % 2 == 0:
                    raise ValueError("wake parity error")
            minutes = int(time[3:])
            current_shift.append(minutes)

sleep_total: Counter[int] = Counter()
sleepytimes: dict[int, Counter[int]] = defaultdict(lambda: Counter())
for id, guard in post.items():
    for date, shift in guard.items():
        for i in range(0, len(shift), 2):
            sleep = shift[i]
            wake = shift[i+1]
            sleep_total[id] += wake - sleep
            for minute in range(sleep, wake):
                sleepytimes[id][minute] += 1
most_sleep = max(sleep_total.values())
sleepy_guard = [id for id, mins in sleep_total.items() if mins == most_sleep][0]
most_shifts = max(sleepytimes[sleepy_guard].values())
sleepy_minute = [min for min, shifts in sleepytimes[sleepy_guard].items() if shifts == most_shifts][0]

print(f"{sleepy_guard} * {sleepy_minute} = {sleepy_guard * sleepy_minute}")

big_sleep_for_guard: dict[int, int] = {}
for id, sleeps in sleepytimes.items():
    big_sleep_for_guard[id] = max(sleeps.values())
biggest_sleep = max(big_sleep_for_guard.values())
sleepiest_guard = [id for id, sleeps in big_sleep_for_guard.items() if sleeps == biggest_sleep][0]
sleepiest_minute = [min for min, shifts in sleepytimes[sleepiest_guard].items() if shifts == biggest_sleep][0]
print(f"{sleepiest_guard} * {sleepiest_minute} = {sleepiest_guard * sleepiest_minute}")
