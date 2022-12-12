from collections import deque

import numpy as np
from numpy import array
from numpy.typing import NDArray

with open(0) as file:
    heightmap = array([list(l.strip()) for l in file.readlines()])

start = np.hstack(np.where(heightmap == "S"))
end = np.hstack(np.where(heightmap == "E"))
heightmap[heightmap == "S"] = "a"
heightmap[heightmap == "E"] = "z"

frontier: deque[tuple[NDArray[np.intp], int]] = deque([(start, 0)])
visited: set[tuple[int, int]] = set()

while len(frontier) > 0:
    current, steps = frontier.popleft()
    neighbors = array([
        current + array([1, 0]),
        current + array([0, 1]),
        current + array([-1, 0]),
        current + array([0, -1]),
    ])
    # discard "easy" (-1) out of bounds
    neighbors = neighbors[(neighbors >= 0).all(axis=1)]
    for neighbor in neighbors:
        nt = tuple(neighbor)
        if nt in visited:
            continue
        try:
            if ord(heightmap[nt]) - ord(heightmap[tuple(current)]) > 1:
                continue
        except IndexError:
            # discard out of bounds
            continue
        if np.array_equal(neighbor, end):
            print(steps + 1)
            exit(0)
        visited.add(nt)
        frontier.append((neighbor, steps + 1))
