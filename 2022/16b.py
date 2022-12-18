#!/usr/bin/env python3
import sys
import re
import collections
from typing import NamedTuple

Room = NamedTuple('Room', [('name', str), ('rate', int), ('tunnels', list[str])])
START_ROOM = 'AA'
TIME_LIMIT = 26
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
best_route: list[tuple[str, ...]] = [(), ()]
best_total = 0

PlayerState = NamedTuple('PlayerState', [
    ('room', str),
    ('route', tuple[str, ...]),
    ('time', int),
])
State = NamedTuple('State', [
    ('players', tuple[PlayerState, ...]),
    ('total', int),
    ('opened', frozenset[str]),
    ('interesting', bool),
])

player_start = tuple([PlayerState(START_ROOM, (), 0) for _ in range(2)])
first_state = State(player_start, 0, frozenset(), False)
state_stack = [first_state]
while len(state_stack):
    state = state_stack.pop()
    # print(f'handling {state}')
    # who is the active player?  Whoever has spent the least time.
    player_order = sorted(range(2), key=lambda i: state.players[i].time)
    player = player_order[0]
    player_obj = state.players[player]
    other_player = player_order[1]  # this would need to change for more players
    other_player_obj = state.players[other_player]
    room = player_obj.room
    opened = set(state.opened)
    if state.interesting:
        print(f"got to room {room} at {player_obj.time}, other player is at {other_player_obj.room}, opened is {opened}")
    if room in opened:
        # the other player beat this one here
        print(f"we got beat to {room}")
        continue
    room_obj = rooms[room]
    new_time = player_obj.time
    route = list(player_obj.route) + [room]
    total = state.total
    # open it, why else did we come here?
    if room_obj.rate > 0:
        new_time += 1
        opened.add(room)
        total += room_obj.rate * (TIME_LIMIT - new_time)
        if total > best_total:
            best_total = total
            best_route = [tuple(route), state.players[other_player].route]
            stack_bottom = [p.route for p in state_stack[0].players]
            print(f"better route with total {total} at time {new_time}, stack at {len(state_stack)}, stack bottom is {stack_bottom}")
    # print(f"distances from {room}: {distances[room]}")
    for next_room, distance in distances[room].items():
        if next_room not in opened and new_time + distance < TIME_LIMIT :
            # special case - don't go to the same room after your partner
            # why doesn't this work?  If I change pass to continue, I
            # get a worse answer.
            interesting = False
            if other_player_obj.room == next_room and other_player_obj.time < new_time + distance:
                print(f"adding despite duplication, our time is {new_time + distance}, theirs is {other_player_obj.time}, going to {next_room}")
                interesting = True
                pass
            # print(f"trying {route} + {next_room}")
            new_player_obj = PlayerState(next_room, tuple(route), new_time + distance)
            new_state = State(
                (new_player_obj, other_player_obj),
                total, frozenset(opened), interesting
            )
            state_stack.append(new_state)
print(best_route, best_total)
