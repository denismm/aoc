#!/usr/bin/env python3
import sys
import re
import collections
from typing import NamedTuple

Room = NamedTuple('Room', [('name', str), ('rate', int), ('tunnels', list[str])])
START_ROOM = 'AA'
TIME_LIMIT = 30
rooms: dict[str, Room] = {}
valve_re = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]+)')

filename = sys.argv[1]
with open(filename, "r") as f:
    for line in f:
        if m := valve_re.match(line):
            name, rate_str, tunnels_str = m.groups()
            rate = int(rate_str)
            tunnels = tunnels_str.split(', ')
            rooms[name] = Room(name, rate, tunnels)
        else:
            raise ValueError(f"couldn't parse line: {line}")

# find distances between useful rooms
source_rooms = set([k for k, r in rooms.items() if r.rate > 0])
source_rooms.add(START_ROOM)
distances: dict[str, dict[str, int]] = {}
for source_room in source_rooms:
    local_distances: dict[str, int] = {source_room: 0}
    queue: collections.deque[str] = collections.deque([source_room])
    while len(queue):
        room = queue.popleft()
        current_dist = local_distances[room]
        room_obj = rooms[room]
        for destination in room_obj.tunnels:
            if destination not in local_distances:
                local_distances[destination] = current_dist + 1
                queue.append(destination)
    distances[source_room] = {room: distance for room, distance in local_distances.items() if rooms[room].rate > 0 and room != source_room}

# run simulation, depth-first
best_route: list[str] = []
best_total = 0

State = NamedTuple('State', [
    ('room', str),
    ('route', tuple[str, ...]),
    ('time', int),
    ('total', int),
    ('opened', frozenset[str]),
])

first_state = State(START_ROOM, (), 0, 0, frozenset())
room_stack = [first_state]
while len(room_stack):
    state = room_stack.pop()
    # print(f'handling {state}')
    room = state.room
    room_obj = rooms[room]
    new_time = state.time
    route = list(state.route) + [room]
    opened = set(state.opened)
    total = state.total
    # open it, why else did we come here?
    if room_obj.rate > 0:
        new_time += 1
        opened.add(room)
        total += room_obj.rate * (TIME_LIMIT - new_time)
        if total > best_total:
            best_total = total
            best_route = route
    # print(f"distances from {room}: {distances[room]}")
    for next_room, distance in distances[room].items():
        if next_room not in opened and new_time + distance < TIME_LIMIT :
            # print(f"trying {route} + {next_room}")
            room_stack.append(State(next_room, tuple(route), new_time + distance, total, frozenset(opened)))
print(best_route, best_total)
