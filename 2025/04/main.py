import numpy

grid_str = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
grid = numpy.array([list(line) for line in grid_str.strip().splitlines()])
rows, cols = grid.shape
counter = 0
for r in range(rows):
    for c in range(cols):
        if grid[r, c] != "@":
            continue
        neighborhood = grid[
            max(0, r - 1) : min(rows, r + 2), max(0, c - 1) : min(cols, c + 2)
        ]
        if len(neighborhood[neighborhood == "@"]) <= 4:
            counter += 1
print(counter)
