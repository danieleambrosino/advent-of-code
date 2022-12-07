from collections import defaultdict
from itertools import accumulate

directories: dict[str, int] = defaultdict(int)
path: list[str] = []

with open("input.txt", "r") as file:
    for line in file:
        match line.strip().split():
            case "$", "ls": pass
            case "dir", _: pass
            case "$", "cd", "..": path.pop()
            case "$", "cd", directory: path.append(directory)
            case size, _:
                for directory in accumulate(path):
                    directories[directory] += int(size)
            case _: pass

print(sum(size for size in directories.values() if size <= 100_000))

total_space = 70_000_000
used_space = directories["/"]
needed_space = 30_000_000
shrinked_used_space = total_space - needed_space
# The minimum size that the directory to be removed should have
min_dir_size = used_space - shrinked_used_space

print(min(size for size in directories.values() if size >= min_dir_size))
