#!/usr/bin/env python3
import sys
from dataclasses import dataclass

@dataclass
class Node:
    data: int
    prev: 'Node'
    next: 'Node'

    def __init__(self, data: int) -> None:
        self.data = data
        self.prev = self
        self.next = self

    def insert(self, prev: 'Node') -> None:
        next: 'Node' = prev.next
        prev.next = self
        self.prev = prev
        next.prev = self
        self.next = next

    def delete(self) -> None:
        self.prev.next = self.next
        self.next.prev = self.prev

    def print_circle(self) -> list[int]:
        output: list[int] = [self.data]
        pointer: Node = self.next
        while pointer != self:
            output.append(pointer.data)
            pointer = pointer.next
        return output

player_count = int(sys.argv[1])
last_marble = int(sys.argv[2])

scores: list[int] = [0] * player_count

current: Node = Node(0)
current_player = 0      # index into player_scores

for marble in range(1, last_marble + 1):
    if marble % 23 == 0:
        scores[current_player] += marble
        for _ in range(6):
            current = current.prev
        scores[current_player] += current.prev.data
        current.prev.delete()
    else:
        new_prev = current.next
        new_node = Node(marble)
        new_node.insert(new_prev)
        current = new_node
    current_player = (current_player + 1) % player_count

    if marble % 10_000 == 0:
        print(marble // 10_000, end=" ", flush=True)

    if False:
        print(current.print_circle())

print(max(scores))
