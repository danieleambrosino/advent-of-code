import numpy


def count_accessible_rolls(grid: numpy.ndarray) -> int:
    rows, cols = grid.shape
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != "@":
                continue
            neighborhood = grid[
                max(0, r - 1) : min(rows, r + 2), max(0, c - 1) : min(cols, c + 2)
            ]
            if len(neighborhood[neighborhood == "@"]) <= 4:
                count += 1
    return count


def main() -> None:
    with open("input.txt") as file:
        grid = numpy.array([list(line) for line in file.read().strip().splitlines()])
    print(count_accessible_rolls(grid))


if __name__ == "__main__":
    main()
