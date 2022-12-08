#!/usr/bin/env python3
import sys
import re
import collections
from typing import Union, Pattern, DefaultDict

FileEntry = int
DirectoryEntry = dict[str, Union[FileEntry, "DirectoryEntry"]]

whitespace: Pattern[str] = re.compile(r"\s+")


filename = sys.argv[1]
with open(filename, "r") as f:
    disk: DirectoryEntry = {}
    position: list[str] = []

    def get_dir(position: list[str]) -> DirectoryEntry:
        pointer: DirectoryEntry = disk
        directory: str
        for directory in position:
            pointer = pointer[directory]  # type: ignore[assignment]
        return pointer

    def handle_cmd(line: str) -> None:
        command: list[str] = whitespace.split(line.rstrip())[1:]
        if command[0] == "cd":
            directory: str = command[1]
            if directory == "/":
                position.clear()
            elif directory == "..":
                position.pop()
            else:
                position.append(directory)
        elif command[0] == "ls":
            pass
        else:
            raise ValueError(f"unrecognized command {command}")

    def handle_file(line: str) -> None:
        detail: str
        name: str
        (detail, name) = whitespace.split(line.rstrip())
        current = get_dir(position)
        if detail == "dir":
            current[name] = {}
        else:
            current[name] = int(detail)

    for line in f:
        if line.startswith("$"):
            handle_cmd(line)
        else:
            handle_file(line)

    dir_size: DefaultDict[str, int] = collections.defaultdict(lambda: 0)

    def find_sizes(current_dir: str, pointer: DirectoryEntry) -> None:
        for (name, entry) in pointer.items():
            if isinstance(entry, int):
                dir_size[current_dir] += entry
            else:
                new_dir = current_dir + "/" + name
                find_sizes(new_dir, entry)
                dir_size[current_dir] += dir_size[new_dir]

    find_sizes("", disk)

    all_smalls: int = sum([size for size in dir_size.values() if size <= 100000])
    print(f"all_smalls: {all_smalls}")

    delete_needed = dir_size[""] - 40000000
    delete_options = [size for size in dir_size.values() if size >= delete_needed]
    print(f"delete: {min(delete_options)}")
